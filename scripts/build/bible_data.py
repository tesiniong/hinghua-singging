#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
建構興化語聖經數據（Build Bible Data）

功能：
1. 解析 rom.txt 和 han.txt，生成 bible_data.json
   （data/ocr-draft.json 列出的節標成 OCR 草稿：verse.rom_draft、chapter.draft_verses）
2. 生成統計資料 stats.json
3. 自動複製所有必要的 JSON 檔案到 website/public/
4. 自動重新生成羅馬字轉漢字字典 romToHanDict.json

使用方法：
    python scripts/build/bible_data.py [han_file] [rom_file] [output_file]

整條建置流程請用 scripts/build_all.py，它會連同字典與同音字表一起更新。

注意：當聖經資料或詞典更新時，執行此腳本即可完成所有構建步驟！
"""

import re
import json
import sys
import shutil
from pathlib import Path
import unicodedata

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _paths import DATA, PUBLIC
from book_info import ALL_BOOKS, HAN_TO_ROM, ROM_TO_HAN, HAN_TO_ENG

DRAFT_FILE = DATA / 'ocr-draft.json'


def load_draft():
    """data/ocr-draft.json → {英文書名: {(章, 節): [校對旗標, …]}}。

    OCR 填入、尚未校對的羅馬字經文（scripts/tools/ocr/assemble.py --write 維護）。
    """
    if not DRAFT_FILE.exists():
        return {}
    with open(DRAFT_FILE, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    return {eng: {tuple(int(x) for x in key.split(':')): flags for key, flags in verses.items()}
            for eng, verses in raw.items()}


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


def is_hanzi(char):
    """檢查一個字符是否在指定的漢字 Unicode 範圍內"""
    return any([
        '\u4e00' <= char <= '\u9fff',  # 基本區
        '\u3400' <= char <= '\u4dbf',  # 擴A
        '\u20000' <= char <= '\u2a6df', # B區
        '\u2a700' <= char <= '\u2b73f', # C區
        '\u2b740' <= char <= '\u2b81f', # D區
        '\u2b820' <= char <= '\u2ceaf', # E區
        '\u2ceb0' <= char <= '\u2ebef', # F區
        '\u30000' <= char <= '\u3134f', # G區
        '\u31350' <= char <= '\u323af', # H區
        '\u2ebf0' <= char <= '\u2ee5f', # I區
        '\u323b0' <= char <= '\u3347f', # J區
        '\uf900' <= char <= '\ufaff',  # 相容表意文字
        '\u3300' <= char <= '\u33ff',  # 相容字元
        '\ufe30' <= char <= '\ufe4f',  # 相容形式
        '\u31c0' <= char <= '\u31ef',  # 筆畫
    ])

def tokenize_han(text):
    """
    將漢字文本分割為 tokens，能處理夾雜的羅馬字 (V3)。
    將夾雜的羅馬字也按音節拆分。
    """
    tokens = []
    i = 0
    punct_chars = '。，、；：！？（）「」『』【】…""''\u201C\u201D\u2018\u2019'

    while i < len(text):
        char = text[i]

        if char == '{': # 專名
            end = text.find('}', i)
            if end != -1:
                tokens.extend(tokenize_han(text[i+1:end]))
                i = end + 1
                continue
        
        if char == '「': # 合音字
            end = text.find('」', i)
            if end != -1:
                tokens.append({'type': 'compound', 'text': text[i+1:end]})
                i = end + 1
                continue

        if char in punct_chars:
            tokens.append({'type': 'punct', 'text': char})
            i += 1
            continue

        if char.isspace():
            i += 1
            continue

        if is_hanzi(char):
            tokens.append({'type': 'char', 'text': char})
            i += 1
            continue

        # 非漢字、非標點、非空白 -> 視為羅馬字
        j = i
        rom_string = ""
        while j < len(text) and not is_hanzi(text[j]) and text[j] not in punct_chars and not text[j].isspace():
            rom_string += text[j]
            j += 1
        
        if rom_string:
            # 按連字號拆分音節
            rom_syllables = rom_string.split('-')
            for syllable in rom_syllables:
                if syllable:
                    tokens.append({'type': 'rom_in_han', 'text': syllable})
            i = j
        else:
            i += 1 # 保底
            
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
    對齊漢字和羅馬字，生成 token 陣列 (V4)
    最終修正版：以羅馬字詞為單位遍歷，消耗對應數量的漢字單元，正確處理標點。
    """
    if not han_text and not rom_text:
        return []
        
    han_units = tokenize_han(han_text)
    rom_words = tokenize_rom(rom_text)

    aligned_tokens = []
    h_cursor = 0  # 漢字單元流的指針

    for rom_word_token in rom_words:
        # 處理 rom_word 前的標點
        while h_cursor < len(han_units) and han_units[h_cursor]['type'] == 'punct':
            aligned_tokens.append({
                'type': 'punct',
                'han': han_units[h_cursor]['text'],
                'rom': ''
            })
            h_cursor += 1

        rom_word = rom_word_token['text']
        rom_syllables = rom_word.split('-')
        num_syllables = len(rom_syllables)

        # 收集對應數量的漢字單元
        collected_han_units = []
        temp_h_cursor = h_cursor
        while len(collected_han_units) < num_syllables and temp_h_cursor < len(han_units):
            if han_units[temp_h_cursor]['type'] != 'punct':
                collected_han_units.append(han_units[temp_h_cursor])
            temp_h_cursor += 1
        
        # 如果成功收集到漢字單元，則組合成一個詞
        if collected_han_units:
            # han_part_text = "".join([t['text'] for t in collected_han_units])
            han_part_parts = []
            for i, unit in enumerate(collected_han_units):
                han_part_parts.append(unit['text'])
                # 如果當前是 rom_in_han 且下一個也是 rom_in_han，則在中間加連字號
                if i < len(collected_han_units) - 1 and \
                   unit['type'] == 'rom_in_han' and \
                   collected_han_units[i+1]['type'] == 'rom_in_han':
                    han_part_parts.append('-')
            han_part_text = "".join(han_part_parts)
            
            form = 'phrase' if num_syllables > 1 or len(collected_han_units) > 1 else 'single'
            if len(collected_han_units) == 1 and collected_han_units[0]['type'] == 'compound':
                form = 'compound_single'

            aligned_tokens.append({
                'type': 'word',
                'han': han_part_text,
                'rom': rom_word,
                'form': form
            })
            h_cursor = temp_h_cursor # 更新主指針

    # 處理結尾剩餘的標點
    while h_cursor < len(han_units) and han_units[h_cursor]['type'] == 'punct':
        aligned_tokens.append({
            'type': 'punct',
            'han': han_units[h_cursor]['text'],
            'rom': ''
        })
        h_cursor += 1
        
    return aligned_tokens

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
            book_name = unicodedata.normalize('NFC', line[2:].strip())
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





