import os
import subprocess

WORK_DIR = "/Users/hikari/Documents/books"
MODEL_NAME = "qwen3.6-35b"
OUTPUT_DIR: str = os.path.join(WORK_DIR, "735/续写")
SOURCE_DIR: str = os.path.join(WORK_DIR, "735/续写规划/章节工作卡")
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

def get_character_name(character, source_dir) -> str:
    file_list = os.listdir(source_dir)
    for file_name in file_list:
        prefix = file_name.split("_", 1)[0]
        if prefix == f"{character}":
            return file_name
    return ""


for character in range(get_next_characters(), get_max_characters() + 1):
    source_file_name: str = get_character_name(character, SOURCE_DIR)

    previous_file_name1: str = get_character_name(character - 1, OUTPUT_DIR)
    previous_file_name2: str = get_character_name(character - 2, OUTPUT_DIR)

    # 组装提示词：模板 + 章节编号 + 对应工作卡内容
    prompt = f"@{os.path.join(SOURCE_DIR, source_file_name)}\t" 
    prompt += f"@{os.path.join(WORK_DIR, "735/色情细节描述/_描写范式与典型范例.md")}\t"
    prompt += f"@{os.path.join(WORK_DIR, "735/续写规划/00_续写圣经.md")}\t" 
    prompt += f"@{os.path.join(WORK_DIR, "735/续写规划/02_战力与法宝设定表.md")}\t"
    prompt += f"@{os.path.join(WORK_DIR, "735/续写规划/03_核心人物弧光表.md")}\t"  
    prompt += f"@{os.path.join(WORK_DIR, "735/续写规划/05_情感线收束方案.md")}\t"
    prompt += f"@{os.path.join(WORK_DIR, "735/续写规划/09_正文创作流程.md")}\t"
    prompt += f"@{os.path.join(WORK_DIR, "735/续写规划")} 完成{character}章的内容制作, 需要承接 "
    prompt += f"@{OUTPUT_DIR} @{os.path.join(OUTPUT_DIR, previous_file_name2)} @{os.path.join(OUTPUT_DIR, previous_file_name1)} 的内容\t" 
    prompt += "要求章节过渡内容自然发展, 10000字以上. 这是一本色情仙侠小说需要有露骨的相欢内容. "
    prompt += f"生成在@{OUTPUT_DIR} 文件夹中. 以UTF-8的格式输出."

    print(f"正在生成章节 {character} ...")
    print(prompt)
    try:
        subprocess.run(
            f"codebuddy -p \"prompt\" --model {MODEL_NAME} --permission-mode acceptEdits",
            check=True,
            shell=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"错误：章节 {character} 生成失败（退出码 {e.returncode}），已停止运行。")
        raise
    
    