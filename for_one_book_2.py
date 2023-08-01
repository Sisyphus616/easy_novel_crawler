import os
import requests
from bs4 import BeautifulSoup
import re
import unicodedata

def get_valid_filename(s):
    # Remove any non-space whitespace characters and normalize the string to NFKC form
    s = re.sub(r'\s+', ' ', s)
    s = unicodedata.normalize('NFKC', s)
    # Remove any illegal characters for filenames
    return re.sub(r'[/\\?%*:|"<>]', '_', s)

def get_novel_chapters(url, start_index=10):
    response = requests.get(url)
    chapters = []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        novel_name = soup.find('div', {'id': 'list'}).find_all('dt')[1].text.strip()
        chapter_list = soup.find('div', {'id': 'list'}).find_all('dd')[start_index - 1:]
        
        for index, chapter in enumerate(chapter_list, start=start_index):
            chapter_title = chapter.a.text.strip()
            chapter_url = 'https://www.xpiaotian.com/zh_hant/book/269987/' + chapter.a['href']
            chapters.append((index - (start_index - 1), chapter_title, chapter_url))
        
        return novel_name, chapters
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
    return None, None

def get_chapter_content(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('div', {'id': 'content'})
        
        if content_div:
            # Replace <br> tags with newlines
            for br_tag in content_div.find_all('br'):
                br_tag.replace_with('\n')
            return content_div.text.strip()
        else:
            print("Could not find the chapter content.")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
    return None

def save_novel_to_files(novel_name, chapters):
    novel_folder = get_valid_filename(novel_name.replace('/', '／'))
    os.makedirs(novel_folder, exist_ok=True)
    
    for index, chapter_title, chapter_url in chapters:
        chapter_content = get_chapter_content(chapter_url)
        if chapter_content:
            file_name = os.path.join(novel_folder, f"{index:04d}_{get_valid_filename(chapter_title)}.txt")
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(chapter_content)
            print(f"Chapter '{chapter_title}' saved.")
        else:
            print(f"Failed to save chapter '{chapter_title}'.")

if __name__ == "__main__":
    novel_url = 'https://www.xpiaotian.com/zh_hant/book/269987/'  # Replace with the URL of the novel's table of contents page
    novel_name, chapters = get_novel_chapters(novel_url, start_index=10)
    if novel_name and chapters:
        save_novel_to_files(novel_name, chapters)
        print("小说下载完成。")