import os
import glob

def merge_txt_files(input_folder, output_file):
    # Get the list of TXT files
    txt_files = glob.glob(os.path.join(input_folder, '*.txt'))

    # Merge the contents of all TXT files with file names as labels
    merged_content = ''
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as f:
            file_name = os.path.splitext(os.path.basename(txt_file))[0]
            content = f.read()
            merged_content += f"文件名：{file_name}\n\n{content}\n\n"

    # Write the merged content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(merged_content)


if __name__ == "__main__":
    # setup_custom_font()  # 设置自定义字体
    input_folder = "./我有九千萬億舔狗金"
    output_file = "output.txt"
    merge_txt_files(input_folder, output_file)