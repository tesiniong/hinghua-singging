#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同音字表資料生成腳本
用途：從 cpx-pron-data.lua 和 bible_data.json 生成同音字表資料
"""

import json
import re
import unicodedata
import argparse
from pathlib import Path
from collections import defaultdict

# 調符位置表
TONE_POSITIONS = {
    # 單字母
    "a": 1, "aa": 1, "e": 1, "ee": 1, "oo": 1, "i": 1, "o": 1, "u": 1, "y": 1,
    # 多字母
    "ai": 1, "au": 1, "aau": 2, "eo": 2, "ia": 2, "ioo": 2, "iu": 2,
    "oi": 1, "ua": 2, "uai": 2, "ui": 1,
    # 鼻音韻
    "ng": 1, "ang": 1, "eng": 1, "ing": 1, "eong": 2, "eeng": 1, "oong": 1,
    "iang": 2, "uang": 2, "yng": 1, "ioong": 2,
    # 鼻化韻
    "ann": 1, "aann": 1, "eenn": 1, "oonn": 1, "iann": 2, "oinn": 1,
    "uann": 2, "aaann": 2, "ioonn": 2,
    # 入聲韻
    "ah": 1, "aih": 1, "aah": 1, "aauh": 3, "eh": 1, "eeh": 1, "eoh": 2,
    "iah": 2, "ih": 1, "iooh": 2, "oih": 1, "ooh": 1, "uah": 2, "uh": 1, "yh": 1,
}

# 聲調符號對應表（數字 → Unicode 組合字元）
TONE_MARKS = {
    '1': '',           # 陰平：無標記
    '2': '\u0301',     # 陽平：´ (acute)
    '3': '\u0302',     # 上聲：ˆ (circumflex)
    '4': '\u030d',     # 陰去：̍ (vertical line above)
    '5': '\u0304',     # 陽去：¯ (macron)
    '6': '',           # 陰入：無標記
    '7': '\u030d',     # 陽入：̍ (vertical line)
}


def input_to_display(input_form):
    """
    將輸入式平話字轉換為顯示用平話字（帶調符）

    Args:
        input_form: 輸入式，如 "sioong5", "gai4"

    Returns:
        顯示式（NFC 正規化），如 "siō̤ng", "ga̍i"
    """
    # 移除末尾可能的星號
    input_form = input_form.rstrip('*').strip()

    # 提取聲調數字（末尾的 1-7）
    tone_match = re.search(r'([1-7])$', input_form)
    if not tone_match:
        # 無聲調標記，直接轉換韻母
        return convert_rhyme(input_form)

    tone = tone_match.group(1)
    syllable_without_tone = input_form[:-1]  # 去除聲調數字

    # 分離聲母和韻母
    initial, rhyme = split_syllable(syllable_without_tone)

    # 轉換韻母（aa → a̤ 等）
    rhyme_display = convert_rhyme(rhyme)

    # 添加聲調符號
    if tone in ['1', '6']:
        # 陰平和陰入無調符
        result = initial + rhyme_display
    else:
        # 根據韻母查找調符位置
        tone_mark = TONE_MARKS[tone]
        tone = 7 if (tone == 4 and rhyme[-1] == 'h') else 4
        rhyme_with_tone = add_tone_mark(rhyme, rhyme_display, tone_mark)
        result = initial + rhyme_with_tone

    # Unicode NFC 正規化
    return unicodedata.normalize('NFC', result)


def split_syllable(syllable):
    """
    分離聲母和韻母

    Args:
        syllable: 不含聲調的音節，如 "sioong", "gai", "ang"

    Returns:
        (initial, rhyme) 元組
    """
    # 可能的聲母列表（按長度降序，避免 ng 被誤判為 n + g）
    initials = ['ng', 'ch', 'b', 'p', 'm', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'c', 's']

    for initial in initials:
        if syllable.startswith(initial):
            rhyme = syllable[len(initial):]
            if initial == 'ng' and rhyme == '':
                return '', 'ng'
            else:
                return initial, rhyme

    # 零聲母
    return '', syllable


def convert_rhyme(rhyme):
    """
    將輸入式韻母轉換為顯示式
    aa → a̤, ee → e̤, oo → o̤, y → ṳ, nn → ⁿ
    """
    rhyme = rhyme.replace('nn', 'ⁿ')  # 鼻化符號
    rhyme = rhyme.replace('aa', 'a̤')
    rhyme = rhyme.replace('ee', 'e̤')
    rhyme = rhyme.replace('oo', 'o̤')
    rhyme = rhyme.replace('y', 'ṳ')
    return rhyme


def add_tone_mark(rhyme_input, rhyme_display, tone_mark):
    """
    在正確位置添加調符

    Args:
        rhyme_input: 輸入式韻母（用於查表），如 "ioong"
        rhyme_display: 已轉換的顯示式韻母，如 "io̤ng"
        tone_mark: 調符 Unicode 字元

    Returns:
        添加調符後的韻母
    """
    # 查找調符位置（0-indexed，基於平話字顯示式）
    position = TONE_POSITIONS.get(rhyme_input, 1)

    return rhyme_display[:position] + tone_mark + rhyme_display[position:]


def parse_lua_file(lua_path):
    """
    解析 cpx-pron-data.lua 檔案

    Returns:
        dict: {漢字: [輸入式讀音列表]}
    """
    result = {}

    with open(lua_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正則表達式提取 ["字"] = {...} 格式
    pattern = r'\["([^"]+)"\]\s*=\s*\{([^}]*)\}'

    for match in re.finditer(pattern, content):
        char = match.group(1)
        prons_str = match.group(2)

        # 提取引號中的讀音
        prons = re.findall(r'"([^"]+)"', prons_str)

        if prons:
            # 將平話字轉回輸入式（需要逆向轉換）
            input_prons = [display_to_input(p.rstrip('*')) for p in prons]
            result[char] = input_prons

    return result


def display_to_input(display_form):
    """
    將顯示式平話字轉回輸入式（近似逆向轉換）

    這是一個簡化版本，用於處理 lua 檔案中的平話字格式
    """
    # 移除所有調符，提取基礎字母和聲調
    # 先正規化為 NFD（分解組合字元）
    nfd = unicodedata.normalize('NFD', display_form)

    # 提取基礎字母和調符
    base = []
    tone = '1'  # 預設陰平
    has_dot_below = False  # 是否有下圓點

    i = 0
    while i < len(nfd):
        char = nfd[i]
        cat = unicodedata.category(char)

        if cat[0] == 'L':  # Letter
            base.append(char)
            # 檢查下一個字符是否為下圓點
            if i + 1 < len(nfd) and nfd[i + 1] == '\u0324':
                has_dot_below = True
                base.append('̤')  # 暫時保留下圓點，後面統一處理
                i += 1  # 跳過下圓點
        elif cat == 'Mn':  # Mark, nonspacing（組合字元）
            # 識別調符
            if char == '\u0301':  # acute
                tone = '2'
            elif char == '\u0302':  # circumflex
                tone = '3'
            elif char == '\u030d':  # vertical line
                tone = '4'
            elif char == '\u0304':  # macron
                tone = '5'
            elif char == '\u0324':  # dot below（下圓點）
                # 已在上面處理，這裡跳過
                pass

        i += 1

    base_str = ''.join(base).lower()  # 轉為小寫

    # 反向轉換特殊字元（按順序很重要）
    base_str = base_str.replace('ⁿ', 'nn')
    base_str = base_str.replace('a̤', 'aa')
    base_str = base_str.replace('e̤', 'ee')
    base_str = base_str.replace('o̤', 'oo')
    base_str = base_str.replace('ṳ', 'y')

    # 判斷入聲（4、7 使用相同調號）
    if tone == '4' and base_str.endswith('h'):
        tone = '7'

    # 無聲調標記時為陰平 1 或陰入 6
    if tone == '1' and base_str.endswith('h'):
        tone = '6'

    return base_str + tone


def extract_bible_pairs(bible_json_path):
    """
    從 bible_data.json 提取單音節漢字-羅馬字對應

    Returns:
        dict: {漢字: set(輸入式讀音)}
    """
    with open(bible_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pairs = defaultdict(set)

    for book in data['books']:
        # 跳過序言
        if book.get('name_eng') in ['Foreword', 'Preface']:
            continue

        for chapter in book.get('chapters', []):
            for section in chapter.get('sections', []):
                if section.get('type') != 'verse':
                    continue

                tokens = section.get('tokens', [])
                for token in tokens:
                    if token.get('type') != 'word':
                        continue

                    han = token.get('han', '')
                    rom = token.get('rom', '')
                    form = token.get('form', '')

                    # 跳過空值
                    if not han or not rom:
                        continue

                    # 計算音節數和字數
                    rom_syllables = len([s for s in rom.split('-') if s])
                    han_chars = len(han)

                    # 對於 phrase 類型，檢查音節數和字數是否一致
                    if form == 'phrase' and rom_syllables != han_chars:
                        continue

                    # 處理單字或一致的 phrase
                    if han_chars == 1:
                        # 單字
                        rom_input = display_to_input(rom)
                        pairs[han].add(rom_input)
                    elif form == 'phrase' and rom_syllables == han_chars:
                        # 多字詞，拆分對應
                        rom_parts = rom.split('-')
                        for char, rom_part in zip(han, rom_parts):
                            rom_input = display_to_input(rom_part)
                            pairs[char].add(rom_input)
                    elif form == 'compound_single':
                        # 合音字：多個漢字對應一個音節
                        rom_input = display_to_input(rom)
                        pairs[han].add(rom_input)

    return pairs


def save_bible_pairs(pairs, output_path):
    """
    將聖經提取的對應關係保存為 YAML 格式

    格式：漢字\t讀音1\t讀音2\t...（按 Unicode 排序）
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 從聖經提取的漢字-羅馬字對應（輸入式）\n")
        f.write("# 格式：漢字<TAB>讀音1<TAB>讀音2<TAB>...\n")
        f.write("# 可手動編輯修正\n\n")

        # 按漢字 Unicode 排序
        for char in sorted(pairs.keys()):
            prons = sorted(pairs[char])
            line = char + '\t' + '\t'.join(prons) + '\n'
            f.write(line)


