import fitz  # PyMuPDF
import json
import os

# ================= 設定區域 =================

INPUT_PDF = "Hinghua_bible.pdf"
OUTPUT_PDF = "Hinghua_bible_bookmarked_with_chapters.pdf"
JSON_FILE = "page-ocr-results.json"

# 目錄頁的「PDF 頁碼」 (從 1 開始)
PAGE_NUM_OT_TOC = 7      # 舊約目錄頁
PAGE_NUM_NT_TOC = 1151   # 新約目錄頁

# 【舊約目錄頁連結設定】
OT_LINK_CONFIG = {
    "start_x": 140, "start_y": 462, "width_col1": 340, "height_col1": 26.9, "line_spacing_col1": 28.4,
    "split_at": 20,
    "col2_x": 490, "col2_start_y": 456, "width_col2": 340, "height_col2": 28.3, "line_spacing_col2": 29.8
}

# 【新約目錄頁連結設定】
NT_LINK_CONFIG = {
    "start_x": 130, "start_y": 462, "width_col1": 340, "height_col1": 26.9, "line_spacing_col1": 28.4,
    "split_at": 14,
    "col2_x": 485, "col2_start_y": 460, "width_col2": 340, "height_col2": 29.5, "line_spacing_col2": 31
}

DEBUG_MODE = False 

# 【舊約 39 卷】 (名稱 | 漢語 | 英文, 起始頁碼)
old_testament_books = [
    ("Cho̤̍ng-sa̤̍-gi̍ | 創世記 | Genesis", 9),
    ("Cheoh-Ai-gi̍h | 出伊及 | Exodus", 72),
    ("Lī-bī Gi̍ | 利未記 | Leviticus", 124),
    ("Míng-so̍ Gi̍ | 民數記 | Numbers", 161),
    ("Sing-mīng Gi̍ | 申命記 | Deuteronomy", 214),
    ("Io̤h-sṳ-a̍ Cṳ | 約書亞書 | Joshua", 262),
    ("Seō-seo Gi̍ | 士師記 | Judges", 294),
    ("Lō-deh Gi̍ | 路得記 | Ruth", 327),
    ("Sah-bâ̤u-cî Céng-cṳ | 撒母耳前書 | 1 Samuel", 332),
    ("Sah-bâ̤u-cî Hā̤u-cṳ | 撒母耳後書 | 2 Samuel", 375),
    ("Le̍h-ó̤ng Siō̤ng-ge̤̍ng | 列王上卷 | 1 Kings", 412),
    ("Le̍h-ó̤ng Hā-ge̤̍ng | 列王下卷 | 2 Kings", 454),
    ("Le̍h-dāi Siō̤ng-ge̤̍ng | 歷代上卷 | 1 Chronicles", 494),
    ("Le̍h-dāi Hā-ge̤̍ng | 歷代下卷 | 2 Chronicles", 534),
    ("Î-seō-la̍h Cṳ | 以斯拉書 | Ezra", 580),
    ("Ní-hi-bî Gi̍ | 尼希米記 | Nehemiah", 593),
    ("Î-seō-tiah Cṳ | 以斯帖書 | Esther", 612),
    ("Io̤h-beh Gi̍ | 約伯記 | Job", 622),
    ("Si-peng | 詩篇 | Psalms", 669),
    ("Cing-ngé̤ng | 箴言 | Proverbs", 786),
    ("Dé̤ng-dō̤ Cṳ | 傳道書 | Ecclesiastes", 826),
    ("Sê̤-ló̤-meóng Ē Ngâ-go̤ | 所羅門兮雅歌 | Song of Solomon", 837),
    ("Î-se̤̍-a̍ Cṳ | 以賽亞書 | Isaiah", 845),
    ("Á̤-lī-bî Cṳ | 耶利米書 | Jeremiah", 914),
    ("Á̤-lī-bî Ai-go̤ Cṳ | 耶利米哀歌書 | Lamentations", 989),
    ("Î-sa̤-geh Cṳ | 以西結書 | Ezekiel", 998),
    ("Dāng-î-lî Cṳ | 但以理書 | Daniel", 1063),
    ("Hó̤-sa̤ Cṳ | 何西書 | Hosea", 1083),
    ("Io̤h-cî Cṳ | 約珥書 | Joel", 1094),
    ("A̍-mó̤-seo Cṳ | 亞摩斯書 | Amos", 1098),
    ("O̤-ba-dâ̤ Cṳ | 阿巴底書 | Obadiah", 1107),
    ("Io̤h-ná Cṳ | 約拿書 | Jonah", 1109),
    ("Bî-gia Cṳ | 彌迦書 | Micah", 1112),
    ("Ná-o̤ng Cṳ | 那翁書 | Nahum", 1119),
    ("Ha̍h-ba-go̤h Cṳ | 哈巴谷書 | Habakkuk", 1122),
    ("Sa̤-huang-ngâ Cṳ | 西番雅書 | Zephaniah", 1126),
    ("Ha̍h-gi Cṳ | 哈基書 | Haggai", 1130),
    ("Sah-ga-lī-a̍ Cṳ | 撒迦利亞書 | Zechariah", 1133),
    ("Mâ-la̍h-gi Cṳ | 瑪拉基書 | Malachi", 1145)
]

