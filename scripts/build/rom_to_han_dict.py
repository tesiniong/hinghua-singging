#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
羅馬字轉漢字字典生成腳本
Generate dictionary for Romanization to Han character conversion

資料來源：
1. data/borhlang_bannuaci.dict.yaml - 莆仙語輸入法詞典（主要詞彙來源）
2. data/bible_data.json - 聖經數據（詞頻統計來源）

輸出：
website/public/romToHanDict.json - 羅馬字轉漢字字典
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# 添加 scripts 目錄到路徑以便導入 romanization_converter
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _paths import ROOT
from romanization_converter import RomanizationConverter


def parse_yaml_dict(yaml_path: Path) -> Tuple[Dict, Dict]:
    """
    解析 borhlang_bannuaci.dict.yaml

    Returns:
        (phrases_dict, syllables_dict)
        - phrases_dict: {輸入式詞組: [(漢字, 詞頻), ...]}
        - syllables_dict: {單音節: [(漢字, 詞頻), ...]}
    """
    phrases = defaultdict(list)
    syllables = defaultdict(list)

    print(f"[1/4] 解析 {yaml_path.name}...")

    with open(yaml_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()

            # 跳過註釋和空行
            if not line or line.startswith('#') or line.startswith('---') or line.startswith('...'):
                continue

            # 跳過 YAML 頭部
            if ':' in line and '@' not in line:
                continue

            # 解析格式：平話字@輸入式@漢字|<TAB>輸入式<TAB>詞頻
            if '@' not in line:
                continue

            try:
                # 分割第一部分和後面部分
                parts = line.split('\t')
                if len(parts) < 3:
                    continue

                first_part = parts[0].rstrip('|')  # 移除結尾的 |
                input_rom = parts[1].strip()
                freq = int(parts[2].strip())

                # 解析第一部分：平話字@輸入式@漢字
                at_split = first_part.split('@')
                if len(at_split) < 3:
                    continue

                buc_form = at_split[0]
                input_form = at_split[1]
                han_chars = at_split[2]

                # 處理漢字（可能有多個，用 / 分隔）
                han_list = [h.strip() for h in han_chars.split('/') if h.strip()]

                # 過濾 ▣（無漢字）
                han_list = [h for h in han_list if h != '▣']
                if not han_list:
                    continue

                # 將輸入式標準化（用連字號連接，不用空格）
                input_key = input_form.replace(' ', '-')

                # 判斷是單音節還是多音節
                syllable_list = input_form.split()

                if len(syllable_list) == 1:
                    # 單音節
                    for han in han_list:
                        syllables[input_key].append((han, freq))
                else:
                    # 多音節詞組
                    for han in han_list:
                        phrases[input_key].append((han, freq))

            except Exception as e:
                print(f"  警告：第 {line_num} 行解析失敗：{e}")
                continue

    print(f"  [OK] 單音節：{len(syllables)} 個")
    print(f"  [OK] 詞組：{len(phrases)} 個")

    return dict(phrases), dict(syllables)


def extract_bible_frequency(bible_json_path: Path) -> Tuple[Dict, Dict]:
    """
    從 bible_data.json 統計詞頻

    Returns:
        (phrase_freq, syllable_freq)
        - phrase_freq: {輸入式詞組: {漢字: 次數}}
        - syllable_freq: {單音節: {漢字: 次數}}（包含從多音節詞分配的部分詞頻）
    """
    phrase_freq = defaultdict(lambda: defaultdict(float))
    syllable_freq = defaultdict(lambda: defaultdict(float))

    # 特殊合音字映射（輸入式 -> 可能的漢字組合列表）
    COMPOUND_CHARS = {
        'dai4': ['第一'],
        'gai4': ['家己'],
        'dau4': ['豆腐'],
        'noong2': ['那當'],
        # 可以繼續添加其他合音字...
    }

    print(f"[2/4] 從 {bible_json_path.name} 統計詞頻...")

    with open(bible_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    converter = RomanizationConverter()

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
                    rom_buc = token.get('rom', '')

                    if not han or not rom_buc:
                        continue

                    # 將平話字轉為輸入式
                    syllable_parts = rom_buc.split('-')
                    input_parts = []

                    for syl in syllable_parts:
                        if syl:
                            try:
                                input_syl = converter.buc_to_input(syl)
                                input_parts.append(input_syl)
                            except:
                                continue

                    if not input_parts:
                        continue

                    input_form = '-'.join(input_parts)

                    # 單音節處理
                    if len(input_parts) == 1:
                        syl = input_parts[0]

                        # 檢查是否為合音字
                        if syl in COMPOUND_CHARS and han in COMPOUND_CHARS[syl]:
                            # 合音字：多個漢字對應一個音節
                            weight = 1.0 / len(han)
                            for ch in han:
                                syllable_freq[syl][ch] += weight
                        elif len(han) == 1:
                            # 普通單字
                            syllable_freq[syl][han] += 1.0

                    # 多音節詞組處理
                    else:
                        # 整體詞頻 +1
                        phrase_freq[input_form][han] += 1

                        # 嘗試對齊音節和漢字，分配部分詞頻
                        han_chars = list(han)
                        syl_idx = 0
                        char_idx = 0
                        alignment_success = True

                        while syl_idx < len(input_parts) and char_idx < len(han_chars):
                            syl = input_parts[syl_idx]

                            # 檢查是否為合音字
                            if syl in COMPOUND_CHARS:
                                matched = False
                                # 嘗試匹配合音字的各種可能寫法
                                for compound in COMPOUND_CHARS[syl]:
                                    if char_idx + len(compound) <= len(han_chars):
                                        han_slice = ''.join(han_chars[char_idx:char_idx+len(compound)])
                                        if han_slice == compound:
                                            # 匹配成功，消耗多個漢字
                                            weight = 1.0 / len(compound)
                                            for ch in compound:
                                                syllable_freq[syl][ch] += weight
                                            char_idx += len(compound)
                                            matched = True
                                            break

                                if not matched:
                                    # 沒匹配到合音字，當普通單字處理
                                    if char_idx < len(han_chars):
                                        syllable_freq[syl][han_chars[char_idx]] += 1.0
                                        char_idx += 1
                            else:
                                # 普通音節，1對1
                                if char_idx < len(han_chars):
                                    syllable_freq[syl][han_chars[char_idx]] += 1.0
                                    char_idx += 1

                            syl_idx += 1

                        # 如果對齊失敗（漢字有剩或音節有剩），標記失敗
                        if char_idx != len(han_chars) or syl_idx != len(input_parts):
                            alignment_success = False

    print(f"  [OK] 單音節詞頻：{len(syllable_freq)} 個")
    print(f"  [OK] 詞組詞頻：{len(phrase_freq)} 個")

    return dict(phrase_freq), dict(syllable_freq)


def merge_data(
    yaml_phrases: Dict,
    yaml_syllables: Dict,
    bible_phrase_freq: Dict,
    bible_syllable_freq: Dict
) -> Dict:
    """
    合併 YAML 和聖經詞頻資料

    **只使用聖經統計的詞頻**，YAML 中有但聖經沒有的詞設為詞頻 1

    Returns:
        {
            "phrases": {
                "輸入式詞組": [
                    {"han": "漢字", "freq": 次數},
                    ...
                ]
            },
            "syllables": {
                "單音節": [
                    {"han": "漢字", "freq": 次數},
                    ...
                ]
            }
        }
    """
    print("[3/4] 合併資料並排序...")

    result = {
        "phrases": {},
        "syllables": {}
    }

    # 處理詞組
    all_phrase_keys = set(yaml_phrases.keys()) | set(bible_phrase_freq.keys())
    # 排序後再走訪：直接迭代 set 會讓每次執行的鍵順序不同，輸出無法重現
    for key in sorted(all_phrase_keys):
        candidates = {}

        # 優先使用聖經詞頻
        if key in bible_phrase_freq:
            for han, count in bible_phrase_freq[key].items():
                candidates[han] = count

        # 添加 YAML 中有但聖經沒有的候選字（詞頻設為 1）
        if key in yaml_phrases:
            for han, _ in yaml_phrases[key]:
                if han not in candidates:
                    candidates[han] = 1  # YAML 中的詞，聖經沒有，設為 1

        # 排序（詞頻從高到低）
        sorted_candidates = [
            {"han": han, "freq": freq}
            for han, freq in sorted(candidates.items(), key=lambda x: (-x[1], x[0]))  # 詞頻降序，相同詞頻按漢字排序
        ]

        result["phrases"][key] = sorted_candidates

    # 處理單音節
    all_syllable_keys = set(yaml_syllables.keys()) | set(bible_syllable_freq.keys())
    # 排序後再走訪：直接迭代 set 會讓每次執行的鍵順序不同，輸出無法重現
    for key in sorted(all_syllable_keys):
        candidates = {}

        # 優先使用聖經詞頻
        if key in bible_syllable_freq:
            for han, count in bible_syllable_freq[key].items():
                candidates[han] = count

        # 添加 YAML 中有但聖經沒有的候選字（詞頻設為 1）
        if key in yaml_syllables:
            for han, _ in yaml_syllables[key]:
                if han not in candidates:
                    candidates[han] = 1  # YAML 中的字，聖經沒有，設為 1

        # 排序（詞頻從高到低）
        sorted_candidates = [
            {"han": han, "freq": freq}
            for han, freq in sorted(candidates.items(), key=lambda x: (-x[1], x[0]))  # 詞頻降序，相同詞頻按漢字排序
        ]

        result["syllables"][key] = sorted_candidates

    print(f"  [OK] 詞組總數：{len(result['phrases'])}")
    print(f"  [OK] 單音節總數：{len(result['syllables'])}")

    return result


def main():
    # 檔案路徑
    project_root = ROOT
    yaml_path = project_root / 'data' / 'borhlang_bannuaci.dict.yaml'
    bible_json_path = project_root / 'data' / 'bible_data.json'
    output_path = project_root / 'website' / 'public' / 'romToHanDict.json'

    # 檢查檔案是否存在
    if not yaml_path.exists():
        print(f"錯誤：找不到 {yaml_path}")
        return
    if not bible_json_path.exists():
        print(f"錯誤：找不到 {bible_json_path}")
        return

    # 1. 解析 YAML
    yaml_phrases, yaml_syllables = parse_yaml_dict(yaml_path)

    # 2. 統計聖經詞頻
    bible_phrase_freq, bible_syllable_freq = extract_bible_frequency(bible_json_path)

    # 3. 合併資料
    merged_data = merge_data(
        yaml_phrases,
        yaml_syllables,
        bible_phrase_freq,
        bible_syllable_freq
    )

    # 4. 保存 JSON
    print(f"[4/4] 保存至 {output_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    print(f"  [OK] 已保存")

    # 統計資訊
    total_phrase_candidates = sum(len(v) for v in merged_data['phrases'].values())
    total_syllable_candidates = sum(len(v) for v in merged_data['syllables'].values())

    print("\n=== 完成 ===")
    print(f"詞組：{len(merged_data['phrases'])} 個，候選字總數：{total_phrase_candidates}")
    print(f"單音節：{len(merged_data['syllables'])} 個，候選字總數：{total_syllable_candidates}")
    print(f"檔案大小：{output_path.stat().st_size / 1024:.1f} KB")


if __name__ == '__main__':
    main()
