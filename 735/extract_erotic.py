#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从分章文件夹中提取性交细节片段
"""
import os
import re

# 分章目录和输出目录
CHAPTERS_DIR = "/Users/hikari/Documents/books/735/分章"
OUTPUT_DIR = "/Users/hikari/Documents/books/735/色情细节描述"

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 判断是否是性交细节的关键字
EROTIC_KEYWORDS = [
    r'酥胸', r'玉峰', r'酥乳', r'雪乳', r'花径', r'花苞', r'阴精', 
    r'巨棒', r'肉茎', r'阳根', r'交欢', r'颠鸾倒凤', r'云雨', 
    r'双修', r'采补', r'娇啼', r'花底', r'腿心', r'嫩瓤', 
    r'蜜液', r'阴唇', r'花蕊', r'玉户', r'香津', r'春水',
    r'挺刺', r'抽送', r'耸杵', r'贯穿', r'陷没', r'窄嫩',
    r'肥硕酥峰', r'葱绿束胸', r'俏乳', r'蛮腰', r'粉股',
    r'如棉粉股', r'花径', r'娇嫩的花径', r'窄紧如花苞',
]

# 判断是否有明显的性交描写
def has_erotic_context(lines):
    """检查段落是否有性交上下文"""
    erotic_count = 0
    for line in lines:
        for keyword in EROTIC_KEYWORDS:
            if re.search(keyword, line):
                erotic_count += 1
                break
    return erotic_count >= 3  # 至少出现3次相关关键词才认为是性交细节

def extract_erotic_passages(filepath, filename):
    """提取文件中的性交细节片段"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    passages = []
    current_passage = []
    in_erotic_section = False
    
    # 识别段落边界（空行或缩进）
    paragraph_lines = []
    all_paragraphs = []
    
    for line in lines:
        if line.strip() == '':
            if paragraph_lines:
                all_paragraphs.append(paragraph_lines)
                paragraph_lines = []
        else:
            paragraph_lines.append(line)
    
    if paragraph_lines:
        all_paragraphs.append(paragraph_lines)
    
    # 查找连续的性交细节段落
    i = 0
    while i < len(all_paragraphs):
        para = all_paragraphs[i]
        para_text = '\n'.join(para)
        
        # 检查是否包含性交关键词
        is_erotic = False
        for keyword in EROTIC_KEYWORDS:
            if re.search(keyword, para_text):
                is_erotic = True
                break
        
        # 如果找到一段,向前后扩展获取完整上下文
        if is_erotic:
            start = max(0, i - 1)
            end = min(len(all_paragraphs), i + 2)
            
            passage_lines = []
            for j in range(start, end):
                passage_lines.extend(all_paragraphs[j])
                if j == end - 1:
                    break
            
            # 检查扩展后的段落是否足够
            extended_text = '\n'.join(passage_lines)
            if has_erotic_context(passage_lines):
                passages.append(extended_text.strip())
                i = end + 1  # 跳过已处理的段落
                continue
        
        i += 1
    
    return passages

def main():
    results = {
        'total': 0,
        'with_content': [],
        'without_content': []
    }
    
    # 获取所有txt文件并按编号排序
    files = [f for f in os.listdir(CHAPTERS_DIR) if f.endswith('.txt')]
    files.sort()
    
    print(f"共找到 {len(files)} 个分章文件")
    
    for filename in files:
        filepath = os.path.join(CHAPTERS_DIR, filename)
        results['total'] += 1
        
        # 从文件名提取章节号
        chapter_num = filename.split('_')[0]
        chapter_name = filename.replace('.txt', '').split('_', 1)[1] if '_' in filename else 'unknown'
        
        passages = extract_erotic_passages(filepath, filename)
        
        if passages:
            results['with_content'].append({
                'chapter': f"{chapter_num}_{chapter_name}",
                'passages_count': len(passages)
            })
            
            # 保存提取的内容
            output_filename = f"{chapter_num}_{chapter_name}.txt"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as out_f:
                out_f.write(f"【章节：{chapter_num}_{chapter_name}】\n\n")
                for idx, passage in enumerate(passages, 1):
                    out_f.write(f"--- 片段 {idx} ---\n")
                    out_f.write(passage + "\n\n")
            
            print(f"[{chapter_num}] {chapter_name}: 提取了 {len(passages)} 个片段")
        else:
            results['without_content'].append(f"{chapter_num}_{chapter_name}")
    
    # 生成汇总报告
    summary_path = os.path.join(OUTPUT_DIR, "_提取汇总.md")
    with open(summary_path, 'w', encoding='utf-8') as sum_f:
        sum_f.write("# 性交细节提取汇总\n\n")
        sum_f.write(f"- **处理章节总数**: {results['total']}\n")
        sum_f.write(f"- **有内容的章节数**: {len(results['with_content'])}\n")
        sum_f.write(f"- **无内容的章节数**: {len(results['without_content'])}\n\n")
        
        sum_f.write("## 有内容的章节列表\n\n")
        for item in results['with_content']:
            sum_f.write(f"- {item['chapter']}: {item['passages_count']}个片段\n")
        
        sum_f.write("\n## 无内容的章节列表\n\n")
        for chapter in results['without_content']:
            sum_f.write(f"- {chapter}\n")
    
    print(f"\n提取完成!")
    print(f"总章节数: {results['total']}")
    print(f"有内容: {len(results['with_content'])}")
    print(f"无内容: {len(results['without_content'])}")
    print(f"汇总报告已保存至: {summary_path}")

if __name__ == '__main__':
    main()