# 【新約 27 卷】
new_testament_books = [
    ("Mâ-ta̍i | 馬太 | Gospel of Matthew", 1153),
    ("Mâ-kô̤ | 馬可 | Gospel of Mark", 1193),
    ("Lō-ga | 路加 | Gospel of Luke", 1218),
    ("Io̤h-hāng | 約翰 | Gospel of John", 1261),
    ("Seo̍-dó Hēng-dē̤ng | 使徒行傳 | Acts of the Apostles", 1294),
    ("Bô̤-ló̤ Gio̤̍ Ló̤-mâ Náng Cṳ | 保羅寄羅馬儂書 | Romans", 1336),
    ("Bô̤-ló̤ Gio̤̍ Go̤-líng-do̤ Céng-cṳ | 保羅寄哥林多前書 | 1 Corinthians", 1355),
    ("Bô̤-ló̤ Gio̤̍ Go̤-líng-do̤ Hā̤u-cṳ | 保羅寄哥林多後書 | 2 Corinthians", 1374),
    ("Bô̤-ló̤ Gio̤̍ Ga-la̍h-ta̍i Cṳ | 保羅寄加拉太書 | Galatians", 1386),
    ("Bô̤-ló̤ Gio̤̍ Î-heo̍h-sê̤ Cṳ | 保羅寄以弗所書 | Ephesians", 1392),
    ("Bô̤-ló̤ Gio̤̍ Hi-li̍h-bî Náng Cṳ | 保羅寄腓立比儂書 | Philippians", 1398),
    ("Bô̤-ló̤ Gio̤̍ Go̤-ló̤-sa̤ Náng Cṳ | 保羅寄歌羅西儂書 | Colossians", 1403),
    ("Bô̤-ló̤ Gio̤̍ Tiah-sah-ló̤-ní-gia Náng Céng-cṳ | 保羅寄帖撒羅尼迦儂前書 | 1 Thessalonians", 1408),
    ("Bô̤-ló̤ Gio̤̍ Tiah-sah-ló̤-ní-gia Náng Hā̤u-cṳ | 保羅寄帖撒羅尼迦儂後書 | 2 Thessalonians", 1412),
    ("Bô̤-ló̤ Gio̤̍ Dá̤-mó̤-ta̍i Céng-cṳ | 保羅寄提摩太前書 | 1 Timothy", 1415),
    ("Bô̤-ló̤ Gio̤̍ Dá̤-mó̤-ta̍i Hā̤u-cṳ | 保羅寄提摩太後書 | 2 Timothy", 1420),
    ("Bô̤-ló̤ Gio̤̍ Dá̤-do̤ Cṳ | 保羅寄提多書 | Titus", 1424),
    ("Bô̤-ló̤ Gio̤̍ Hi-lī-meóng Cṳ | 保羅寄腓利門書 | Philemon", 1427),
    ("Hi-beh-lái Náng Cṳ | 希伯來儂書 | Hebrews", 1428),
    ("Seo̍-dó Ngâ-go̤h Cṳ | 使徒雅各書 | James", 1442),
    ("Bî-deh Céng-cṳ | 彼得前書 | 1 Peter", 1447),
    ("Bî-deh Hā̤u-cṳ | 彼得後書 | 2 Peter", 1453),
    ("Io̤h-hāng Ih Cṳ | 約翰一書 | 1 John", 1456),
    ("Io̤h-hāng Cī Cṳ | 約翰二書 | 2 John", 1461),
    ("Iók-hâng So̤ⁿ Cṳ | 約翰三書 | 3 John", 1462),
    ("Seo̍-dó Iú-dāi Cṳ | 使徒猶大書 | Jude", 1463),
    ("Seo̍-dó Io̤h-hāng Be̍h-sī-le̤̍h | 使徒約翰默示錄 | Revelation", 1465)
]

