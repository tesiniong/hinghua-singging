#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
興化語聖經文本解析腳本 v3
完全重寫以處理 lomaci.txt 和 hanci.txt 的不同格式

策略：
1. 分別解析兩個文件
2. lomaci.txt: 每節一行，格式 "章:節 內容"
3. hanci.txt: 多節一行，格式 "節號內容節號內容..."
4. 根據章節號對齊
5. token 級別對齊：1 漢字 = 1 羅馬字音節（「」內的多字 = 1 音節）
"""

import re
import json
from typing import List, Dict, Tuple, Optional
from collections import defaultdict


class BibleTextParserV3:
    """聖經文本解析器 v3"""

    def __init__(self):
        # 羅馬字到漢字的標點符號映射
        self.punct_map = {
            '.': '。',
            ',': '，',
            ';': '；',
            ':': '：',
            '!': '！',
            '?': '？',
            '(': '（',
            ')': '）',
        }

    def parse_lomaci_file(self, filepath: str) -> Dict[Tuple[int, int], Dict]:
        """
        解析羅馬字文件

        返回：{(章, 節): {'text': str, 'syllables': [...]} }
        """
        verses = {}
        current_chapter = 1

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # 檢測書卷標題（通常很短，沒有章節號）
                if not re.search(r'\d+:\d+', line) and len(line) < 50:
                    # 可能是書卷名或章標題，跳過
                    continue

                # 解析 章:節 內容
                match = re.match(r'(\d+):(\d+)\s+(.+)', line)
                if match:
                    chapter = int(match.group(1))
                    verse = int(match.group(2))
                    text = match.group(3).strip()

                    current_chapter = chapter

                    # 分析詞和標點
                    tokens = self._tokenize_lomaci(text)

                    verses[(chapter, verse)] = {
                        'text': text,
                        'tokens': tokens
                    }

        print(f"[OK] lomaci.txt: 解析 {len(verses)} 節經文")
        return verses

    def parse_hanci_file(self, filepath: str) -> Dict[Tuple[int, int], Dict]:
        """
        解析漢字文件

        返回：{(章, 節): {'text': str, 'chars': [...]} }
        """
        # 使用列表保持順序，避免重複節號覆蓋
        verses_list = []

        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                # 檢測書卷標題（第一行或很短的行）
                if not re.search(r'^\d', line):
                    # 可能是書卷名，跳過
                    continue

                # 使用正則表達式找出所有 "數字+內容" 的配對
                # 格式：1內容2內容3內容...
                # 匹配：數字 + 非數字內容（直到下一個數字開頭或結尾）
                verse_pattern = r'(\d+)([^0-9]+?)(?=\d+|$)'
                matches = re.findall(verse_pattern, line)

                for verse_str, verse_text in matches:
                    verse_num = int(verse_str)

                    # 分析漢字和合音字
                    tokens = self._tokenize_hanci(verse_text)

                    verses_list.append({
                        'verse': verse_num,
                        'text': verse_text,
                        'tokens': tokens
                    })

        # 後處理：推斷章號並轉換為 dict
        verses = self._infer_chapters_hanci_from_list(verses_list)

        print(f"[OK] hanci.txt: 解析 {len(verses)} 節經文")
        return verses

    def _infer_chapters_hanci_from_list(self, verses_list: List[Dict]) -> Dict[Tuple[int, int], Dict]:
        """
        從列表推斷漢字文件的章號

        策略：觀察節號的變化，當節號變小或等於前一個節號時，表示新的一章
        （因為節號應該是遞增的）

        輸入：[{'verse': 1, 'text': '...', 'chars': [...]}, ...]
        輸出：{(章, 節): {'text': '...', 'chars': [...]}, ...}
        """
        result = {}
        current_chapter = 1
        last_verse_num = 0

        for verse_data in verses_list:
            verse_num = verse_data['verse']

            # 如果節號變小或相等，表示進入新的一章
            # （正常情況下節號應該遞增：1, 2, 3, ... 當回到 1 或更小時就是新章）
            if verse_num <= last_verse_num:
                current_chapter += 1

            result[(current_chapter, verse_num)] = {
                'text': verse_data['text'],
                'tokens': verse_data['tokens']
            }

            last_verse_num = verse_num

        return result

    def _tokenize_lomaci(self, text: str) -> List[Dict]:
        """
        將羅馬字文本分割為 tokens

        詞的規則：
        - 以空格分隔詞
        - 保留連字號（不拆分），例如："má-láu" 保持完整
        - 包含引號：" " ' ' (U+201C/D, U+2018/9)

        返回：[{'type': 'word'|'punct', 'text': str}, ...]
        """
        tokens = []
        i = 0
        current_word = ''

        while i < len(text):
            char = text[i]

            # 標點符號（包含各種引號）
            # Unicode: U+201C=" U+201D=" U+2018=' U+2019='
            if char in '.,;:!?()\'"…、。，；：！？（）「」\u201C\u201D\u2018\u2019':
                # 保存之前累積的詞（保持完整，不拆分連字號）
                if current_word.strip():
                    tokens.append({
                        'type': 'word',
                        'text': current_word.strip()
                    })
                    current_word = ''

                # 添加標點
                tokens.append({
                    'type': 'punct',
                    'text': char
                })
                i += 1

            # 空格：結束當前詞
            elif char == ' ':
                if current_word.strip():
                    tokens.append({
                        'type': 'word',
                        'text': current_word.strip()
                    })
                    current_word = ''
                i += 1

            # 其他字符：累積到當前詞
            else:
                current_word += char
                i += 1

        # 保存最後的詞
        if current_word.strip():
            tokens.append({
                'type': 'word',
                'text': current_word.strip()
            })

        return tokens

    def _tokenize_hanci(self, text: str) -> List[Dict]:
        """
        將漢字文本分割為 tokens

        返回：[{'type': 'char'|'compound'|'punct', 'text': str, 'chars': [...]}, ...]
        """
        tokens = []
        i = 0

        while i < len(text):
            char = text[i]

            # 合音字開始（「」標記）
            if char == '「':
                end = text.find('」', i)
                if end != -1:
                    compound = text[i+1:end]
                    tokens.append({
                        'type': 'compound',
                        'text': compound,
                        'chars': list(compound)
                    })
                    i = end + 1
                    continue

            # 標點符號（包含中英文標點和各種引號）
            # Unicode: U+201C=" U+201D=" U+2018=' U+2019='
            if char in '。，、；：！？（）「」….,;:!?()\'""\u201C\u201D''\u2018\u2019':
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

    def align_verses(self, lomaci_verses: Dict, hanci_verses: Dict) -> List[Dict]:
        """
        對齊羅馬字和漢字的經節

        返回書卷結構
        """
        # 獲取所有章節號的集合
        all_keys = set(lomaci_verses.keys()) | set(hanci_verses.keys())

        # 按章節號排序
        sorted_keys = sorted(all_keys)

        # 組織成書卷結構（這裡簡化處理，不區分書卷）
        chapters = defaultdict(list)

        for ch, v in sorted_keys:
            lomaci_data = lomaci_verses.get((ch, v))
            hanci_data = hanci_verses.get((ch, v))

            # 對齊 tokens
            if lomaci_data and hanci_data:
                tokens = self._align_tokens(
                    lomaci_data['tokens'],
                    hanci_data['tokens']
                )
            elif lomaci_data:
                # 只有羅馬字
                tokens = [{'type': 'word', 'rom': t['text'], 'han': '', 'form': 'single' if '-' not in t['text'] else 'phrase'}
                          for t in lomaci_data['tokens'] if t['type'] == 'word']
            elif hanci_data:
                # 只有漢字
                tokens = [{'type': 'word', 'han': t['text'], 'rom': '', 'form': 'single' if t['type'] == 'char' else 'compound'}
                          for t in hanci_data['tokens'] if t['type'] in ('char', 'compound')]
            else:
                tokens = []

            verse_data = {
                'verse': v,
                'rom': lomaci_data['text'] if lomaci_data else '',
                'han': hanci_data['text'] if hanci_data else '',
                'tokens': tokens
            }

            chapters[ch].append(verse_data)

        # 轉換成列表格式
        result = []
        for ch in sorted(chapters.keys()):
            result.append({
                'chapter': ch,
                'verses': chapters[ch]
            })

        return result

    def _align_tokens(self, lomaci_tokens: List[Dict], hanci_tokens: List[Dict]) -> List[Dict]:
        """
        對齊羅馬字和漢字的 tokens

        規則：
        - 1 個漢字 = 1 個羅馬字音節
        - 1 個合音字（多個漢字在「」中）= 1 個羅馬字音節
        - 標點以漢字為主
        """
        aligned = []
        l_idx = 0  # lomaci index
        h_idx = 0  # hanci index

        # 提取羅馬字詞（忽略標點，因為兩版本標點不一致）
        lomaci_words = [t for t in lomaci_tokens if t['type'] == 'word']

        while h_idx < len(hanci_tokens):
            h_token = hanci_tokens[h_idx]

            # 標點符號：直接添加（只用漢字版本的標點）
            if h_token['type'] == 'punct':
                aligned.append({
                    'type': 'punct',
                    'han': h_token['text'],
                    'rom': ''
                })
                h_idx += 1
                continue

            # 一般字或合音字
            if l_idx < len(lomaci_words):
                rom_word = lomaci_words[l_idx]['text']

                # 判斷 form
                rom_syllable_count = len(rom_word.split('-'))

                if h_token['type'] == 'compound':
                    # 合音字：多個漢字對應1個羅馬字音節
                    form = 'compound'
                    han_text = h_token['text']
                    h_idx += 1
                elif h_token['type'] == 'char':
                    # 一般字
                    if rom_syllable_count == 1:
                        form = 'single'  # 1音節1字
                        han_text = h_token['text']
                        h_idx += 1
                    else:
                        # 多音節詞：需要收集多個漢字
                        form = 'phrase'
                        chars = [h_token['text']]
                        h_idx += 1

                        # 收集剩餘的漢字（音節數-1個）
                        # 跳過中間的標點
                        collected = 1
                        while collected < rom_syllable_count and h_idx < len(hanci_tokens):
                            if hanci_tokens[h_idx]['type'] == 'char':
                                chars.append(hanci_tokens[h_idx]['text'])
                                collected += 1
                                h_idx += 1
                            elif hanci_tokens[h_idx]['type'] == 'punct':
                                # 跳過標點，不計入詞中
                                h_idx += 1
                            else:
                                break

                        han_text = ''.join(chars)

                aligned.append({
                    'type': 'word',
                    'han': han_text,
                    'rom': rom_word,
                    'form': form
                })

                l_idx += 1
            else:
                # 羅馬字已用完，漢字多出來的
                aligned.append({
                    'type': 'word',
                    'han': h_token['text'],
                    'rom': '',
                    'form': 'single' if h_token['type'] == 'char' else 'compound'
                })
                h_idx += 1

        # 如果羅馬字還有剩餘
        while l_idx < len(lomaci_words):
            rom_word = lomaci_words[l_idx]['text']
            rom_syllable_count = len(rom_word.split('-'))

            aligned.append({
                'type': 'word',
                'han': '',
                'rom': rom_word,
                'form': 'single' if rom_syllable_count == 1 else 'phrase'
            })
            l_idx += 1

        return aligned

    def export_json(self, chapters: List[Dict], output_file: str):
        """匯出為 JSON"""
        # 簡化的書卷結構（單一書卷）
        bible_data = {
            'books': [
                {
                    'name_han': '興化語聖經',
                    'name_rom': 'Hing-hua Bible',
                    'chapters': chapters
                }
            ]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(bible_data, f, ensure_ascii=False, indent=2)

        print(f"\n[OK] 已匯出至 {output_file}")
        print(f"  共 {len(chapters)} 章")

        total_verses = sum(len(ch['verses']) for ch in chapters)
        print(f"  共 {total_verses} 節")


if __name__ == '__main__':
    print("=" * 60)
    print("[PARSING] 興化語聖經文本解析器 v3")
    print("=" * 60)

    parser = BibleTextParserV3()

    # 解析羅馬字文件
    print("\n[1] 解析 lomaci.txt...")
    lomaci_verses = parser.parse_lomaci_file('lomaci.txt')

    # 解析漢字文件
    print("\n[2] 解析 hanci.txt...")
    hanci_verses = parser.parse_hanci_file('hanci.txt')

    # 對齊
    print("\n[3] 對齊經文...")
    chapters = parser.align_verses(lomaci_verses, hanci_verses)

    # 匯出
    print("\n[4] 匯出 JSON...")
    parser.export_json(chapters, 'bible_data.json')

    print("\n[DONE] 完成！")