def load_bible_pairs(yaml_path):
    """
    載入聖經對應關係 YAML 檔案

    Returns:
        dict: {漢字: [輸入式讀音列表]}
    """
    result = {}

    if not Path(yaml_path).exists():
        return result

    with open(yaml_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split('\t')
            if len(parts) >= 2:
                char = parts[0]
                prons = parts[1:]
                result[char] = prons

    return result


def merge_data(lua_data, bible_data):
    """
    合併 lua 和聖經資料

    Returns:
        dict: {漢字: [輸入式讀音列表]}（去重）
    """
    merged = defaultdict(set)

    # 添加 lua 資料
    for char, prons in lua_data.items():
        merged[char].update(prons)

    # 添加聖經資料
    for char, prons in bible_data.items():
        merged[char].update(prons)

    # 轉為 list 並排序
    return {char: sorted(prons) for char, prons in merged.items()}


def decompose_syllable(input_form):
    """
    將輸入式音節分解為 (聲母, 韻母, 聲調)

    Args:
        input_form: 輸入式，如 "sioong5", "gai4", "ang3"

    Returns:
        (initial, rhyme, tone) 元組
    """
    # 提取聲調
    tone_match = re.search(r'([1-7])$', input_form)
    if not tone_match:
        return ('', '', '')

    tone = tone_match.group(1)
    syllable = input_form[:-1]

    # 分離聲母和韻母
    initial, rhyme = split_syllable(syllable)

    return (initial, rhyme, tone)


def generate_homophone_data(merged_data):
    """
    生成同音字表 JSON 資料

    Returns:
        dict: {
            "syllables": [
                {
                    "i": "聲母",
                    "r": "韻母",
                    "t": "聲調",
                    "p_input": "輸入式",
                    "p_display": "平話字（NFC）",
                    "chars": ["字1", "字2", ...]
                }
            ]
        }
    """
    # 按音節分組
    syllable_chars = defaultdict(list)

    for char, prons in merged_data.items():
        for pron in prons:
            # 分解音節
            initial, rhyme, tone = decompose_syllable(pron)

            if not tone:  # 跳過無效音節
                continue

            # 使用 (聲母, 韻母, 聲調) 作為 key
            key = (initial, rhyme, tone)
            syllable_chars[key].append(char)

    # 生成結果
    syllables = []
    for (initial, rhyme, tone), chars in syllable_chars.items():
        # 重組輸入式
        input_form = initial + rhyme + tone

        # 轉換為顯示式
        display_form = input_to_display(input_form)

        syllables.append({
            'i': initial,
            'r': rhyme,
            't': tone,
            'p_input': input_form,
            'p_display': display_form,
            'chars': sorted(set(chars))  # 去重並排序
        })

    # 按聲母、韻母、聲調排序
    syllables.sort(key=lambda x: (x['i'], x['r'], x['t']))

    return {'syllables': syllables}


def main():
    parser = argparse.ArgumentParser(description='生成同音字表資料')
    parser.add_argument(
        '--rebuild-bible-data',
        action='store_true',
        help='重新從 bible_data.json 提取資料並更新 bible-han-rom-pairs.yaml'
    )
    args = parser.parse_args()

    # 檔案路徑
    project_root = Path(__file__).parent.parent
    lua_path = project_root / 'data' / 'cpx-pron-data.lua'
    bible_json_path = project_root / 'data' / 'bible_data.json'
    bible_yaml_path = project_root / 'data' / 'bible-han-rom-pairs.yaml'
    output_path = project_root / 'website' / 'public' / 'homophoneData.json'

    print("[1/5] Parsing cpx-pron-data.lua...")
    lua_data = parse_lua_file(lua_path)
    print(f"      Loaded {len(lua_data)} characters")

    # 載入或重建聖經資料
    if args.rebuild_bible_data:
        print("[2/5] Extracting data from bible_data.json...")
        bible_pairs = extract_bible_pairs(bible_json_path)
        print(f"      Extracted {len(bible_pairs)} characters")

        print(f"[3/5] Saving to {bible_yaml_path}...")
        save_bible_pairs(bible_pairs, bible_yaml_path)

        bible_data = {char: sorted(prons) for char, prons in bible_pairs.items()}
    else:
        print(f"[2/5] Loading {bible_yaml_path}...")
        bible_data = load_bible_pairs(bible_yaml_path)
        print(f"      Loaded {len(bible_data)} characters")

    # 合併資料
    print("[3/5] Merging data...")
    merged_data = merge_data(lua_data, bible_data)
    print(f"      Total {len(merged_data)} characters")

    # 生成同音字表
    print("[4/5] Generating homophone table...")
    homophone_data = generate_homophone_data(merged_data)
    print(f"      Generated {len(homophone_data['syllables'])} syllables")

    # 保存 JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(homophone_data, f, ensure_ascii=False, indent=2)

    print(f"[5/5] Saved to {output_path}")
    print("\n=== DONE ===")

    # 統計資訊
    total_chars = sum(len(s['chars']) for s in homophone_data['syllables'])
    print(f"\nStatistics:")
    print(f"  - Syllables: {len(homophone_data['syllables'])}")
    print(f"  - Characters (with duplicates): {total_chars}")


if __name__ == '__main__':
    main()
