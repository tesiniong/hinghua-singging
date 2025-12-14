#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析興化語聖經文本（第四版）
支援新的格式化文本：每節一行，有標題和段落標題
"""

import re
import json
import sys
import shutil
from pathlib import Path
import unicodedata
from book_info import ALL_BOOKS, HAN_TO_ROM, ROM_TO_HAN, HAN_TO_ENG

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
    對齊漢字和羅馬字，生成 token 陣列 (重構版)
    以羅馬字詞為單位進行遍歷，來解決包含合音字的 phrase 的對齊問題
    """
    han_tokens = tokenize_han(han_text)
    rom_tokens = tokenize_rom(rom_text)

    aligned = []
    h_idx = 0  # han_tokens 的索引
    r_idx = 0  # rom_tokens 的索引

    while h_idx < len(han_tokens) or r_idx < len(rom_tokens):
        # 優先處理漢字中的標點
        if h_idx < len(han_tokens) and han_tokens[h_idx]['type'] == 'punct':
            aligned.append({
                'type': 'punct',
                'han': han_tokens[h_idx]['text'],
                'rom': ''
            })
            h_idx += 1
            continue

        # 如果漢字用完，或羅馬字用完，則退出（正常情況下不應發生）
        if h_idx >= len(han_tokens) or r_idx >= len(rom_tokens):
            break

        rom_token = rom_tokens[r_idx]
        rom_word = rom_token['text']
        rom_syllables = rom_word.split('-')
        num_syllables = len(rom_syllables)

        # 收集對應數量的漢字 token
        collected_han_tokens = []
        temp_h_idx = h_idx
        while len(collected_han_tokens) < num_syllables and temp_h_idx < len(han_tokens):
            # 跳過標點
            if han_tokens[temp_h_idx]['type'] == 'punct':
                temp_h_idx += 1
                continue
            collected_han_tokens.append(han_tokens[temp_h_idx])
            temp_h_idx += 1
        
        han_part_text = "".join([t['text'] for t in collected_han_tokens])
        
        # 判斷 form 類型
        if num_syllables == 1 and len(collected_han_tokens) == 1:
            if collected_han_tokens[0]['type'] == 'char':
                form = 'single'
            else: # compound
                form = 'compound_single'
        else:
            form = 'phrase'
            
        # 檢查專有名詞
        is_proper_name = any(t.get('proper_name', False) for t in collected_han_tokens)

        token = {
            'type': 'word',
            'han': han_part_text,
            'rom': rom_word,
            'form': form
        }
        if is_proper_name:
            token['proper_name'] = True
        
        aligned.append(token)

        # 更新索引
        h_idx = temp_h_idx
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
    
    for rom_name_orig, han_name_orig, eng_name, page in ALL_BOOKS:
        rom_name = unicodedata.normalize('NFC', rom_name_orig)
        han_name = unicodedata.normalize('NFC', han_name_orig)

        print(f"處理中: {eng_name}")
        book = { "name_han": han_name, "name_rom": rom_name, "name_eng": eng_name, "chapters": [] }

        # Case 1: 英文序
        if eng_name == 'Foreword':
            try:
                with open('data/foreword-en.txt', 'r', encoding='utf-8') as f:
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
                with open('data/foreword-cpx.txt', 'r', encoding='utf-8') as f:
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
                    tokens = tokenize_rom(rom_text)
                elif han_text:
                    tokens = tokenize_han(han_text)

                chapter['sections'].append({
                    "type": "verse", "verse": verse_num, "rom": rom_text, "han": han_clean,
                    "tokens": tokens
                })
            
            if chapter['sections']:
                book['chapters'].append(chapter)
        
        if book['chapters']:
            books.append(book)

    result = {"books": books}
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    website_output = Path('website/public/bible_data.json')
    if website_output.parent.exists():
        shutil.copy2(output_file, website_output)
        print(f"\n  已複製至: {website_output}")
    else:
        print(f"\n  警告: website/public/ 目錄不存在，跳過複製")

    total_verses_han = sum(len(ch.get('verses', {})) for bk in han_data.values() for ch in bk.get('chapters', {}).values())
    total_verses_rom = sum(len(ch.get('verses', {})) for bk in rom_data.values() for ch in bk.get('chapters', {}).values())

    print(f"\n解析完成")
    print(f"  總書卷數: {len(books)}")
    print(f"  總經節數 (han.txt): {total_verses_han}")
    print(f"  總經節數 (rom.txt): {total_verses_rom}")
    print(f"  輸出檔案: {output_file}")


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
