import os
import subprocess

WORK_DIR = "D:\\Git\\Books"
MODEL_NAME = "deepseek-v4-pro"
OUTPUT_DIR = os.path.join(WORK_DIR, "735\\续写")
SOURCE_DIR = os.path.join(WORK_DIR, "735\\续写规划\\章节工作卡")
PROMPT_TEMPLATE = ""

def get_next_characters():
    file_list = os.listdir(OUTPUT_DIR)
    cur_characters = 0
    for file_name in file_list:
        # 提取文件名开头的数字部分（如 "280_天倾岛乱.txt" -> 280）
        prefix = file_name.split("_", 1)[0]
        if prefix.isdigit():
            num = int(prefix)
            if num > cur_characters:
                cur_characters = num

    return cur_characters + 1


def get_max_characters():
    file_list = os.listdir(SOURCE_DIR)
    max_characters = 0
    for file_name in file_list:
        # 提取文件名开头的数字部分（如 "280_天倾岛乱.txt" -> 280）
        prefix = file_name.split("_", 1)[0]
        if prefix.isdigit():
            num = int(prefix)
            if num > max_characters:
                max_characters = num

    return max_characters

def get_character_name(character):
    file_list = os.listdir(OUTPUT_DIR)
    for file_name in file_list:
        prefix = file_name.split("_", 1)[0]
        if prefix == f"{character}":
            return file_name


for character in range(get_next_characters(), get_max_characters() + 1):
    # 组装提示词：模板 + 章节编号 + 对应工作卡内容
    prompt = PROMPT_TEMPLATE + f"{character}"
    

    print(f"正在生成章节 {character} ...")
    subprocess.run(
        ["codebuddy", "-p", prompt, "--model", MODEL_NAME],
        check=True,
        shell=True,
    )
    
    