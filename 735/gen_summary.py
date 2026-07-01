#!/usr/bin/env python3
"""批量读取分章文件，为每章生成剧情梗概"""
import os, glob

chapters_dir = "/Users/hikari/Documents/books/735/分章"
output_dir = "/Users/hikari/Documents/books/735/剧情概要"
os.makedirs(output_dir, exist_ok=True)

# 获取所有章节文件，按文件名排序（001, 002...）
files = sorted(glob.glob(os.path.join(chapters_dir, "*.txt")))
print(f"共发现 {len(files)} 个章节文件")

for i, filepath in enumerate(files):
    filename = os.path.basename(filepath)
    print(f"[{i+1}/{len(files)}] 读取: {filename}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取章节号（从文件名或内容）
    chapter_num = filename.split('_')[0] if '_' in filename else "???"
    
    with open(os.path.join(output_dir, "chapters_A.txt"), 'a', encoding='utf-8') as out:
        out.write(f"== {filename} ==\n")
        # 写入前5行作为预览，后面用...代替
        lines = content.split('\n')[:200]  # limit to first 200 lines per file
        for line in lines:
            out.write(line + '\n')
        if len(content.split('\n')) > 200:
            out.write("...\n[内容已截断，共 " + str(len(lines)) + " 行]\n")
        out.write("\n---\n\n")

print(f"\done! 输出到 {output_dir}/chapters_A.txt")