# 【各書卷章數統計】
ot_chapter_counts = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4]
nt_chapter_counts = [28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22]

# ================= 輔助功能 =================

def load_json_data(file_path):
    """讀取並排序 JSON 數據 (轉為 List of dict, 按頁碼排序)"""
    if not os.path.exists(file_path):
        print(f"警告: 找不到 {file_path}，將無法生成章節書籤。")
        return []
        
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 轉換為列表並按頁碼排序
    # 結構: [{"page": 9, "chapter": 1, "verse": 1, "book_english": "Genesis"}, ...]
    sorted_pages = []
    for page_str, content in data.items():
        entry = content.copy()
        entry["page_num"] = int(page_str)
        sorted_pages.append(entry)
    
    # 按頁碼排序
    sorted_pages.sort(key=lambda x: x["page_num"])
    return sorted_pages

def find_chapter_start_page(sorted_pages, target_book_eng, target_chapter):
    """
    推算特定書卷、特定章節的起始頁碼
    回傳: PDF 頁碼 (從 1 開始) 或 None
    """
    # 邏輯：
    # 1. 遍歷所有頁面數據
    # 2. 如果找到 (Book == target, Chapter == target, Verse == 1) -> 該頁即為起始頁 (Return P)
    # 3. 如果找到 (Book == target, Chapter > target) 或 (Book == target, Chapter == target, Verse > 1) 或 (Book != target 但頁碼大於該書最早出現頁)
    #    -> 說明目標章節在「上一頁」就已經開始了 (Return P - 1)
    
    found_book_started = False

    for entry in sorted_pages:
        page_num = entry["page_num"]
        book_eng = entry.get("book_english", "").strip()
        chapter = entry.get("chapter", 0)
        verse = entry.get("verse", 0)

        # 忽略不同書卷，直到找到目標書卷
        if book_eng != target_book_eng:
            if found_book_started:
                # 已經遍歷完目標書卷的所有頁面，進入了下一卷書
                # 如果還沒找到精確的Verse 1，那最後一章肯定是在上一頁開始的
                return page_num - 1
            continue
        
        found_book_started = True

        # === 進入目標書卷範圍 ===
        
        # 情況 A: 精確命中 (第 N 章 第 1 節)
        if chapter == target_chapter and verse == 1:
            return page_num
        
        # 情況 B: 已經超過了目標開頭 (章節 > N，或是 章節 = N 但 節數 > 1)
        if chapter > target_chapter or (chapter == target_chapter and verse > 1):
            return page_num - 1
            
    # 如果循環結束還在該書卷內 (例如是最後一卷書的最後一章)，回傳最後一頁
    if found_book_started:
        return sorted_pages[-1]["page_num"]
        
    return None

def extract_english_name(full_name_str):
    """從 'Cho̤̍ng-sa̤̍-gi̍ | 創世記 | Genesis' 提取 'Genesis'"""
    parts = full_name_str.split("|")
    if len(parts) >= 3:
        return parts[2].strip()
    return "" # Fallback

def add_links_to_toc_page(doc, toc_page_num_1based, books_list, config):
    """(保留原有的目錄頁連結功能)"""
    try:
        page_idx = toc_page_num_1based - 1
        page = doc.load_page(page_idx)
    except Exception as e:
        return

    start_x = config["start_x"]
    start_y = config["start_y"]
    width_col1 = config["width_col1"]
    height_col1 = config["height_col1"]
    line_spacing_col1 = config["line_spacing_col1"]
    
    split_at = config["split_at"]
    col2_x = config["col2_x"]
    col2_start_y = config["col2_start_y"]
    width_col2 = config["width_col2"]
    height_col2 = config["height_col2"]
    line_spacing_col2 = config["line_spacing_col2"]

    for i, (book_name, target_page_num) in enumerate(books_list):
        if target_page_num == 0: continue
        if i < split_at:
            current_x = start_x
            current_width = width_col1
            current_height = height_col1
            row_index = i
            current_y = start_y + (row_index * line_spacing_col1)
        else:
            current_x = col2_x
            current_width = width_col2
            current_height = height_col2
            row_index = i - split_at
            current_y = col2_start_y + (row_index * line_spacing_col2)

        link_rect = fitz.Rect(current_x, current_y, current_x + current_width, current_y + current_height)
        page.insert_link({"kind": fitz.LINK_GOTO, "page": target_page_num - 1, "from": link_rect})
        if DEBUG_MODE:
            page.draw_rect(link_rect, color=(1, 0, 0), width=0.5)

