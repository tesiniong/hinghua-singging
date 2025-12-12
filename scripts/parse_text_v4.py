#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析興化語聖經文本（第四版）
支援新的格式化文本：每節一行，有標題和段落標題
"""

# 【舊約 39 卷】
old_testament_books = [
    ("Cho̤̍ng-sa̤-gi̍", "創世記", "Genesis", 9),
    ("Cheoh-Ai-gi̍h", "出伊及", "Exodus", 72),
    ("Lī-bī Gi̍", "利未記", "Leviticus", 124),
    ("Míng-so̍ Gi̍", "民數記", "Numbers", 161),
    ("Sing-mīng Gi̍", "申命記", "Deuteronomy", 214),
    ("Io̤h-sṳ-a̍ Cṳ", "約書亞書", "Joshua", 262),
    ("Seō-seo Gi̍", "士師記", "Judges", 294),
    ("Lō-deh Gi̍", "路得記", "Ruth", 327),
    ("Sah-bâ̤u-cî Céng-cṳ", "撒母耳前書", "1 Samuel", 332),
    ("Sah-bâ̤u-cî Hā̤u-cṳ", "撒母耳後書", "2 Samuel", 375),
    ("Le̍h-ó̤ng Siō̤ng-ge̤̍ng", "列王上卷", "1 Kings", 412),
    ("Le̍h-ó̤ng Hā-ge̤̍ng", "列王下卷", "2 Kings", 454),
    ("Le̍h-dāi Siō̤ng-ge̤̍ng", "歷代上卷", "1 Chronicles", 494),
    ("Le̍h-dāi Hā-ge̤̍ng", "歷代下卷", "2 Chronicles", 534),
    ("Î-seō-la̍h Cṳ", "以斯拉書", "Ezra", 580),
    ("Ní-hi-bî Gi̍", "尼希米記", "Nehemiah", 593),
    ("Î-seō-tiah Cṳ", "以斯帖書", "Esther", 612),
    ("Io̤h-beh Gi̍", "約伯記", "Job", 622),
    ("Si-peng", "詩篇", "Psalms", 669),
    ("Cing-ngé̤ng", "箴言", "Proverbs", 786),
    ("Dé̤ng-dō̤ Cṳ", "傳道書", "Ecclesiastes", 826),
    ("Sê̤-ló̤-meóng Ē Ngâ-go̤", "所羅門兮雅歌", "Song of Solomon", 837),
    ("Î-se̤̍-a̍ Cṳ", "以賽亞書", "Isaiah", 845),
    ("Á̤-lī-bî Cṳ", "耶利米書", "Jeremiah", 914),
    ("Á̤-lī-bî Ai-go̤ Cṳ", "耶利米哀歌書", "Lamentations", 989),
    ("Î-sa̤-geh Cṳ", "以西結書", "Ezekiel", 998),
    ("Dāng-î-lî Cṳ", "但以理書", "Daniel", 1063),
    ("Hó̤-sa̤ Cṳ", "何西書", "Hosea", 1083),
    ("Io̤h-cî Cṳ", "約珥書", "Joel", 1094),
    ("A̍-mó̤-seo Cṳ", "亞摩斯書", "Amos", 1098),
    ("O̤-ba-dâ̤ Cṳ", "阿巴底書", "Obadiah", 1107),
    ("Io̤h-ná Cṳ", "約拿書", "Jonah", 1109),
    ("Bî-gia Cṳ", "彌迦書", "Micah", 1112),
    ("Ná-o̤ng Cṳ", "那翁書", "Nahum", 1119),
    ("Ha̍h-ba-go̤h Cṳ", "哈巴谷書", "Habakkuk", 1122),
    ("Sa̤-huang-ngâ Cṳ", "西番雅書", "Zephaniah", 1126),
    ("Ha̍h-gi Cṳ", "哈基書", "Haggai", 1130),
    ("Sah-ga-lī-a̍ Cṳ", "撒迦利亞書", "Zechariah", 1133),
    ("Mâ-la̍h-gi Cṳ", "瑪拉基書", "Malachi", 1145)
]

# 【新約 27 卷】
new_testament_books = [
    ("Mâ-ta̍i", "馬太", "Gospel of Matthew", 1153),
    ("Mâ-kô̤", "馬可", "Gospel of Mark", 1193),
    ("Lō-ga", "路加", "Gospel of Luke", 1218),
    ("Io̤h-hāng", "約翰", "Gospel of John", 1261),
    ("Seo̍-dó Hēng-dē̤ng", "使徒行傳", "Acts of the Apostles", 1294),
    ("Bô̤-ló̤ Gio̤̍ Ló̤-mâ Náng Cṳ", "保羅寄羅馬儂書", "Romans", 1336),
    ("Bô̤-ló̤ Gio̤̍ Go̤-líng-do̤ Céng-cṳ", "保羅寄哥林多前書", "1 Corinthians", 1355),
    ("Bô̤-ló̤ Gio̤̍ Go̤-líng-do̤ Hā̤u-cṳ", "保羅寄哥林多後書", "2 Corinthians", 1374),
    ("Bô̤-ló̤ Gio̤̍ Ga-la̍h-ta̍i Cṳ", "保羅寄加拉太書", "Galatians", 1386),
    ("Bô̤-ló̤ Gio̤̍ Î-heo̍h-sê̤ Cṳ", "保羅寄以弗所書", "Ephesians", 1392),
    ("Bô̤-ló̤ Gio̤̍ Hi-li̍h-bî Náng Cṳ", "保羅寄腓立比儂書", "Philippians", 1398),
    ("Bô̤-ló̤ Gio̤̍ Go̤-ló̤-sa̤ Náng Cṳ", "保羅寄歌羅西儂書", "Colossians", 1403),
    ("Bô̤-ló̤ Gio̤̍ Tiah-sah-ló̤-ní-gia Náng Céng-cṳ", "保羅寄帖撒羅尼迦儂前書", "1 Thessalonians", 1408),
    ("Bô̤-ló̤ Gio̤̍ Tiah-sah-ló̤-ní-gia Náng Hā̤u-cṳ", "保羅寄帖撒羅尼迦儂後書", "2 Thessalonians", 1412),
    ("Bô̤-ló̤ Gio̤̍ Dá̤-mó̤-ta̍i Céng-cṳ", "保羅寄提摩太前書", "1 Timothy", 1415),
    ("Bô̤-ló̤ Gio̤̍ Dá̤-mó̤-ta̍i Hā̤u-cṳ", "保羅寄提摩太後書", "2 Timothy", 1420),
    ("Bô̤-ló̤ Gio̤̍ Dá̤-do̤ Cṳ", "保羅寄提多書", "Titus", 1424),
    ("Bô̤-ló̤ Gio̤̍ Hi-lī-meóng Cṳ", "保羅寄腓利門書", "Philemon", 1427),
    ("Hi-beh-lái Náng Cṳ", "希伯來儂書", "Hebrews", 1428),
    ("Seo̍-dó Ngâ-go̤h Cṳ", "使徒雅各書", "James", 1442),
    ("Bî-deh Céng-cṳ", "彼得前書", "1 Peter", 1447),
    ("Bî-deh Hā̤u-cṳ", "彼得後書", "2 Peter", 1453),
    ("Io̤h-hāng Ih Cṳ", "約翰一書", "1 John", 1456),
    ("Io̤h-hāng Cī Cṳ", "約翰二書", "2 John", 1461),
    ("Iók-hâng So̤ⁿ Cṳ", "約翰三書", "3 John", 1462),
    ("Seo̍-dó Iú-dāi Cṳ", "使徒猶大書", "Jude", 1463),
    ("Seo̍-dó Io̤h-hāng Be̍h-sī-le̤̍h", "使徒約翰默示錄", "Revelation", 1465)
]

import re
import json
import sys
import shutil
from pathlib import Path

# 創建書名映射字典
ALL_BOOKS = old_testament_books + new_testament_books
ROM_TO_HAN = {rom: han for rom, han, eng, page in ALL_BOOKS}
HAN_TO_ROM = {han: rom for rom, han, eng, page in ALL_BOOKS}
HAN_TO_ENG = {han: eng for rom, han, eng, page in ALL_BOOKS}

def number_to_chinese(n):
    """阿拉伯數字轉漢字"""
    if n == 0:
        return '零'

    digits = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九']

    if n < 10:
        return digits[n]
    elif n < 20:
        return '十' + (digits[n-10] if n > 10 else '')
    elif n < 100:
        tens = digits[n // 10]
        ones = digits[n % 10]
        return tens + '十' + (ones if ones else '')
    elif n < 1000:
        hundreds = digits[n // 100]
        remainder = n % 100
        result = hundreds + '百'
        if remainder > 0:
            if remainder < 10:
                result += '零' + digits[remainder]
            else:
                result += number_to_chinese(remainder)
        return result
    else:
        return str(n)  # 超過1000就用阿拉伯數字


def tokenize_rom(text):
    """
    將羅馬字文本分割為詞 tokens
    返回：[{'type': 'word', 'text': 'Kî-táu'}, {'type': 'punct', 'text': ','}, ...]
    """
    tokens = []
    i = 0
    current_word = ""

    while i < len(text):
        char = text[i]

        # 標點符號（包含 ASCII 和 Unicode 引號）
        if char in '.,;:!?\'"()[]""''…—""''\u201C\u201D\u2018\u2019':
            # 保存當前詞
            if current_word.strip():
                tokens.append({
                    'type': 'word',
                    'text': current_word.strip()
                })
                current_word = ""

            # 跳過標點（不添加到 tokens，因為漢字版標點不同）
            i += 1
            continue

        # 空格：詞的分界
        if char == ' ':
            if current_word.strip():
                tokens.append({
                    'type': 'word',
                    'text': current_word.strip()
                })
                current_word = ""
            i += 1
            continue

        # 一般字符
        current_word += char
        i += 1

    # 保存最後的詞
    if current_word.strip():
        tokens.append({
            'type': 'word',
            'text': current_word.strip()
        })

    return tokens


def tokenize_han(text):
    """
    將漢字文本分割為 tokens
    返回：[{'type': 'char', 'text': '起'}, {'type': 'compound', 'text': '第一', 'chars': ['第', '一']}, ...]
    """
    tokens = []
    i = 0

    while i < len(text):
        char = text[i]

        # 專名標記（跳過）
        if char == '{':
            end = text.find('}', i)
            if end != -1:
                # 找到專名，記錄專名內容
                proper_name = text[i+1:end]
                # 拆分專名中的每個字
                for c in proper_name:
                    if c in '。，、；：！？（）「」…':
                        tokens.append({'type': 'punct', 'text': c})
                    elif c.strip():
                        tokens.append({'type': 'char', 'text': c, 'proper_name': True})
                i = end + 1
                continue

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

        # 標點符號（包含中文和 Unicode 引號）
        if char in '。，、；：！？（）「」『』【】…""''\u201C\u201D\u2018\u2019':
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


def extract_proper_names(han_text):
    """
    提取專名標記 {...}
    返回：(乾淨文本, {位置: 長度})
    """
    proper_names = {}  # {start_pos: length}
    clean_text = ""
    offset = 0

    i = 0
    while i < len(han_text):
        if han_text[i] == '{':
            # 找到專名開始
            j = i + 1
            while j < len(han_text) and han_text[j] != '}':
                j += 1

            if j < len(han_text):
                # 找到配對的 }
                proper_name = han_text[i+1:j]
                proper_names[len(clean_text)] = len(proper_name)
                clean_text += proper_name
                i = j + 1
            else:
                # 沒有配對，保留 {
                clean_text += han_text[i]
                i += 1
        else:
            clean_text += han_text[i]
            i += 1

    return clean_text, proper_names


def extract_compound_chars(han_text):
    """
    提取合音字標記 「...」
    返回：(乾淨文本, {位置: 長度})
    """
    compounds = {}  # {start_pos: length}
    clean_text = ""

    i = 0
    while i < len(han_text):
        if han_text[i] == '「':
            # 找到合音字開始
            j = i + 1
            while j < len(han_text) and han_text[j] != '」':
                j += 1

            if j < len(han_text):
                # 找到配對的 」
                compound = han_text[i+1:j]
                compounds[len(clean_text)] = len(compound)
                clean_text += compound
                i = j + 1
            else:
                # 沒有配對，保留 「
                clean_text += han_text[i]
                i += 1
        else:
            clean_text += han_text[i]
            i += 1

    return clean_text, compounds


def align_tokens(han_text, rom_text):
    """
    對齊漢字和羅馬字，生成 token 陣列

    規則：
    - 1 個漢字 = 1 個羅馬字音節
    - 1 個合音字（多個漢字在「」中）= 1 個羅馬字音節
    - 多音節羅馬字詞（用 - 連接）= 對應數量的漢字
    - 標點以漢字為主

    返回：[{"type": "word", "han": "...", "rom": "...", "form": "..."}, ...]
    """
    # Tokenize
    han_tokens = tokenize_han(han_text)
    rom_tokens = tokenize_rom(rom_text)

    # 提取羅馬字詞（忽略標點）
    rom_words = [t for t in rom_tokens if t['type'] == 'word']

    aligned = []
    h_idx = 0  # han index
    r_idx = 0  # rom index

    while h_idx < len(han_tokens):
        h_token = han_tokens[h_idx]

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
        if r_idx < len(rom_words):
            rom_word = rom_words[r_idx]['text']

            # 計算羅馬字音節數量
            rom_syllable_count = len(rom_word.split('-'))

            # 檢查是否是專名
            is_proper_name = h_token.get('proper_name', False)

            if h_token['type'] == 'compound':
                # 合音字：多個漢字對應1個羅馬字音節
                form = 'compound_single'
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
                    # 檢查是否所有字符都有連字號
                    if '-' in rom_word:
                        form = 'phrase'
                    else:
                        form = 'compound'

                    chars = [h_token['text']]
                    h_idx += 1

                    # 收集剩餘的漢字（音節數-1個）
                    # 跳過中間的標點
                    collected = 1
                    while collected < rom_syllable_count and h_idx < len(han_tokens):
                        if han_tokens[h_idx]['type'] == 'char':
                            chars.append(han_tokens[h_idx]['text'])
                            collected += 1
                            h_idx += 1
                        elif han_tokens[h_idx]['type'] == 'compound':
                            # 遇到合音字，也算一個音節
                            chars.append(han_tokens[h_idx]['text'])
                            collected += 1
                            h_idx += 1
                        elif han_tokens[h_idx]['type'] == 'punct':
                            # 跳過標點，不計入詞中
                            h_idx += 1
                        else:
                            break

                    han_text = ''.join(chars)

            token = {
                'type': 'word',
                'han': han_text,
                'rom': rom_word,
                'form': form
            }

            # 添加專名標記
            if is_proper_name:
                token['proper_name'] = True

            aligned.append(token)
            r_idx += 1
        else:
            # 羅馬字已用完，漢字多出來的
            token = {
                'type': 'word',
                'han': h_token['text'],
                'rom': '',
                'form': 'single' if h_token['type'] == 'char' else 'compound_single'
            }
            if h_token.get('proper_name'):
                token['proper_name'] = True

            aligned.append(token)
            h_idx += 1

    # 如果羅馬字還有剩餘
    while r_idx < len(rom_words):
        rom_word = rom_words[r_idx]['text']
        rom_syllable_count = len(rom_word.split('-'))

        aligned.append({
            'type': 'word',
            'han': '',
            'rom': rom_word,
            'form': 'single' if rom_syllable_count == 1 else 'phrase'
        })
        r_idx += 1

    return aligned


def parse_structured_text(file_path):
    """
    解析格式化的文本文件
    返回：{book_name: {chapter_num: {section_titles: [...], verses: {verse_num: text}}}}
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    result = {}
    current_book = None
    current_chapter = None
    current_verse_buffer = []
    pending_section_titles = []  # 暫存在章節之前出現的段落小標

    def flush_verse():
        """完成當前節的收集"""
        if current_verse_buffer and current_book and current_chapter is not None:
            verse_num = current_verse_buffer[0]
            verse_text = ''.join(current_verse_buffer[1:])

            if current_chapter not in result[current_book]['chapters']:
                result[current_book]['chapters'][current_chapter] = {
                    'section_titles': [],
                    'verses': {}
                }

            result[current_book]['chapters'][current_chapter]['verses'][verse_num] = verse_text
            current_verse_buffer.clear()

    for line in lines:
        line = line.rstrip('\n')

        # 空行
        if not line.strip():
            flush_verse()
            continue

        # 一級標題：書名
        if line.startswith('# '):
            flush_verse()
            book_name = line[2:].strip()
            current_book = book_name
            result[current_book] = {'chapters': {}}
            current_chapter = None
            pending_section_titles = []
            continue

        # 三級標題：段落小標
        if line.startswith('### '):
            flush_verse()
            section_title = line[4:].strip()
            if current_book and current_chapter is not None:
                # 章節已經存在，直接添加
                if current_chapter not in result[current_book]['chapters']:
                    result[current_book]['chapters'][current_chapter] = {
                        'section_titles': [],
                        'verses': {}
                    }
                result[current_book]['chapters'][current_chapter]['section_titles'].append(section_title)
            elif current_book:
                # 章節還未出現，暫存
                pending_section_titles.append(section_title)
            continue

        # 二級標題：章號
        if line.startswith('## '):
            flush_verse()
            chapter_str = line[3:].strip()
            try:
                current_chapter = int(chapter_str)
                if current_book:
                    if current_chapter not in result[current_book]['chapters']:
                        result[current_book]['chapters'][current_chapter] = {
                            'section_titles': [],
                            'verses': {}
                        }
                    # 將暫存的段落小標添加到這個章節
                    if pending_section_titles:
                        result[current_book]['chapters'][current_chapter]['section_titles'].extend(pending_section_titles)
                        pending_section_titles = []
            except ValueError:
                pass
            continue

        # 經節行
        match = re.match(r'^(\d+)\s+(.*)', line)
        if match:
            flush_verse()
            verse_num = int(match.group(1))
            verse_content = match.group(2)
            current_verse_buffer = [verse_num, verse_content]
        else:
            # 續行（詩歌體）
            if current_verse_buffer:
                current_verse_buffer.append('\n' + line)

    # 處理最後一節
    flush_verse()

    return result


