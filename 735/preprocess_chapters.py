#!/usr/bin/env python3
"""Parse pre-extracted chapters and save to individual files for parallel summaries."""
import os, re

chapters_file = "/tmp/chapters_extracted.md"
output_dir = "/Users/hikari/Documents/books/735/剧情概要"
os.makedirs(output_dir, exist_ok=True)

with open(chapters_file, 'r', encoding='utf-8') as f:
    content = f.read()

sections = content.split('=====================================================')

chapter_num = 0
for si in range(1, len(sections)):
    section = sections[si]
    if not section.strip():
        continue
    
    # Extract filename from 【xxx】 marker
    fname_match = re.search(r'【(.+?)】', section)
    if not fname_match:
        chapter_num += 1
        continue
    fname = fname_match.group(1)
    
    parts_split = fname.split('_')
    try:
        ch_num = int(parts_split[0])
    except (ValueError, IndexError):
        ch_num = chapter_num
    
    lines = section.strip().split('\n')
    
    # Collect meaningful content lines after the 【...】 line
    text_lines = []
    for line in lines:
        if '【' not in line and li > 0 and '】' not in line:
            pass
        
    # Skip empty lines right after title
    start_idx = None
    for li, line in enumerate(lines):
        if '【在' in line:
            continue
    
    # Better approach: after the 【文件名】 line, skip blank/title lines
    found_title = False
    text_lines = []
    for line in lines:
        if not found_title:
            if '【' in line and '】' in line:
                found_title = True
                continue
            continue
        
        # Collect non-blank, non-separator lines
        stripped = line.strip()
        if line.startswith('========') or line.startswith('-'):
            continue
        
        text_lines.append(line)
    
    ch_text = '\n'.join(text_lines).strip()
    if len(ch_text) < 5:
        chapter_num += 1
        continue
    
    fname_out, _ext = os.path.splitext(fname.replace('/', '_').replace('\\', '_'))
    filepath = os.path.join(output_dir, f"{fname_out}.txt")
    with open(filepath, 'w', encoding='utf-8') as out:
        out.write(ch_text + '\n\n')
    
    chapter_num += 1

total_files = len([f for f in os.listdir(output_dir) if f.endswith('.txt')])
print(f"Written {chapter_num} chapters. Total .txt files in output dir: {total_files}")
