#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
興化語聖經文本解析腳本 v2
根據最新需求更新：
1. 標點符號處理：Ruby 版以漢字標點為主，移除羅馬字標點（保留連字號）
2. 引號處理：Ruby 版不顯示引號
3. 版本差異：如果某一邊內容缺失，留空
4. 排版：雙欄版一節一行，Ruby 版同章連續
"""

import re
import json
from typing import List, Dict, Tuple, Optional

class BibleTextParser:
    """聖經文本解析器"""

    def __init__(self):
        # 標點符號映射（羅馬字 → 漢字）
        self.punct_map = {
            '.': '。',
            ',': '，',
            ';': '；',
            ':': '：',
            '!': '！',
            '?': '？',
            '(': '（',
            ')': '）',
            '"': '「',
            '"': '」',
        }

    def parse_line_number(self, line: str) -> Tuple[Optional[int], str]:
        """
        解析行號格式：數字→內容
        返回：(行號, 內容)
        """
        match = re.match(r'\s*(\d+)→(.+)', line)
        if match:
            return int(match.group(1)), match.group(2).strip()
        return None, line.strip()

    def parse_verse_ref(self, text: str) -> Tuple[Optional[int], Optional[int], str]:
        """
        解析章節引用：1:1 內容
        返回：(章, 節, 內容)
        """
        match = re.match(r'(\d+):(\d+)\s+(.*)', text)
        if match:
            return int(match.group(1)), int(match.group(2)), match.group(3)
        return None, None, text

    def tokenize_hanci(self, text: str) -> List[Dict]:
        """
        分詞漢字文本
        處理合音字（「」標記）
        保留刻意換行
        """
        tokens = []
        lines = text.split('\n')

        for line_idx, line in enumerate(lines):
            if line_idx > 0:
                # 不是第一行，添加換行標記
                tokens.append({'type': 'newline'})

            i = 0
            while i < len(line):
                char = line[i]

                # 合音字開始
                if char == '「':
                    end = line.find('」', i)
                    if end != -1:
                        compound = line[i+1:end]
                        tokens.append({
                            'type': 'compound',
                            'text': compound,
                            'chars': list(compound)
                        })
                        i = end + 1
                        continue

                # 標點符號
                if char in '。，、；：！？（）「」…':
                    tokens.append({
                        'type': 'punct',
                        'text': char
                    })
                    i += 1
                    continue

                # 空白
                if char.strip() == '':
                    i += 1
                    continue

                # 一般漢字
                tokens.append({
                    'type': 'char',
                    'text': char
                })
                i += 1

        return tokens

    def tokenize_lomaci(self, text: str) -> List[Dict]:
        """
        分詞羅馬字文本
        以空格、連字號作為音節分隔
        識別標點符號
        """
        tokens = []
        lines = text.split('\n')

        for line_idx, line in enumerate(lines):
            if line_idx > 0:
                tokens.append({'type': 'newline'})

            # 正則表達式：匹配音節和標點
            # 音節：連續的字母和特殊符號（如 ̤、̍、̄ 等）
            pattern = r'([a-zA-ZĀāÁáǍǎÀàĒēÉéĚěÈèĪīÍíǏǐÌìŌōÓóǑǒÒòŪūÚúǓǔÙùⁿ̤̍̄̆̂̃]+(?:-[a-zA-ZĀāÁáǍǎÀàĒēÉéĚěÈèĪīÍíǏǐÌìŌōÓóǑǒÒòŪūÚúǓǔÙùⁿ̤̍̄̆̂̃]+)*)|([.,;:!?()"\'…])'

            for match in re.finditer(pattern, line):
                text = match.group(0)

                # 判斷是音節還是標點
                if re.match(r'[a-zA-Z]', text):
                    tokens.append({
                        'type': 'syllable',
                        'text': text
                    })
                else:
                    tokens.append({
                        'type': 'punct',
                        'text': text
                    })

        return tokens

    def align_tokens(self, hanci_tokens: List[Dict], lomaci_tokens: List[Dict]) -> List[Dict]:
        """
        對齊漢字和羅馬字 tokens

        規則：
        1. 一般字：一個漢字 ↔ 一個羅馬字音節
        2. 合音字：多個漢字（在「」內）↔ 一個羅馬字音節
        3. 標點：以漢字標點為主
        4. 換行：保留
        """
        aligned = []
        h_idx = 0
        l_idx = 0

        while h_idx < len(hanci_tokens):
            h_token = hanci_tokens[h_idx]

            # 換行
            if h_token['type'] == 'newline':
                aligned.append({'type': 'newline'})
                h_idx += 1
                # 同步羅馬字的換行
                if l_idx < len(lomaci_tokens) and lomaci_tokens[l_idx]['type'] == 'newline':
                    l_idx += 1
                continue

            # 標點符號：以漢字為主
            if h_token['type'] == 'punct':
                aligned.append({
                    'type': 'punct',
                    'hanci': h_token['text']
                })
                h_idx += 1
                # 跳過對應的羅馬字標點
                if l_idx < len(lomaci_tokens) and lomaci_tokens[l_idx]['type'] == 'punct':
                    l_idx += 1
                continue

            # 合音字
            if h_token['type'] == 'compound':
                if l_idx < len(lomaci_tokens) and lomaci_tokens[l_idx]['type'] == 'syllable':
                    aligned.append({
                        'type': 'word',
                        'hanci': h_token['text'],
                        'lomaci': lomaci_tokens[l_idx]['text'],
                        'is_compound': True
                    })
                    h_idx += 1
                    l_idx += 1
                else:
                    # 羅馬字缺失
                    aligned.append({
                        'type': 'word',
                        'hanci': h_token['text'],
                        'lomaci': '',
                        'is_compound': True
                    })
                    h_idx += 1
                continue

            # 一般字
            if h_token['type'] == 'char':
                if l_idx < len(lomaci_tokens) and lomaci_tokens[l_idx]['type'] == 'syllable':
                    aligned.append({
                        'type': 'word',
                        'hanci': h_token['text'],
                        'lomaci': lomaci_tokens[l_idx]['text'],
                        'is_compound': False
                    })
                    h_idx += 1
                    l_idx += 1
                else:
                    # 羅馬字缺失
                    aligned.append({
                        'type': 'word',
                        'hanci': h_token['text'],
                        'lomaci': '',
                        'is_compound': False
                    })
                    h_idx += 1
                continue

            h_idx += 1

        return aligned

    def detect_structure(self, line: str) -> str:
        """
        識別文本結構：書卷名、章標題、小節標題、經文

        簡單規則：
        - 如果以數字:數字開頭 → 經文
        - 如果很短（<10字）且不是經文 → 可能是標題
        - 否則 → 段落文字
        """
        # 經文
        if re.match(r'^\d+:\d+', line):
            return 'verse'

        # 短文本可能是標題
        if len(line) < 15 and not re.search(r'[。，]', line):
            return 'heading'

        return 'paragraph'

    def parse_files(self, hanci_file: str, lomaci_file: str) -> Dict:
        """
        解析漢字和羅馬字文件
        """
        with open(hanci_file, 'r', encoding='utf-8') as hf:
            hanci_lines = hf.readlines()

        with open(lomaci_file, 'r', encoding='utf-8') as lf:
            lomaci_lines = lf.readlines()

        bible = {
            'books': []
        }

        current_book = None
        current_chapter = None

        for h_line, l_line in zip(hanci_lines, lomaci_lines):
            # 解析行號
            _, h_content = self.parse_line_number(h_line)
            _, l_content = self.parse_line_number(l_line)

            if not h_content:
                continue

            # 識別結構
            structure = self.detect_structure(h_content)

            if structure == 'verse':
                # 解析經文
                chapter, verse, h_text = self.parse_verse_ref(h_content)
                _, _, l_text = self.parse_verse_ref(l_content)

                if chapter and verse:
                    # 檢查是否需要新的章
                    if current_chapter is None or current_chapter['chapter'] != chapter:
                        current_chapter = {
                            'chapter': chapter,
                            'verses': []
                        }
                        if current_book:
                            current_book['chapters'].append(current_chapter)

                    # 分詞和對齊
                    hanci_tokens = self.tokenize_hanci(h_text)
                    lomaci_tokens = self.tokenize_lomaci(l_text)
                    aligned = self.align_tokens(hanci_tokens, lomaci_tokens)

                    verse_data = {
                        'verse': verse,
                        'hanci': h_text,
                        'lomaci': l_text,
                        'tokens': aligned,
                        'has_linebreak': '\n' in h_text  # 標記是否有刻意換行
                    }

                    if current_chapter:
                        current_chapter['verses'].append(verse_data)

            elif structure == 'heading':
                # 標題（可能是書卷名或小節標題）
                if current_book is None or len(h_content) < 10:
                    # 新書卷
                    current_book = {
                        'name_hanci': h_content,
                        'name_lomaci': l_content,
                        'chapters': []
                    }
                    bible['books'].append(current_book)
                    current_chapter = None
                else:
                    # 小節標題
                    if current_chapter:
                        current_chapter['heading'] = {
                            'hanci': h_content,
                            'lomaci': l_content
                        }

        return bible

    def export_json(self, bible_data: Dict, output_file: str):
        """匯出為 JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(bible_data, f, ensure_ascii=False, indent=2)

        print(f"[OK] 已匯出至 {output_file}")
        print(f"  共 {len(bible_data['books'])} 卷")


if __name__ == '__main__':
    parser = BibleTextParser()

    bible_data = parser.parse_files('hanci.txt', 'lomaci.txt')
    parser.export_json(bible_data, 'bible_data.json')

    # 輸出統計資訊
    total_verses = sum(
        len(chapter['verses'])
        for book in bible_data['books']
        for chapter in book['chapters']
    )
    print(f"  共 {total_verses} 節經文")
