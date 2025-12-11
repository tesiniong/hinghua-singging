#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增量更新腳本
比對新舊版本的 han.txt，識別改動，避免重複排版
"""

import re
import sys
from parse_text_v4 import parse_structured_text

def normalize_text(text):
    """
    標準化文本：移除數字、標點符號、空白，只保留漢字
    用於比對是否有實質內容改動
    """
    # 移除專名標記 {}
    text = re.sub(r'[{}]', '', text)
    # 移除合音字標記 「」
    text = re.sub(r'[「」]', '', text)
    # 移除所有標點符號（中英文）
    text = re.sub(r'[，。；：！？、（）「」『』【】…\.,;:!?\'"()\[\]""'']', '', text)
    # 移除數字
    text = re.sub(r'\d+', '', text)
    # 移除空白
    text = re.sub(r'\s+', '', text)
    return text


def get_verse_key(book, chapter, verse):
    """生成經節唯一標識"""
    return f"{book}:{chapter}:{verse}"


def compare_versions(old_file, new_file):
    """
    比對新舊版本
    返回：{
        'unchanged': [(key, text), ...],
        'added': [(key, text), ...],
        'modified': [(key, old_text, new_text), ...],
        'deleted': [(key, text), ...]
    }
    """
    print(f"解析舊版本: {old_file}")
    old_data = parse_structured_text(old_file)

    print(f"解析新版本: {new_file}")
    new_data = parse_structured_text(new_file)

    # 建立經節索引
    old_verses = {}  # {key: text}
    new_verses = {}  # {key: text}

    # 提取舊版本的所有經節
    for book_name, book_data in old_data.items():
        for chapter_num, chapter_data in book_data['chapters'].items():
            for verse_num, verse_text in chapter_data['verses'].items():
                key = get_verse_key(book_name, chapter_num, verse_num)
                old_verses[key] = verse_text

    # 提取新版本的所有經節
    for book_name, book_data in new_data.items():
        for chapter_num, chapter_data in book_data['chapters'].items():
            for verse_num, verse_text in chapter_data['verses'].items():
                key = get_verse_key(book_name, chapter_num, verse_num)
                new_verses[key] = verse_text

    # 比對
    unchanged = []
    added = []
    modified = []
    deleted = []

    # 檢查新版本中的每一節
    for key, new_text in new_verses.items():
        if key in old_verses:
            old_text = old_verses[key]
            # 標準化後比對
            old_normalized = normalize_text(old_text)
            new_normalized = normalize_text(new_text)

            if old_normalized == new_normalized:
                # 內容未改動
                unchanged.append((key, new_text))
            else:
                # 內容有改動
                modified.append((key, old_text, new_text))
        else:
            # 新增的經節
            added.append((key, new_text))

    # 檢查刪除的經節
    for key, old_text in old_verses.items():
        if key not in new_verses:
            deleted.append((key, old_text))

    return {
        'unchanged': unchanged,
        'added': added,
        'modified': modified,
        'deleted': deleted
    }


def generate_report(comparison, output_file='changes_report.txt'):
    """生成變更報告"""
    unchanged = comparison['unchanged']
    added = comparison['added']
    modified = comparison['modified']
    deleted = comparison['deleted']

    total = len(unchanged) + len(added) + len(modified) + len(deleted)

    lines = []
    lines.append("=" * 60)
    lines.append("增量更新報告")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"總經節數: {total}")
    lines.append(f"  [OK] 未改動: {len(unchanged)} 節 ({len(unchanged)/total*100:.1f}%)")
    lines.append(f"  [+]  新增:   {len(added)} 節 ({len(added)/total*100:.1f}%)")
    lines.append(f"  [~]  修改:   {len(modified)} 節 ({len(modified)/total*100:.1f}%)")
    lines.append(f"  [-]  刪除:   {len(deleted)} 節 ({len(deleted)/total*100:.1f}%)")
    lines.append("")

    needs_attention = len(added) + len(modified)
    if needs_attention > 0:
        lines.append(f"[!] 需要處理: {needs_attention} 節")
    else:
        lines.append("[OK] 無需處理，所有經節未改動")

    lines.append("")
    lines.append("=" * 60)

    # 詳細列表
    if added:
        lines.append("")
        lines.append(f"新增的經節 ({len(added)} 節):")
        lines.append("-" * 60)
        for key, text in sorted(added):
            lines.append(f"  [{key}]")
            lines.append(f"    {text[:100]}...")
            lines.append("")

    if modified:
        lines.append("")
        lines.append(f"修改的經節 ({len(modified)} 節):")
        lines.append("-" * 60)
        for key, old_text, new_text in sorted(modified):
            lines.append(f"  [{key}]")
            lines.append(f"    舊: {old_text[:100]}...")
            lines.append(f"    新: {new_text[:100]}...")
            # 顯示差異
            old_norm = normalize_text(old_text)
            new_norm = normalize_text(new_text)
            lines.append(f"    差異: '{old_norm[:50]}' → '{new_norm[:50]}'")
            lines.append("")

    if deleted:
        lines.append("")
        lines.append(f"刪除的經節 ({len(deleted)} 節):")
        lines.append("-" * 60)
        for key, text in sorted(deleted):
            lines.append(f"  [{key}]")
            lines.append(f"    {text[:100]}...")
            lines.append("")

    # 寫入檔案
    report_text = '\n'.join(lines)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_text)

    # 輸出到終端
    print(report_text)
    print(f"\n完整報告已儲存至: {output_file}")

    return comparison


def main():
    if len(sys.argv) < 3:
        print("用法: python incremental_update.py <舊版本.txt> <新版本.txt> [報告檔案.txt]")
        print("範例: python incremental_update.py han_old.txt han.txt changes_report.txt")
        sys.exit(1)

    old_file = sys.argv[1]
    new_file = sys.argv[2]
    report_file = sys.argv[3] if len(sys.argv) > 3 else 'changes_report.txt'

    print("開始比對...")
    comparison = compare_versions(old_file, new_file)

    print("\n生成報告...")
    generate_report(comparison, report_file)

    # 返回值：如果有需要處理的經節，返回 1
    needs_attention = len(comparison['added']) + len(comparison['modified'])
    if needs_attention > 0:
        print(f"\n[!] 請檢查 {report_file}，處理 {needs_attention} 節經文")
        sys.exit(1)
    else:
        print("\n[OK] 所有經節未改動，無需處理")
        sys.exit(0)


if __name__ == '__main__':
    main()
