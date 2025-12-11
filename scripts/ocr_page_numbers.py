#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR 識別圖片上的章節號
從每張圖片的上方（左上角、右上角）識別章節號（如 2:32）
生成精確的頁碼-章節對應表
"""

import re
import json
from pathlib import Path
from PIL import Image
import pytesseract
from book_info import get_book_by_page, ALL_BOOKS

# 如果 Windows 系統，需要指定 tesseract 路徑
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_chapter_verse_from_image(image_path: str, page_num: int) -> tuple:
    """
    改進版：從圖片中提取章節號
    """
    try:
        img = Image.open(image_path)
        
        # 1. 調整裁切框 (請先確認這個座標是否真的對準了左上角)
        # 如果是左上角，座標通常應該接近 (100, 100, 800, 400) 之類
        # 原本的 (400, 600...) 在大圖中可能已經跑到中間去了
        # 建議你先執行一次看 debug_crop.png
        crop_box = (400, 600, 1100, 1000) 
        cropped = img.crop(crop_box)

        # 【關鍵步驟 1】轉換為灰階
        cropped = cropped.convert('L')

        # 【關鍵步驟 2】二值化處理 (去除淺色雜訊)
        # 閾值設為 150，小於 150 變黑(文字)，大於變白(背景)
        threshold = 150
        cropped = cropped.point(lambda p: p > threshold and 255) 

        # 【關鍵步驟 3】放大圖片 (Upscaling)
        # Tesseract 在大字體上表現更好，放大 2-3 倍
        new_size = (cropped.width * 3, cropped.height * 3)
        cropped = cropped.resize(new_size, Image.Resampling.LANCZOS)
        
        # 【DEBUG】檢查存在目錄下的圖片長怎樣
        # cropped.save(f"debug_crop_{page_num}.png")

        # 【關鍵步驟 4】調整 Tesseract 參數
        # --psm 6: 假設是一個統一的文本塊 (比 psm 7 對空格容忍度更好)
        # 移除 whitelist: 讓 Tesseract 識別所有字符，我們再用 Python 過濾
        text = pytesseract.image_to_string(
            cropped,
            config='--psm 6' 
        )

        # 【關鍵步驟 5】更強大的 Regex
        # 允許冒號前後有空格 (\s*)
        # 允許數字中間可能有誤判的雜訊
        match = re.search(r'(\d+)\s*[:;]\s*(\d+)', text)
        
        if match:
            chapter = int(match.group(1))
            verse = int(match.group(2))
            
            # 簡單的邏輯檢核：章節不可能超過 150 (詩篇) 或 176 (節) 太誇張的數字
            if 0 < chapter <= 150 and 0 < verse <= 200:
                return chapter, verse
        
        # 如果第一次失敗，嘗試針對 "Underdots" 的修補
        # 很多時候 '2' 會被辨識成非數字字符，這裡可以做 fallback 處理
        # 但通常放大圖片 + 移除 whitelist 就能解決 90%

        # print(f"  [Debug] Raw text for page {page_num}: {text.strip()}") # 除錯看原始文字

    except Exception as e:
        print(f"  [!] 識別錯誤 {image_path}: {e}")

    return None, None


def scan_all_images(image_dir: str, renamed: bool = False) -> dict:
    """
    掃描所有圖片，識別章節號

    Args:
        image_dir: 圖片目錄
        renamed: 是否已重命名為流水號

    Returns:
        {
            '0001': {'chapter': 1, 'verse': 1, 'book': ...},
            '0002': {'chapter': 1, 'verse': 15, 'book': ...},
            ...
        }
    """
    image_path = Path(image_dir)

    if renamed:
        # 已重命名，按數字順序
        image_files = sorted(image_path.glob('*.tif'), key=lambda x: int(x.stem))
    else:
        # 未重命名，使用自然排序
        from natsort import natsorted
        image_files = natsorted(list(image_path.glob('*.tif')))

    print(f"找到 {len(image_files)} 張圖片")
    print("開始 OCR 識別...")

    page_mapping = {}

    for i, img_file in enumerate(image_files, 1):
        # 頁碼（從檔名獲取，或使用序號）
        if renamed:
            page_num = int(img_file.stem)
        else:
            page_num = i

        # OCR 識別
        chapter, verse = extract_chapter_verse_from_image(str(img_file), page_num)

        # 獲取書卷資訊
        book_info = get_book_by_page(page_num)

        if chapter and verse and book_info:
            page_mapping[f"{page_num:04d}"] = {
                'chapter': chapter,
                'verse': verse,
                'book_lomaci': book_info[0],
                'book_hanci': book_info[1],
                'book_english': book_info[2]
            }

            if i % 1 == 0:
                print(f"  進度: {i}/{len(image_files)} - {book_info[1]} {chapter}:{verse}")
        else:
            # 識別失敗，使用前一頁的資訊推測
            if page_mapping:
                last_page = list(page_mapping.values())[-1]
                page_mapping[f"{page_num:04d}"] = {
                    'chapter': last_page['chapter'],
                    'verse': None,  # 無法確定
                    'book_lomaci': last_page['book_lomaci'],
                    'book_hanci': last_page['book_hanci'],
                    'book_english': last_page['book_english'],
                    'ocr_failed': True
                }

            if i % 50 == 0:
                print(f"  進度: {i}/{len(image_files)} - 識別失敗")

    print(f"\n[OK] OCR 完成！成功識別 {len([p for p in page_mapping.values() if 'ocr_failed' not in p])} 頁")

    return page_mapping


def generate_chapter_page_mapping(page_mapping: dict, output_file: str = 'chapter-page-mapping.json'):
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
        book_hanci = info['book_hanci']
        chapter = info['chapter']
        verse = info.get('verse')

        # 新書卷
        if book_hanci != current_book:
            # 保存前一章
            if current_book and current_chapter and chapter_start_page:
                prev_page = f"{int(page_num_str) - 1:04d}"
                chapter_mapping[current_book][str(current_chapter)] = {
                    'page_start': chapter_start_page,
                    'page_end': prev_page,
                    'verses': chapter_verses
                }

            current_book = book_hanci
            current_chapter = chapter
            chapter_start_page = page_num_str
            chapter_verses = {}

            if current_book not in chapter_mapping:
                chapter_mapping[current_book] = {}

        # 新章
        elif chapter != current_chapter:
            # 保存前一章
            prev_page = f"{int(page_num_str) - 1:04d}"
            chapter_mapping[current_book][str(current_chapter)] = {
                'page_start': chapter_start_page,
                'page_end': prev_page,
                'verses': chapter_verses
            }

            current_chapter = chapter
            chapter_start_page = page_num_str
            chapter_verses = {}

        # 記錄verse位置
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

    # 輸出 JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chapter_mapping, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] 已生成章節-頁碼對應表：{output_file}")

    # 統計
    total_chapters = sum(len(chapters) for chapters in chapter_mapping.values())
    print(f"  共 {len(chapter_mapping)} 卷")
    print(f"  共 {total_chapters} 章")

    return chapter_mapping


if __name__ == '__main__':
    import sys

    print("=" * 60)
    print("興化語聖經 - OCR 頁碼識別工具")
    print("=" * 60)

    # 檢查 tesseract 是否安裝
    try:
        pytesseract.get_tesseract_version()
        print("[OK] Tesseract OCR 已安裝")
    except:
        print("[ERROR] 錯誤：未找到 Tesseract OCR")
        print("  請安裝 Tesseract：")
        print("  - Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  - macOS: brew install tesseract")
        print("  - Linux: sudo apt-get install tesseract-ocr")
        sys.exit(1)

    # 選擇圖片目錄
    if Path('pics').exists():
        image_dir = 'pics'
        renamed = True
        print(f"\n使用圖片目錄：{image_dir}")
    else:
        print("[ERROR] 找不到 pics 目錄")
        sys.exit(1)

    # 掃描圖片
    page_mapping = scan_all_images(image_dir, renamed=renamed)

    # 保存原始 OCR 結果
    with open('page-ocr-results.json', 'w', encoding='utf-8') as f:
        json.dump(page_mapping, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] 已保存 OCR 原始結果：page-ocr-results.json")

    # 生成章節對應表
    chapter_mapping = generate_chapter_page_mapping(page_mapping)

    print("\n[DONE] 完成！")
