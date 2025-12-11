#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
格式化漢字版聖經文本
將節號統一格式化為：每節一行，節號後加空格
保留標題、段落小標、詩歌體換行
"""

import re
import sys

def is_verse_number(text, pos):
    """
    檢查指定位置是否是節號
    節號特徵：數字後直接接漢字（沒有空格、沒有標點）
    """
    # 提取從 pos 開始的數字
    match = re.match(r'(\d+)', text[pos:])
    if not match:
        return None, None

    num = match.group(1)
    end_pos = pos + len(num)

    # 檢查數字後面是什麼
    if end_pos >= len(text):
        return None, None

    next_char = text[end_pos]

    # 如果是空格，可能已經格式化過了，跳過
    if next_char == ' ':
        # 檢查空格後是否是漢字
        if end_pos + 1 < len(text) and is_chinese(text[end_pos + 1]):
            return num, end_pos  # 這是已格式化的節號
        return None, None

    # 如果直接接漢字，這是節號
    if is_chinese(next_char):
        return num, end_pos

    return None, None


def is_chinese(char):
    """檢查是否是漢字"""
    return '\u4e00' <= char <= '\u9fff'


def format_hanci_text(input_file, output_file):
    """
    格式化漢字版文本
    - 保留所有標題行（#, ##, ###）和空行
    - 在節號前換行，節號後加空格
    - 保留詩歌體/引文的換行
    """

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    result = []
    current_verse = []  # 累積當前節的內容

    def flush_verse():
        """輸出當前累積的節"""
        if current_verse:
            result.append(''.join(current_verse))
            current_verse.clear()

    for line in lines:
        line = line.rstrip('\n')

        # 1. 標題行：直接輸出
        if line.startswith('#'):
            flush_verse()
            result.append(line)
            continue

        # 2. 空行：直接輸出
        if not line.strip():
            flush_verse()
            result.append(line)
            continue

        # 3. 非數字開頭的行：續行（詩歌體/引文）
        if not re.match(r'^\d', line):
            if current_verse:
                current_verse.append('\n' + line)
            else:
                # 孤立的續行（不應該發生，但保留）
                result.append(line)
            continue

        # 4. 處理包含節號的行
        # 掃描整行，找到所有節號位置
        i = 0
        segments = []  # [(verse_num, content), ...]

        while i < len(line):
            # 檢查當前位置是否是節號
            verse_num, end_pos = is_verse_number(line, i)

            if verse_num:
                # 找到節號
                # 找到這一節的內容（到下一個節號或行尾）
                content_start = end_pos
                if content_start < len(line) and line[content_start] == ' ':
                    content_start += 1  # 跳過已有的空格

                # 找下一個節號
                next_verse_pos = None
                j = content_start
                while j < len(line):
                    if line[j].isdigit():
                        test_num, test_end = is_verse_number(line, j)
                        if test_num:
                            next_verse_pos = j
                            break
                    j += 1

                if next_verse_pos:
                    content = line[content_start:next_verse_pos]
                else:
                    content = line[content_start:]

                segments.append((verse_num, content))
                i = next_verse_pos if next_verse_pos else len(line)
            else:
                i += 1

        # 輸出分段
        for idx, (verse_num, content) in enumerate(segments):
            if idx == 0:
                # 第一個節：可能接續上一節
                if current_verse:
                    # 輸出上一節
                    flush_verse()
                # 開始新節
                current_verse.append(f'{verse_num} {content}')
            else:
                # 後續節：先輸出前一節
                flush_verse()
                current_verse.append(f'{verse_num} {content}')

    # 輸出最後一節
    flush_verse()

    # 寫入輸出
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))

    print(f"格式化完成")
    print(f"  輸入: {input_file}")
    print(f"  輸出: {output_file}")
    print(f"  總行數: {len(result)}")


def main():
    input_file = 'hanci.txt'
    output_file = 'hanci_formatted.txt'

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    format_hanci_text(input_file, output_file)


if __name__ == '__main__':
    main()
