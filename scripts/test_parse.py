#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""測試解析器"""

import re

# 測試 hanci.txt 解析
print("=" * 60)
print("Testing hanci.txt parsing")
print("=" * 60)

with open('hanci.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

total_verses = 0
for line_num, line in enumerate(lines, 1):
    line = line.strip()
    if not line:
        continue

    # 檢測是否為標題行（不以數字開頭）
    if not re.search(r'^\d', line):
        print(f"Line {line_num}: [TITLE]")
        continue

    # 找出所有經節
    verse_pattern = r'(\d+)([^0-9]+?)(?=\d+|$)'
    matches = re.findall(verse_pattern, line)

    if matches:
        total_verses += len(matches)
        print(f"Line {line_num}: {len(matches)} verses")

print(f"\nTotal verses parsed: {total_verses}")

# Test lomaci.txt parsing
print("\n" + "=" * 60)
print("Testing lomaci.txt parsing")
print("=" * 60)

with open('lomaci.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

total_verses = 0
for line_num, line in enumerate(lines[:20], 1):
    line = line.strip()
    if not line:
        continue

    match = re.match(r'(\d+):(\d+)\s+(.+)', line)
    if match:
        total_verses += 1
        chapter, verse, text = match.groups()
        print(f"Line {line_num}: {chapter}:{verse}")
    else:
        print(f"Line {line_num}: [NO MATCH]")

print(f"\nTotal verses in first 20 lines: {total_verses}")
