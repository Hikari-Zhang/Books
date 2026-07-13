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

def get_character_name(character, source_dir):
    file_list = os.listdir(source_dir)
    for file_name in file_list:
        prefix = file_name.split("_", 1)[0]
        if prefix == f"{character}":
            return file_name


for character in range(get_next_characters(), get_max_characters() + 1):
    source_file_name = get_character_name(character, SOURCE_DIR)
    source_file_path = os.path.join(SOURCE_DIR, source_file_name)

    previous_file_name1 = get_character_name(character - 1, OUTPUT_DIR)
    previous_file_path1 = os.path.join(OUTPUT_DIR, previous_file_name1)
    previous_file_name2 = get_character_name(character - 2, OUTPUT_DIR)
    previous_file_path2 = os.path.join(OUTPUT_DIR, previous_file_name2)

    # 组装提示词：模板 + 章节编号 + 对应工作卡内容
    prompt = PROMPT_TEMPLATE + f"{character}"
    print(f"正在生成章节 {character} ...")
    try:
        subprocess.run(
            ["codebuddy", "-p", prompt, "--model", MODEL_NAME],
            check=True,
            shell=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"错误：章节 {character} 生成失败（退出码 {e.returncode}），已停止运行。")
        raise
    
    