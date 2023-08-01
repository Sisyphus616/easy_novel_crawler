import requests
from bs4 import BeautifulSoup

def get_novel_content(url):
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
            print("Could not find the novel content.")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
    return None

if __name__ == "__main__":
    novel_url = 'https://www.mayiwxw.com/109_109408/44676790.html'
    novel_content = get_novel_content(novel_url)
    if novel_content:
        with open('novel.txt', 'w', encoding='utf-8') as file:
            file.write(novel_content)
        print("小说内容已保存到 'novel.txt' 文件。")