# ================= 主程式 =================

def main():
    doc = fitz.open(INPUT_PDF)
    print(f"已開啟: {INPUT_PDF}, 總頁數: {len(doc)}")
    
    # 載入 OCR 數據
    json_data = load_json_data(JSON_FILE)
    print(f"已載入 JSON 數據，共 {len(json_data)} 頁資料。")

    # ---------------- 第一部分：建立側邊欄書籤 (包含章節) ----------------
    toc = []
    toc.append([1, "Gū-sing-io̤h Cé̤ng-cṳ | 舊新約全書 | Holy Bible Containing the Old and New Testaments", 1])
    toc.append([1, "FOREWORD", 3])
    toc.append([1, "Sṳ̄ | 序", 5])

    # === 舊約處理 ===
    toc.append([1, "Gū-io̤h Cé̤ng-cṳ Bo̤̍h-le̤̍h | 舊約全書目錄 | Table of Contents of the Old Testament", PAGE_NUM_OT_TOC])
    
    for idx, (book_str, start_page) in enumerate(old_testament_books):
        if start_page == 0: continue
        
        # Level 2: 書卷名
        toc.append([2, book_str, start_page])
        
        # Level 3: 章節
        if idx < len(ot_chapter_counts):
            total_chapters = ot_chapter_counts[idx]
            eng_name = extract_english_name(book_str)
            
            # 對該書卷的每一章尋找頁碼
            for chap in range(1, total_chapters + 1):
                # 第 1 章通常就是書卷起始頁，不需要查 JSON (避免 JSON 缺漏或誤差)
                if chap == 1:
                    chap_page = start_page
                else:
                    chap_page = find_chapter_start_page(json_data, eng_name, chap)
                
                # 如果找到了頁碼，就加入書籤
                if chap_page:
                    toc.append([3, f"Dā̤ {chap} Ca̤uⁿ | 第{chap}章 | Chapter {chap}", chap_page])
                else:
                    # 如果找不到，fallback 到書卷起始頁，或者選擇不加
                    pass 

    # === 新約處理 ===
    toc.append([1, "Sing-io̤h Cé̤ng-cṳ Bo̤̍h-le̤̍h | 新約全書目錄 | Table of Contents of the the New Testament", PAGE_NUM_NT_TOC])
    
    for idx, (book_str, start_page) in enumerate(new_testament_books):
        if start_page == 0: continue
        
        # Level 2: 書卷名
        toc.append([2, book_str, start_page])
        
        # Level 3: 章節
        if idx < len(nt_chapter_counts):
            total_chapters = nt_chapter_counts[idx]
            eng_name = extract_english_name(book_str)
            
            for chap in range(1, total_chapters + 1):
                if chap == 1:
                    chap_page = start_page
                else:
                    chap_page = find_chapter_start_page(json_data, eng_name, chap)
                
                if chap_page:
                    toc.append([3, f"Chapter {chap}", chap_page])

    # 套用書籤
    doc.set_toc(toc, collapse=1)
    print(f"側邊欄書籤已更新！(含章節資訊)")

    # ---------------- 第二部分：目錄頁連結 (維持不變) ----------------
    add_links_to_toc_page(doc, PAGE_NUM_OT_TOC, old_testament_books, OT_LINK_CONFIG)
    add_links_to_toc_page(doc, PAGE_NUM_NT_TOC, new_testament_books, NT_LINK_CONFIG)

    # ---------------- 儲存檔案 ----------------
    doc.save(OUTPUT_PDF)
    print(f"檔案已儲存至: {OUTPUT_PDF}")

if __name__ == "__main__":
    main()