def find_matching_rom_book(han_book_name, han_book_data, rom_data):
    """
    使用書名對照表找到對應的羅馬字書名
    只有在對照表中有明確配對關係的書才會配對
    """
    # 檢查漢字書名是否在對照表中
    if han_book_name not in HAN_TO_ROM:
        print(f"  Not in mapping table")
        return None, {}

    # 獲取對應的羅馬字書名
    expected_rom_name = HAN_TO_ROM[han_book_name]

    # 檢查這本羅馬字書是否存在於 rom_data 中
    if expected_rom_name in rom_data:
        print(f"  Matched")
        return expected_rom_name, rom_data[expected_rom_name]
    else:
        print(f"  Rom book not found")
        return None, {}


def merge_and_generate_json(han_data, rom_data, output_file):
    """
    合併漢字和羅馬字資料，生成 bible_data.json
    按照聖經書目順序（先舊約再新約）輸出
    """
    books = []
    used_rom_books = set()  # 記錄已使用的羅馬字書名

    # 按照聖經書目順序遍歷（使用 ALL_BOOKS 的順序）
    for rom_name, han_name, eng_name, page in ALL_BOOKS:
        # 檢查這本書是否存在於 han_data 中
        if han_name not in han_data:
            continue

        book_name_han = han_name
        han_book_data = han_data[book_name_han]
        # 找到對應的羅馬字書名（通過內容匹配）
        rom_book_name, rom_book_data = find_matching_rom_book(book_name_han, han_book_data, rom_data)

        if rom_book_name:
            used_rom_books.add(rom_book_name)
        else:
            # 沒有找到對應的羅馬字書內容，但從對照表填入書名
            rom_book_name = HAN_TO_ROM.get(book_name_han, "")
            rom_book_data = {'chapters': {}}

        book = {
            "name_han": book_name_han,
            "name_rom": rom_book_name,
            "name_eng": HAN_TO_ENG.get(book_name_han, ""),
            "chapters": []
        }

        # 遍歷章節
        for chapter_num in sorted(han_book_data['chapters'].keys()):
            han_chapter = han_book_data['chapters'][chapter_num]
            rom_chapter = rom_book_data['chapters'].get(chapter_num, {'section_titles': [], 'verses': {}})

            chapter = {
                "chapter": chapter_num,
                "chapter_title_han": f"第{number_to_chinese(chapter_num)}章",
                "chapter_title_rom": f"Dā̤ {chapter_num} Ca̤uⁿ",
                "sections": []
            }

            # 添加段落標題
            for section_title_han in han_chapter.get('section_titles', []):
                section = {
                    "type": "section_title",
                    "han": section_title_han,
                    "rom": "",  # 目前羅馬字版沒有段落標題
                    "tokens": align_tokens(section_title_han, "")  # 暫時沒有對應的羅馬字
                }
                chapter['sections'].append(section)

            # 添加經節
            for verse_num in sorted(han_chapter['verses'].keys()):
                han_text = han_chapter['verses'][verse_num]
                rom_text = rom_chapter['verses'].get(verse_num, "")

                # 移除專名和合音字標記，得到乾淨的顯示文本
                han_clean, _ = extract_proper_names(han_text)
                han_clean, _ = extract_compound_chars(han_clean)

                verse = {
                    "type": "verse",
                    "verse": verse_num,
                    "rom": rom_text,
                    "han": han_clean,
                    "tokens": align_tokens(han_text, rom_text) if rom_text else []
                }

                chapter['sections'].append(verse)

            book['chapters'].append(chapter)

        books.append(book)

    # 處理只有羅馬字、沒有漢字的書卷（按照聖經書目順序）
    for rom_name, han_name, eng_name, page in ALL_BOOKS:
        if rom_name not in used_rom_books and rom_name in rom_data:
            # 這本羅馬字書沒有對應的漢字版
            rom_book_name = rom_name
            rom_book_data = rom_data[rom_name]

            book = {
                "name_han": han_name,
                "name_rom": rom_book_name,
                "name_eng": eng_name,
                "chapters": []
            }

            # 遍歷章節
            for chapter_num in sorted(rom_book_data['chapters'].keys()):
                rom_chapter = rom_book_data['chapters'][chapter_num]

                chapter = {
                    "chapter": chapter_num,
                    "chapter_title_han": f"第{number_to_chinese(chapter_num)}章",
                    "chapter_title_rom": f"Dā̤ {chapter_num} Ca̤uⁿ",
                    "sections": []
                }

                # 添加段落標題（如果有）
                for section_title_rom in rom_chapter.get('section_titles', []):
                    section = {
                        "type": "section_title",
                        "han": "",
                        "rom": section_title_rom,
                        "tokens": []
                    }
                    chapter['sections'].append(section)

                # 添加經節（只有羅馬字）
                for verse_num in sorted(rom_chapter['verses'].keys()):
                    rom_text = rom_chapter['verses'][verse_num]

                    verse = {
                        "type": "verse",
                        "verse": verse_num,
                        "rom": rom_text,
                        "han": "",
                        "tokens": []
                    }

                    chapter['sections'].append(verse)

                book['chapters'].append(chapter)

            books.append(book)

    # 生成最終 JSON
    result = {"books": books}

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 自動複製到網站目錄
    website_output = Path('website/public/bible_data.json')
    if website_output.parent.exists():
        shutil.copy2(output_file, website_output)
        print(f"  已複製至: {website_output}")
    else:
        print(f"  警告: website/public/ 目錄不存在，跳過複製")

    # 統計
    total_verses_han = sum(
        len(ch['verses'])
        for bk in han_data.values()
        for ch in bk['chapters'].values()
    )
    total_verses_rom = sum(
        len(ch['verses'])
        for bk in rom_data.values()
        for ch in bk['chapters'].values()
    )
    total_chapters_han = sum(len(bk['chapters']) for bk in han_data.values())
    total_chapters_rom = sum(len(bk['chapters']) for bk in rom_data.values())

    print(f"解析完成")
    print(f"  書卷數: {len(books)}")
    print(f"    - 漢字書卷: {len(han_data)}")
    print(f"    - 羅馬字書卷: {len(rom_data)}")
    print(f"    - 配對成功: {len(used_rom_books)}")
    print(f"  章節數: {total_chapters_han} (漢) / {total_chapters_rom} (羅)")
    print(f"  經節數: {total_verses_han} (漢) / {total_verses_rom} (羅)")
    print(f"  輸出: {output_file}")


def main():
    han_file = 'data/han.txt'
    rom_file = 'data/rom.txt'
    output_file = 'data/bible_data.json'

    if len(sys.argv) > 1:
        han_file = sys.argv[1]
    if len(sys.argv) > 2:
        rom_file = sys.argv[2]
    if len(sys.argv) > 3:
        output_file = sys.argv[3]

    print("解析漢字版 (han.txt)...")
    han_data = parse_structured_text(han_file)

    print("解析羅馬字版 (rom.txt)...")
    rom_data = parse_structured_text(rom_file)

    print("合併並生成 JSON...")
    merge_and_generate_json(han_data, rom_data, output_file)


if __name__ == '__main__':
    main()
