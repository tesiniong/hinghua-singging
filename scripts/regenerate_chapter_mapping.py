#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
從 page-ocr-results.json 重新生成 chapter-page-mapping.json
用途：手動編輯 page-ocr-results.json 後，執行此腳本重新生成章節對應表
"""

import json
from pathlib import Path


def generate_chapter_page_mapping(page_mapping: dict, output_file: str = 'data/chapter-page-mapping.json'):
    """
    生成章節-頁碼對應表

    格式：
    {
        "創世記": {
            "1": {"page_start": "0009", "page_end": "0012", "verses": {...}},
            "2": {"page_start": "0013", "page_end": "0015", "verses": {...}},
            ...
        },
        ...
    }
    """
    chapter_mapping = {}

    current_book = None
    current_chapter = None
    chapter_start_page = None
    chapter_verses = {}

    sorted_pages = sorted(page_mapping.items(), key=lambda x: int(x[0]))

    for page_num_str, info in sorted_pages:
        book_han = info['book_han']
        chapter = info['chapter']
        verse = info.get('verse')

        # 新書卷
        if book_han != current_book:
            # 保存前一章
            if current_book and current_chapter and chapter_start_page:
                prev_page = f"{int(page_num_str) - 1:04d}"
                chapter_mapping[current_book][str(current_chapter)] = {
                    'page_start': chapter_start_page,
                    'page_end': prev_page,
                    'verses': chapter_verses
                }

            current_book = book_han
            chapter_mapping[current_book] = {}
            current_chapter = chapter
            chapter_start_page = page_num_str
            chapter_verses = {}

        # 新章節
        elif chapter != current_chapter:
            # 保存前一章
            if chapter_start_page:
                prev_page = f"{int(page_num_str) - 1:04d}"
                chapter_mapping[current_book][str(current_chapter)] = {
                    'page_start': chapter_start_page,
                    'page_end': prev_page,
                    'verses': chapter_verses
                }

            current_chapter = chapter
            chapter_start_page = page_num_str
            chapter_verses = {}

        # 記錄節號
        if verse:
            chapter_verses[str(verse)] = page_num_str

    # 保存最後一章
    if current_book and current_chapter and chapter_start_page:
        last_page = sorted_pages[-1][0]
        chapter_mapping[current_book][str(current_chapter)] = {
            'page_start': chapter_start_page,
            'page_end': last_page,
            'verses': chapter_verses
        }

    # 寫入檔案
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chapter_mapping, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Generated chapter-page mapping: {output_file}")

    # 統計
    total_chapters = sum(len(chapters) for chapters in chapter_mapping.values())
    print(f"  Total books: {len(chapter_mapping)}")
    print(f"  Total chapters: {total_chapters}")

    return chapter_mapping


if __name__ == '__main__':
    print("=" * 60)
    print("[REGENERATE] Chapter-Page Mapping")
    print("=" * 60)

    # 檢查 page-ocr-results.json 是否存在
    if not Path('data/page-ocr-results.json').exists():
        print("[ERROR] data/page-ocr-results.json not found")
        print("  Please run ocr_page_numbers.py first, or create the file manually")
        exit(1)

    # 讀取 OCR 結果
    print("\n[1] Loading data/page-ocr-results.json...")
    with open('data/page-ocr-results.json', 'r', encoding='utf-8') as f:
        page_mapping = json.load(f)

    print(f"[OK] Loaded {len(page_mapping)} pages")

    # 生成章節對應表
    print("\n[2] Generating chapter-page-mapping.json...")
    chapter_mapping = generate_chapter_page_mapping(page_mapping)

    print("\n[DONE] Complete!")
    print("\nUsage:")
    print("  1. Edit data/page-ocr-results.json manually")
    print("  2. Run this script to regenerate data/chapter-page-mapping.json")
