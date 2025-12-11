#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聖經書卷資訊
包含羅馬字、漢字、英文名稱及起始頁碼
"""

# 舊約39卷
OLD_TESTAMENT_BOOKS = [
    ("Cho̤̍ng-sa̤̍-gi̍", "創世記", "Genesis", 9),
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

# 新約27卷
NEW_TESTAMENT_BOOKS = [
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

# 合併所有書卷
ALL_BOOKS = OLD_TESTAMENT_BOOKS + NEW_TESTAMENT_BOOKS

def get_book_by_page(page_num: int):
    """
    根據頁碼獲取書卷資訊

    Args:
        page_num: 頁碼（數字）

    Returns:
        (羅馬字, 漢字, 英文, 起始頁) 或 None
    """
    for i, book in enumerate(ALL_BOOKS):
        lomaci, hanci, english, start_page = book

        # 檢查下一卷的起始頁
        if i < len(ALL_BOOKS) - 1:
            next_start = ALL_BOOKS[i + 1][3]
            if start_page <= page_num < next_start:
                return book
        else:
            # 最後一卷
            if page_num >= start_page:
                return book

    return None

def get_book_index(page_num: int):
    """獲取書卷索引（0-based）"""
    for i, book in enumerate(ALL_BOOKS):
        lomaci, hanci, english, start_page = book

        if i < len(ALL_BOOKS) - 1:
            next_start = ALL_BOOKS[i + 1][3]
            if start_page <= page_num < next_start:
                return i
        else:
            if page_num >= start_page:
                return i

    return None


if __name__ == '__main__':
    # 測試
    test_pages = [9, 72, 1153, 1465]

    for page in test_pages:
        book = get_book_by_page(page)
        if book:
            print(f"第 {page} 頁 → {book[1]} ({book[0]})")