def merge_and_generate_json(han_data, rom_data, output_file):
    """
    合併漢字和羅馬字資料，生成 bible_data.json
    按照聖經書目順序（從 book_info.py 的 ALL_BOOKS）輸出
    """
    books = []
    draft = load_draft()
    draft_seen = set()  # 已對上經文的草稿標記；剩下的就是過時的
    
    # 計算 testament 分界索引
    foreword_count = len([b for b in ALL_BOOKS if b["eng"] in ("Foreword", "Preface")])
    ot_count = 39  # 舊約 39 卷

    for idx, book_info in enumerate(ALL_BOOKS):
        rom_name = unicodedata.normalize('NFC', book_info["rom"])
        han_name = unicodedata.normalize('NFC', book_info["han"])
        eng_name = book_info["eng"]
        abbr = book_info["abbr"]
        total_chapters = book_info["chapters"]

        # 判斷所屬部分
        if idx < foreword_count:
            testament = "foreword"
        elif idx < foreword_count + ot_count:
            testament = "ot"
        else:
            testament = "nt"

        print(f"處理中: {eng_name}")
        book = {
            "name_han": han_name,
            "name_rom": rom_name,
            "name_eng": eng_name,
            "abbr": abbr,
            "total_chapters": total_chapters,
            "testament": testament,
            "chapters": []
        }

        # Case 1: 英文序
        if eng_name == 'Foreword':
            try:
                with open(DATA / 'foreword-en.txt', 'r', encoding='utf-8') as f:
                    content = f.read()
                paragraphs = [p.strip() for p in content.splitlines() if p.strip()]
                sections = []
                for i, para_text in enumerate(paragraphs):
                    sections.append({ "type": "verse", "verse": i + 1, "rom": para_text, "han": "", "tokens": [] })
                book['chapters'].append({ "chapter": 1, "chapter_title_han": "", "chapter_title_rom": "", "sections": sections })
                books.append(book)
            except FileNotFoundError:
                print(f"  警告: foreword-en.txt 不存在，已跳過")
            continue

        # Case 2: 興化語序
        if eng_name == 'Preface':
            try:
                with open(DATA / 'foreword-cpx.txt', 'r', encoding='utf-8') as f:
                    content = f.read()

                rom_part, han_part = "", ""
                if "# 序" in content:
                    parts = content.split("# 序")
                    rom_part = parts[0].replace("# Sṳ̄.", "").strip()
                    han_part = parts[1].strip() if len(parts) > 1 else ""

                rom_lines = [p.strip() for p in rom_part.splitlines() if p.strip()]
                han_lines = [p.strip() for p in han_part.splitlines() if p.strip()]

                sections = []
                num_lines = max(len(rom_lines), len(han_lines))
                for i in range(num_lines):
                    rom_text = rom_lines[i] if i < len(rom_lines) else ""
                    han_text = han_lines[i] if i < len(han_lines) else ""
                    han_clean, _ = extract_proper_names(han_text)
                    han_clean, _ = extract_compound_chars(han_clean)

                    sections.append({
                        "type": "verse", "verse": i + 1, "rom": rom_text, "han": han_clean,
                        "tokens": align_tokens(han_text, rom_text) if rom_text and han_text else []
                    })
                book['chapters'].append({ "chapter": 1, "chapter_title_han": "", "chapter_title_rom": "", "sections": sections })
                books.append(book)
            except FileNotFoundError:
                print(f"  警告: foreword-cpx.txt 不存在，已跳過")
            continue

        # Case 3: 一般聖經書卷
        han_book_data = han_data.get(han_name)
        rom_book_data = rom_data.get(rom_name)
        book_draft = draft.get(eng_name, {})

        if not han_book_data and not rom_book_data:
            print(f"  警告: {eng_name} 在 han.txt 和 rom.txt 中均未找到，已跳過")
            continue

        chapter_keys = set()
        if han_book_data:
            chapter_keys.update(han_book_data.get('chapters', {}).keys())
        if rom_book_data:
            chapter_keys.update(rom_book_data.get('chapters', {}).keys())
        
        if not chapter_keys:
            continue

        for chapter_num in sorted(list(chapter_keys)):
            han_chapter = han_book_data.get('chapters', {}).get(chapter_num) if han_book_data else None
            rom_chapter = rom_book_data.get('chapters', {}).get(chapter_num) if rom_book_data else None

            chapter = {
                "chapter": chapter_num,
                "chapter_title_han": f"第{number_to_chinese(chapter_num)}章",
                "chapter_title_rom": f"Dā̤ {chapter_num} Ca̤uⁿ",
                "sections": []
            }
            
            han_verses = han_chapter.get('verses', {}) if han_chapter else {}
            rom_verses = rom_chapter.get('verses', {}) if rom_chapter else {}
            all_verse_nums = sorted(list(set(han_verses.keys()) | set(rom_verses.keys())))

            if not all_verse_nums and not (han_chapter and han_chapter.get('section_titles')):
                continue

            if han_chapter and han_chapter.get('section_titles'):
                for section_title_han in han_chapter['section_titles']:
                     chapter['sections'].append({
                        "type": "section_title", "han": section_title_han, "rom": "",
                        "tokens": align_tokens(section_title_han, "")
                    })

            for verse_num in all_verse_nums:
                han_text = han_verses.get(verse_num, "")
                rom_text = rom_verses.get(verse_num, "")
                
                han_clean, tokens = "", []
                if han_text:
                    han_clean, _ = extract_proper_names(han_text)
                    han_clean, _ = extract_compound_chars(han_text)

                if rom_text and han_text:
                    tokens = align_tokens(han_text, rom_text)
                elif rom_text:
                    # 純羅馬字：統一格式為 {'type': ..., 'han': '', 'rom': ...}
                    tokens = [{'type': t['type'], 'han': '', 'rom': t['text']}
                              for t in tokenize_rom(rom_text)]
                elif han_text:
                    # 純漢字：統一格式為 {'type': ..., 'han': ..., 'rom': ''}
                    tokens = [{'type': t['type'], 'han': t['text'], 'rom': ''}
                              for t in tokenize_han(han_text)]

                section = {
                    "type": "verse", "verse": verse_num, "rom": rom_text, "han": han_clean,
                    "tokens": tokens
                }
                if rom_text and (chapter_num, verse_num) in book_draft:
                    # OCR 草稿：前端據此顯示「OCR 辨識草稿，未經校對」，字典與同音字表建置略過
                    section["rom_draft"] = list(book_draft[(chapter_num, verse_num)])
                    draft_seen.add((eng_name, chapter_num, verse_num))
                chapter['sections'].append(section)

            n_draft = sum(1 for s in chapter['sections'] if 'rom_draft' in s)
            if n_draft:
                chapter['draft_verses'] = n_draft
                chapter['draft_flagged'] = sum(1 for s in chapter['sections'] if s.get('rom_draft'))
            
            if chapter['sections']:
                book['chapters'].append(chapter)
        
        if book['chapters']:
            books.append(book)

    stale = [(eng, c, v) for eng, verses in draft.items() for (c, v) in verses if (eng, c, v) not in draft_seen]
    for eng, c, v in stale:
        print(f"  警告: ocr-draft.json 的 {eng} {c}:{v} 在 rom.txt 沒有內容，標記已過時（用 scripts/tools/ocr/draft.py --check）")

    result = {"books": books}
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 生成 bookList.json（包含所有 68 本書的基本資訊，供前端選單使用）
    from book_info import FOREWORD_BOOKS, OLD_TESTAMENT_BOOKS, NEW_TESTAMENT_BOOKS

    # 建立已有內容的書卷集合（使用英文名稱比對）
    books_with_content = {book['name_eng'] for book in books}

    book_list = []
    for testament_name, testament_books in [
        ("foreword", FOREWORD_BOOKS),
        ("ot", OLD_TESTAMENT_BOOKS),
        ("nt", NEW_TESTAMENT_BOOKS)
    ]:
        for book_info in testament_books:
            eng_name = book_info["eng"]
            book_list.append({
                "rom": book_info["rom"],
                "han": book_info["han"],
                "eng": eng_name,
                "abbr": book_info["abbr"],
                "chapters": book_info["chapters"],
                "testament": testament_name,
                "hasContent": eng_name in books_with_content
            })

    book_list_file = DATA / 'bookList.json'
    with open(book_list_file, 'w', encoding='utf-8') as f:
        json.dump(book_list, f, ensure_ascii=False, indent=2)
    print(f"已生成書目清單: {book_list_file}")

    # 自動複製所有需要的 JSON 檔案到 website/public/
    website_public_dir = PUBLIC
    if website_public_dir.exists():
        # 要複製的檔案列表 (source_path, target_filename)
        files_to_copy = [
            (Path(output_file), 'bible_data.json'),
            (DATA / 'page-ocr-results.json', 'page-ocr-results.json'),
            (DATA / 'chapter-page-mapping.json', 'chapter-page-mapping.json'),
            (book_list_file, 'bookList.json'),
        ]

        print(f"\n複製 JSON 檔案到 website/public/:")
        for source, target_name in files_to_copy:
            target = website_public_dir / target_name
            if source.exists():
                shutil.copy2(source, target)
                print(f"  [OK] {target_name}")
            else:
                print(f"  [SKIP] {target_name} (來源檔案不存在: {source})")
    else:
        print(f"\n  警告: website/public/ 目錄不存在，跳過複製")

    # --- 開始產生統計資料 ---
    from book_info import TOTALS, OLD_TESTAMENT_BOOKS, NEW_TESTAMENT_BOOKS
    
    ot_books_rom_names = {unicodedata.normalize('NFC', b["rom"]) for b in OLD_TESTAMENT_BOOKS}
    nt_books_rom_names = {unicodedata.normalize('NFC', b["rom"]) for b in NEW_TESTAMENT_BOOKS}

    # rom 的 draft_verses 是 verses 之中尚未校對的 OCR 草稿節數
    stats = {
        "rom": {"ot": {"books": 0, "chapters": 0, "verses": 0, "draft_verses": 0},
                "nt": {"books": 0, "chapters": 0, "verses": 0, "draft_verses": 0}},
        "han": {"ot": {"books": 0, "chapters": 0, "verses": 0}, "nt": {"books": 0, "chapters": 0, "verses": 0}},
    }

    for book in books:
        book_rom_name = unicodedata.normalize('NFC', book['name_rom'])
        is_ot = book_rom_name in ot_books_rom_names
        is_nt = book_rom_name in nt_books_rom_names
        
        testament = None
        if is_ot:
            testament = "ot"
        elif is_nt:
            testament = "nt"

        if testament:
            has_rom_content = any(s.get('rom') for c in book['chapters'] for s in c['sections'])
            has_han_content = any(s.get('han') for c in book['chapters'] for s in c['sections'])

            if has_rom_content:
                stats["rom"][testament]["books"] += 1
            if has_han_content:
                stats["han"][testament]["books"] += 1

            for chapter in book['chapters']:
                has_rom_chapter = any(s.get('rom') for s in chapter['sections'])
                has_han_chapter = any(s.get('han') for s in chapter['sections'])

                if has_rom_chapter:
                    stats["rom"][testament]["chapters"] += 1
                if has_han_chapter:
                    stats["han"][testament]["chapters"] += 1
                
                stats["rom"][testament]["verses"] += sum(1 for s in chapter['sections'] if s.get('type') == 'verse' and s.get('rom'))
                stats["rom"][testament]["draft_verses"] += chapter.get('draft_verses', 0)
                stats["han"][testament]["verses"] += sum(1 for s in chapter['sections'] if s.get('type') == 'verse' and s.get('han'))

    # 計算總計
    for lang in ["rom", "han"]:
        stats[lang]["total"] = {
            "books": stats[lang]["ot"]["books"] + stats[lang]["nt"]["books"],
            "chapters": stats[lang]["ot"]["chapters"] + stats[lang]["nt"]["chapters"],
            "verses": stats[lang]["ot"]["verses"] + stats[lang]["nt"]["verses"],
        }
    stats["rom"]["total"]["draft_verses"] = stats["rom"]["ot"]["draft_verses"] + stats["rom"]["nt"]["draft_verses"]
    
    stats["totals"] = TOTALS

    # 寫入 stats.json
    stats_output_path = PUBLIC / 'stats.json'
    with open(stats_output_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"  已產生統計資料: {stats_output_path}")

    print(f"\n解析完成")
    print(f"  總書卷數: {len(books)}")
    print(f"  羅馬字: {stats['rom']['total']['verses']} 節 / {stats['rom']['total']['chapters']} 章 / {stats['rom']['total']['books']} 本"
          f"（含 OCR 草稿 {stats['rom']['total']['draft_verses']} 節）")
    print(f"  漢字: {stats['han']['total']['verses']} 節 / {stats['han']['total']['chapters']} 章 / {stats['han']['total']['books']} 本")
    print(f"  輸出檔案: {output_file}, {stats_output_path.name}")


def main():
    han_file = DATA / 'han.txt'
    rom_file = DATA / 'rom.txt'
    output_file = DATA / 'bible_data.json'

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
