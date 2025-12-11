#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
興化語聖經文本解析腳本
用於將 TXT 文字檔轉換為結構化的 JSON 格式
"""

import re
import json
from typing import List, Dict, Tuple

def parse_verse_reference(line: str) -> Tuple[str, str, str]:
    """
    解析經文引用格式
    例如：1:1 → (章, 節, 內容)
    """
    # 匹配章節格式：數字:數字 內容
    match = re.match(r'(\d+):(\d+)\s+(.*)', line)
    if match:
        chapter = match.group(1)
        verse = match.group(2)
        content = match.group(3)
        return chapter, verse, content
    return None, None, line

def tokenize_hanci(text: str) -> List[Dict]:
    """
    將漢字文本分詞
    處理合音字（用「」標記）

    例如：「第一」 → 一個 token
    """
    tokens = []
    i = 0
    while i < len(text):
        # 檢查是否是合音字開始
        if text[i] == '「':
            # 找到配對的結束引號
            end = text.find('」', i)
            if end != -1:
                # 提取合音字
                compound = text[i+1:end]
                tokens.append({
                    'text': compound,
                    'type': 'compound',  # 合音字
                    'char_count': len(compound)
                })
                i = end + 1
                continue

        # 一般字符
        char = text[i]
        if char.strip():  # 忽略空白
            tokens.append({
                'text': char,
                'type': 'normal',
                'char_count': 1
            })
        i += 1

    return tokens

def tokenize_lomaci(text: str) -> List[str]:
    """
    將羅馬字文本分為音節
    以空格和 hyphen 作為分隔
    """
    # 先移除標點符號兩側的空白
    # 然後按空格和 hyphen 分割
    tokens = []

    # 使用正則表達式分割，保留標點
    parts = re.split(r'([\s\-,.:;!?，。：；！？、])', text)

    for part in parts:
        part = part.strip()
        if part and part not in ['-', ' ']:
            tokens.append(part)

    return tokens

def align_tokens(hanci_tokens: List[Dict], lomaci_tokens: List[str]) -> List[Dict]:
    """
    對齊漢字和羅馬字 tokens
    基本原則：一個漢字對應一個羅馬字音節
    例外：合音字（多個漢字）對應一個音節
    """
    aligned = []
    h_idx = 0
    l_idx = 0

    while h_idx < len(hanci_tokens) and l_idx < len(lomaci_tokens):
        h_token = hanci_tokens[h_idx]
        l_token = lomaci_tokens[l_idx]

        if h_token['type'] == 'compound':
            # 合音字：多個漢字對應一個羅馬字音節
            aligned.append({
                'hanci': h_token['text'],
                'lomaci': l_token,
                'is_compound': True
            })
            h_idx += 1
            l_idx += 1
        else:
            # 一般字：一對一對應
            aligned.append({
                'hanci': h_token['text'],
                'lomaci': l_token,
                'is_compound': False
            })
            h_idx += 1
            l_idx += 1

    return aligned

def parse_bible_text(hanci_file: str, lomaci_file: str, output_file: str):
    """
    解析聖經文本並生成 JSON
    """
    bible_data = {
        'books': []
    }

    current_book = None
    current_chapter = None

    with open(hanci_file, 'r', encoding='utf-8') as hf, \
         open(lomaci_file, 'r', encoding='utf-8') as lf:

        hanci_lines = hf.readlines()
        lomaci_lines = lf.readlines()

        for h_line, l_line in zip(hanci_lines, lomaci_lines):
            # 移除行號前綴（格式：數字→內容）
            h_content = h_line.split('→', 1)[-1].strip() if '→' in h_line else h_line.strip()
            l_content = l_line.split('→', 1)[-1].strip() if '→' in l_line else l_line.strip()

            if not h_content or not l_content:
                continue

            # 檢查是否是書卷名稱（通常沒有章節號）
            if not re.match(r'^\d+:', h_content):
                # 可能是書卷名稱或小標題
                if current_book is None or len(h_content) < 20:
                    # 新書卷
                    current_book = {
                        'name_hanci': h_content,
                        'name_lomaci': l_content,
                        'chapters': []
                    }
                    bible_data['books'].append(current_book)
                    current_chapter = None
                continue

            # 解析章節引用
            chapter, verse, h_text = parse_verse_reference(h_content)
            _, _, l_text = parse_verse_reference(l_content)

            if chapter and verse:
                # 檢查是否需要新增章
                if current_chapter is None or current_chapter['chapter'] != int(chapter):
                    current_chapter = {
                        'chapter': int(chapter),
                        'verses': []
                    }
                    if current_book:
                        current_book['chapters'].append(current_chapter)

                # 分詞和對齊
                hanci_tokens = tokenize_hanci(h_text)
                lomaci_tokens = tokenize_lomaci(l_text)
                aligned_tokens = align_tokens(hanci_tokens, lomaci_tokens)

                # 添加經節
                verse_data = {
                    'verse': int(verse),
                    'hanci': h_text,
                    'lomaci': l_text,
                    'tokens': aligned_tokens
                }

                if current_chapter:
                    current_chapter['verses'].append(verse_data)

    # 寫入 JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(bible_data, f, ensure_ascii=False, indent=2)

    print(f"解析完成！輸出至 {output_file}")
    print(f"共 {len(bible_data['books'])} 卷")

if __name__ == '__main__':
    parse_bible_text(
        'hanci.txt',
        'lomaci.txt',
        'bible_data.json'
    )
