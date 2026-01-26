#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聖經書卷資訊
包含羅馬字、漢字、英文名稱、簡稱、章數、每章節數及起始頁碼
"""

# 【序言】
FOREWORD_BOOKS = [
    {
        "rom": "Foreword",
        "han": "Foreword",
        "eng": "Foreword",
        "abbr": "",
        "start_page": 3,
        "chapters": 1,
        "verses_per_chapter": [0],
    },
    {
        "rom": "Sṳ̄.",
        "han": "序",
        "eng": "Preface",
        "abbr": "序",
        "start_page": 5,
        "chapters": 1,
        "verses_per_chapter": [0],
    },
]

# 舊約39卷
OLD_TESTAMENT_BOOKS = [
    {
        "rom": "Cho̤̍ng-sa̤̍ Gi̍",
        "han": "創世記",
        "eng": "Genesis",
        "abbr": "創",
        "start_page": 9,
        "chapters": 50,
        "verses_per_chapter": [31, 25, 24, 26, 32, 22, 24, 22, 29, 32, 32, 20, 18, 24, 21, 16, 27, 33, 38, 18, 34, 24, 20, 67, 34, 35, 46, 22, 35, 43, 55, 32, 20, 31, 29, 43, 36, 30, 23, 23, 57, 38, 34, 34, 28, 34, 31, 22, 33, 26],
    },
    {
        "rom": "Cheoh-Ai-gi̍h",
        "han": "出伊及",
        "eng": "Exodus",
        "abbr": "出",
        "start_page": 72,
        "chapters": 40,
        "verses_per_chapter": [22, 25, 22, 31, 23, 30, 25, 32, 35, 29, 10, 51, 22, 31, 27, 36, 16, 27, 25, 26, 36, 31, 33, 18, 40, 37, 21, 43, 46, 38, 18, 35, 23, 35, 35, 38, 29, 31, 43, 38],
    },
    {
        "rom": "Lī-bī Gi̍",
        "han": "利未記",
        "eng": "Leviticus",
        "abbr": "利",
        "start_page": 124,
        "chapters": 27,
        "verses_per_chapter": [17, 16, 17, 35, 19, 30, 38, 36, 24, 20, 47, 8, 59, 57, 33, 34, 16, 30, 37, 27, 24, 33, 44, 23, 55, 46, 34],
    },
    {
        "rom": "Míng-so̍ Gi̍",
        "han": "民數記",
        "eng": "Numbers",
        "abbr": "民",
        "start_page": 161,
        "chapters": 36,
        "verses_per_chapter": [54, 34, 51, 49, 31, 27, 89, 26, 23, 36, 35, 16, 33, 45, 41, 50, 13, 32, 22, 29, 35, 41, 30, 25, 18, 65, 23, 31, 40, 16, 54, 42, 56, 29, 34, 13],
    },
    {
        "rom": "Sing-mīng Gi̍",
        "han": "申命記",
        "eng": "Deuteronomy",
        "abbr": "申",
        "start_page": 214,
        "chapters": 34,
        "verses_per_chapter": [46, 37, 29, 49, 33, 25, 26, 20, 29, 22, 32, 32, 18, 29, 23, 22, 20, 22, 21, 20, 23, 30, 25, 22, 19, 19, 26, 68, 29, 20, 30, 52, 29, 12],
    },
    {
        "rom": "Io̤h-sṳ-a̍ Cṳ",
        "han": "約書亞書",
        "eng": "Joshua",
        "abbr": "書",
        "start_page": 262,
        "chapters": 24,
        "verses_per_chapter": [18, 24, 17, 24, 15, 27, 26, 35, 27, 43, 23, 24, 33, 15, 63, 10, 18, 28, 51, 9, 45, 34, 16, 33],
    },
    {
        "rom": "Seō-seo Gi̍",
        "han": "士師記",
        "eng": "Judges",
        "abbr": "士",
        "start_page": 294,
        "chapters": 21,
        "verses_per_chapter": [36, 23, 31, 24, 31, 40, 25, 35, 57, 18, 40, 15, 25, 20, 20, 31, 13, 31, 30, 48, 25],
    },
    {
        "rom": "Lō-deh Gi̍",
        "han": "路得記",
        "eng": "Ruth",
        "abbr": "得",
        "start_page": 327,
        "chapters": 4,
        "verses_per_chapter": [22, 23, 18, 22],
    },
    {
        "rom": "Sah-bâ̤u-cî Céng-cṳ",
        "han": "撒母耳前書",
        "eng": "1 Samuel",
        "abbr": "撒上",
        "start_page": 332,
        "chapters": 31,
        "verses_per_chapter": [28, 36, 21, 22, 12, 21, 17, 22, 27, 27, 15, 25, 23, 52, 35, 23, 58, 30, 24, 42, 15, 23, 29, 22, 44, 25, 12, 25, 11, 31, 13],
    },
    {
        "rom": "Sah-bâ̤u-cî Hā̤u-cṳ",
        "han": "撒母耳後書",
        "eng": "2 Samuel",
        "abbr": "撒下",
        "start_page": 375,
        "chapters": 24,
        "verses_per_chapter": [27, 32, 39, 12, 25, 23, 29, 18, 13, 19, 27, 31, 39, 33, 37, 23, 29, 33, 43, 26, 22, 51, 39, 25],
    },
    {
        "rom": "Le̍h-ó̤ng Siō̤ng-ge̤̍ng",
        "han": "列王上卷",
        "eng": "1 Kings",
        "abbr": "王上",
        "start_page": 412,
        "chapters": 22,
        "verses_per_chapter": [53, 46, 28, 34, 18, 38, 51, 66, 28, 29, 43, 33, 34, 31, 34, 34, 24, 46, 21, 43, 29, 53],
    },
    {
        "rom": "Le̍h-ó̤ng Hā-ge̤̍ng",
        "han": "列王下卷",
        "eng": "2 Kings",
        "abbr": "王下",
        "start_page": 454,
        "chapters": 25,
        "verses_per_chapter": [18, 25, 27, 44, 27, 33, 20, 29, 37, 36, 21, 21, 25, 29, 38, 20, 41, 37, 37, 21, 26, 20, 37, 20, 30],
    },
    {
        "rom": "Le̍h-dāi Siō̤ng-ge̤̍ng",
        "han": "歷代上卷",
        "eng": "1 Chronicles",
        "abbr": "代上",
        "start_page": 494,
        "chapters": 29,
        "verses_per_chapter": [54, 55, 24, 43, 26, 81, 40, 40, 44, 14, 47, 40, 14, 17, 29, 43, 27, 17, 19, 8, 30, 19, 32, 31, 31, 32, 34, 21, 30],
    },
    {
        "rom": "Le̍h-dāi Hā-ge̤̍ng",
        "han": "歷代下卷",
        "eng": "2 Chronicles",
        "abbr": "代下",
        "start_page": 534,
        "chapters": 36,
        "verses_per_chapter": [17, 18, 17, 22, 14, 42, 22, 18, 31, 19, 23, 16, 22, 15, 19, 14, 19, 34, 11, 37, 20, 12, 21, 27, 28, 23, 9, 27, 36, 27, 21, 33, 25, 33, 27, 23],
    },
    {
        "rom": "Î-seō-la̍h Cṳ",
        "han": "以斯拉書",
        "eng": "Ezra",
        "abbr": "拉",
        "start_page": 580,
        "chapters": 10,
        "verses_per_chapter": [11, 70, 13, 24, 17, 22, 28, 36, 15, 44],
    },
    {
        "rom": "Ní-hi-bî Gi̍",
        "han": "尼希米記",
        "eng": "Nehemiah",
        "abbr": "尼",
        "start_page": 593,
        "chapters": 13,
        "verses_per_chapter": [11, 20, 32, 23, 19, 19, 73, 18, 38, 39, 36, 47, 31],
    },
    {
        "rom": "Î-seō-tiah Cṳ",
        "han": "以斯帖書",
        "eng": "Esther",
        "abbr": "斯",
        "start_page": 612,
        "chapters": 10,
        "verses_per_chapter": [22, 23, 15, 17, 14, 14, 10, 17, 32, 3],
    },
    {
        "rom": "Io̤h-beh Gi̍",
        "han": "約伯記",
        "eng": "Job",
        "abbr": "伯",
        "start_page": 622,
        "chapters": 42,
        "verses_per_chapter": [22, 13, 26, 21, 27, 30, 21, 22, 35, 22, 20, 25, 28, 22, 35, 22, 16, 21, 29, 29, 34, 30, 17, 25, 6, 14, 23, 28, 25, 31, 40, 22, 33, 37, 16, 33, 24, 41, 30, 24, 34, 17],
    },
    {
        "rom": "Si-peng",
        "han": "詩篇",
        "eng": "Psalms",
        "abbr": "詩",
        "start_page": 669,
        "chapters": 150,
        "verses_per_chapter": [6, 12, 8, 8, 12, 10, 17, 9, 20, 18, 7, 8, 6, 7, 5, 11, 15, 50, 14, 9, 13, 31, 6, 10, 22, 12, 14, 9, 11, 12, 24, 11, 22, 22, 28, 12, 40, 22, 13, 17, 13, 11, 5, 26, 17, 11, 9, 14, 20, 23, 19, 9, 6, 7, 23, 13, 11, 11, 17, 12, 8, 12, 11, 10, 13, 20, 7, 35, 36, 5, 24, 20, 28, 23, 10, 12, 20, 72, 13, 19, 16, 8, 18, 12, 13, 17, 7, 18, 52, 17, 16, 15, 5, 23, 11, 13, 12, 9, 9, 5, 8, 28, 22, 35, 45, 48, 43, 13, 31, 7, 10, 10, 9, 8, 18, 19, 2, 29, 176, 7, 8, 9, 4, 8, 5, 6, 5, 6, 8, 8, 3, 18, 3, 3, 21, 26, 9, 8, 24, 13, 10, 7, 12, 15, 21, 10, 20, 14, 9, 6],
    },
    {
        "rom": "Cing-ngé̤ng",
        "han": "箴言",
        "eng": "Proverbs",
        "abbr": "箴",
        "start_page": 786,
        "chapters": 31,
        "verses_per_chapter": [33, 22, 35, 27, 23, 35, 27, 36, 18, 32, 31, 28, 25, 35, 33, 33, 28, 24, 29, 30, 31, 29, 35, 34, 28, 28, 27, 28, 27, 33, 31],
    },
    {
        "rom": "Dé̤ng-dō̤ Cṳ",
        "han": "傳道書",
        "eng": "Ecclesiastes",
        "abbr": "傳",
        "start_page": 826,
        "chapters": 12,
        "verses_per_chapter": [18, 26, 22, 16, 20, 12, 29, 17, 18, 20, 10, 14],
    },
    {
        "rom": "Sê̤-ló̤-meóng Ē Ngâ-go̤",
        "han": "所羅門兮雅歌",
        "eng": "Song of Solomon",
        "abbr": "歌",
        "start_page": 837,
        "chapters": 8,
        "verses_per_chapter": [17, 17, 11, 16, 16, 13, 13, 14],
    },
    {
        "rom": "Î-se̤̍-a̍ Cṳ",
        "han": "以賽亞書",
        "eng": "Isaiah",
        "abbr": "賽",
        "start_page": 845,
        "chapters": 66,
        "verses_per_chapter": [31, 22, 26, 6, 30, 13, 25, 22, 21, 34, 16, 6, 22, 32, 9, 14, 14, 7, 25, 6, 17, 25, 18, 23, 12, 21, 13, 29, 24, 33, 9, 20, 24, 17, 10, 22, 38, 22, 8, 31, 29, 25, 28, 28, 25, 13, 15, 22, 26, 11, 23, 15, 12, 17, 13, 12, 21, 14, 21, 22, 11, 12, 19, 12, 25, 24],
    },
    {
        "rom": "Á̤-lī-bî Cṳ",
        "han": "耶利米書",
        "eng": "Jeremiah",
        "abbr": "耶",
        "start_page": 914,
        "chapters": 52,
        "verses_per_chapter": [19, 37, 25, 31, 31, 30, 34, 22, 26, 25, 23, 17, 27, 22, 21, 21, 27, 23, 15, 18, 14, 30, 40, 10, 38, 24, 22, 17, 32, 24, 40, 44, 26, 22, 19, 32, 21, 28, 18, 16, 18, 22, 13, 30, 5, 28, 7, 47, 39, 46, 64, 34],
    },
    {
        "rom": "Á̤-lī-bî Ai-go̤ Cṳ",
        "han": "耶利米哀歌書",
        "eng": "Lamentations",
        "abbr": "哀",
        "start_page": 989,
        "chapters": 5,
        "verses_per_chapter": [22, 22, 66, 22, 22],
    },
    {
        "rom": "Î-sa̤-geh Cṳ",
        "han": "以西結書",
        "eng": "Ezekiel",
        "abbr": "結",
        "start_page": 998,
        "chapters": 48,
        "verses_per_chapter": [28, 10, 27, 17, 17, 14, 27, 18, 11, 22, 25, 28, 23, 23, 8, 63, 24, 32, 14, 49, 32, 31, 49, 27, 17, 21, 36, 26, 21, 26, 18, 32, 33, 31, 15, 38, 28, 23, 29, 49, 26, 20, 27, 31, 25, 24, 23, 35],
    },
    {
        "rom": "Dāng-î-lî Cṳ",
        "han": "但以理書",
        "eng": "Daniel",
        "abbr": "但",
        "start_page": 1063,
        "chapters": 12,
        "verses_per_chapter": [21, 49, 30, 37, 31, 28, 28, 27, 27, 21, 45, 13],
    },
    {
        "rom": "Hó̤-sa̤ Cṳ",
        "han": "何西書",
        "eng": "Hosea",
        "abbr": "何",
        "start_page": 1083,
        "chapters": 14,
        "verses_per_chapter": [11, 23, 5, 19, 15, 11, 16, 14, 17, 15, 12, 14, 16, 9],
    },
    {
        "rom": "Io̤h-cî Cṳ",
        "han": "約珥書",
        "eng": "Joel",
        "abbr": "珥",
        "start_page": 1094,
        "chapters": 3,
        "verses_per_chapter": [20, 32, 21],
    },
    {
        "rom": "A̍-mó̤-seo Cṳ",
        "han": "亞摩斯書",
        "eng": "Amos",
        "abbr": "摩",
        "start_page": 1098,
        "chapters": 9,
        "verses_per_chapter": [15, 16, 15, 13, 27, 14, 17, 14, 15],
    },
    {
        "rom": "O̤-ba-dâ̤ Cṳ",
        "han": "阿巴底書",
        "eng": "Obadiah",
        "abbr": "阿",
        "start_page": 1107,
        "chapters": 1,
        "verses_per_chapter": [21],
    },
    {
        "rom": "Io̤h-ná Cṳ",
        "han": "約拿書",
        "eng": "Jonah",
        "abbr": "拿",
        "start_page": 1109,
        "chapters": 4,
        "verses_per_chapter": [17, 10, 10, 11],
    },
    {
        "rom": "Bî-gia Cṳ",
        "han": "彌迦書",
        "eng": "Micah",
        "abbr": "彌",
        "start_page": 1112,
        "chapters": 7,
        "verses_per_chapter": [16, 13, 12, 13, 15, 16, 20],
    },
    {
        "rom": "Ná-o̤ng Cṳ",
        "han": "那翁書",
        "eng": "Nahum",
        "abbr": "翁",
        "start_page": 1119,
        "chapters": 3,
        "verses_per_chapter": [15, 13, 19],
    },
    {
        "rom": "Ha̍h-ba-go̤h Cṳ",
        "han": "哈巴谷書",
        "eng": "Habakkuk",
        "abbr": "哈",
        "start_page": 1122,
        "chapters": 3,
        "verses_per_chapter": [17, 20, 19],
    },
    {
        "rom": "Sa̤-huang-ngâ Cṳ",
        "han": "西番雅書",
        "eng": "Zephaniah",
        "abbr": "番",
        "start_page": 1126,
        "chapters": 3,
        "verses_per_chapter": [18, 15, 20],
    },
    {
        "rom": "Ha̍h-gi Cṳ",
        "han": "哈基書",
        "eng": "Haggai",
        "abbr": "基",
        "start_page": 1130,
        "chapters": 2,
        "verses_per_chapter": [15, 23],
    },
    {
        "rom": "Sah-ga-lī-a̍ Cṳ",
        "han": "撒迦利亞書",
        "eng": "Zechariah",
        "abbr": "亞",
        "start_page": 1133,
        "chapters": 14,
        "verses_per_chapter": [21, 13, 10, 14, 11, 15, 14, 23, 17, 12, 17, 14, 9, 21],
    },
    {
        "rom": "Mâ-la̍h-gi Cṳ",
        "han": "瑪拉基書",
        "eng": "Malachi",
        "abbr": "瑪",
        "start_page": 1145,
        "chapters": 4,
        "verses_per_chapter": [14, 17, 18, 6],
    },
]

# 新約27卷
NEW_TESTAMENT_BOOKS = [
    {
        "rom": "Mâ-ta̍i",
        "han": "馬太",
        "eng": "Gospel of Matthew",
        "abbr": "太",
        "start_page": 1153,
        "chapters": 28,
        "verses_per_chapter": [25, 23, 17, 25, 48, 34, 29, 34, 38, 42, 30, 50, 58, 36, 39, 28, 27, 35, 30, 34, 46, 46, 39, 51, 46, 75, 66, 20],
    },
    {
        "rom": "Mâ-kô̤",
        "han": "馬可",
        "eng": "Gospel of Mark",
        "abbr": "可",
        "start_page": 1193,
        "chapters": 16,
        "verses_per_chapter": [45, 28, 35, 41, 43, 56, 37, 38, 50, 52, 33, 44, 37, 72, 47, 20],
    },
    {
        "rom": "Lō-ga",
        "han": "路加",
        "eng": "Gospel of Luke",
        "abbr": "路",
        "start_page": 1218,
        "chapters": 24,
        "verses_per_chapter": [80, 52, 38, 44, 39, 49, 50, 56, 62, 42, 54, 59, 35, 35, 32, 31, 37, 43, 48, 47, 38, 71, 56, 53],
    },
    {
        "rom": "Io̤h-hāng",
        "han": "約翰",
        "eng": "Gospel of John",
        "abbr": "約",
        "start_page": 1261,
        "chapters": 21,
        "verses_per_chapter": [51, 25, 36, 54, 47, 71, 53, 59, 41, 42, 57, 50, 38, 31, 27, 33, 26, 40, 42, 31, 25],
    },
    {
        "rom": "Seo̍-dó Hēng-dē̤ng",
        "han": "使徒行傳",
        "eng": "Acts of the Apostles",
        "abbr": "徒",
        "start_page": 1294,
        "chapters": 28,
        "verses_per_chapter": [26, 47, 26, 37, 42, 15, 60, 40, 43, 48, 30, 25, 52, 28, 41, 40, 34, 28, 41, 38, 40, 30, 35, 27, 27, 32, 44, 31],
    },
    {
        "rom": "Bô̤-ló̤ Gio̤̍ Ló̤-mâ Náng Cṳ",
        "han": "保羅寄羅馬儂書",
        "eng": "Romans",
        "abbr": "羅",
        "start_page": 1336,
        "chapters": 16,
        "verses_per_chapter": [32, 29, 31, 25, 21, 23, 25, 39, 33, 21, 36, 21, 14, 23, 33, 27],
    },
    {
        "rom": "Bô̤-ló̤ Gio̤̍ Go̤-líng-do̤ Céng-cṳ",
        "han": "保羅寄哥林多前書",
        "eng": "1 Corinthians",
        "abbr": "林前",
        "start_page": 1355,
        "chapters": 16,
        "verses_per_chapter": [31, 16, 23, 21, 13, 20, 40, 13, 27, 33, 34, 31, 13, 40, 58, 24],
    },
    {
        "rom": "Bô̤-ló̤ Gio̤̍ Go̤-líng-do̤ Hā̤u-cṳ",
        "han": "保羅寄哥林多後書",
        "eng": "2 Corinthians",
        "abbr": "林後",
        "start_page": 1374,
        "chapters": 13,
        "verses_per_chapter": [24, 17, 18, 18, 21, 18, 16, 24, 15, 18, 33, 21, 14],
    },
    {
        "rom": "Bô̤-ló̤ Gio̤̍ Ga-la̍h-ta̍i Cṳ",
        "han": "保羅寄加拉太書",
        "eng": "Galatians",
        "abbr": "加",
        "start_page": 1386,
        "chapters": 6,
        "verses_per_chapter": [24, 21, 29, 31, 26, 18],
    },
    {
        "rom": "Bô̤-ló̤ Gio̤̍ Î-heo̍h-sê̤ Cṳ",
        "han": "保羅寄以弗所書",
        "eng": "Ephesians",
        "abbr": "弗",
        "start_page": 1392,
        "chapters": 6,
        "verses_per_chapter": [23, 22, 21, 32, 33, 24],
    },
    {
        "rom": "Bô̤-ló̤ Gio̤̍ Hi-li̍h-bî Náng Cṳ",
        "han": "保羅寄腓立比儂書",
        "eng": "Philippians",
        "abbr": "腓",
        "start_page": 1398,
        "chapters": 4,
        "verses_per_chapter": [30, 30, 21, 23],
    },
    {
        "rom": "Bô̤-ló̤ Gio̤̍ Go̤-ló̤-sa̤ Náng Cṳ",
        "han": "保羅寄歌羅西儂書",
        "eng": "Colossians",
        "abbr": "西",
        "start_page": 1403,
        "chapters": 4,
        "verses_per_chapter": [29, 23, 25, 18],
    },
    {
        "rom": "Bô̤-ló̤ Gio̤̍ Tiah-sah-ló̤-ní-gia Náng Céng-cṳ",
        "han": "保羅寄帖撒羅尼迦儂前書",
        "eng": "1 Thessalonians",
        "abbr": "帖前",
        "start_page": 1408,
        "chapters": 5,
        "verses_per_chapter": [10, 20, 13, 18, 28],
    },
    {
        "rom": "Bô̤-ló̤ Gio̤̍ Tiah-sah-ló̤-ní-gia Náng Hā̤u-cṳ",
        "han": "保羅寄帖撒羅尼迦儂後書",
        "eng": "2 Thessalonians",
        "abbr": "帖後",
        "start_page": 1412,
        "chapters": 3,
        "verses_per_chapter": [12, 17, 18],
    },
    {
        "rom": "Bô̤-ló̤ Gio̤̍ Dá̤-mó̤-ta̍i Céng-cṳ",
        "han": "保羅寄提摩太前書",
        "eng": "1 Timothy",
        "abbr": "提前",
        "start_page": 1415,
        "chapters": 6,
        "verses_per_chapter": [20, 15, 16, 16, 25, 21],
    },
    {
        "rom": "Bô̤-ló̤ Gio̤̍ Dá̤-mó̤-ta̍i Hā̤u-cṳ",
        "han": "保羅寄提摩太後書",
        "eng": "2 Timothy",
        "abbr": "提後",
        "start_page": 1420,
        "chapters": 4,
        "verses_per_chapter": [18, 26, 17, 22],
    },
    {
        "rom": "Bô̤-ló̤ Gio̤̍ Dá̤-do̤ Cṳ",
        "han": "保羅寄提多書",
        "eng": "Titus",
        "abbr": "多",
        "start_page": 1424,
        "chapters": 3,
        "verses_per_chapter": [16, 15, 15],
    },
    {
        "rom": "Bô̤-ló̤ Gio̤̍ Hi-lī-meóng Cṳ",
        "han": "保羅寄腓利們書",
        "eng": "Philemon",
        "abbr": "們",
        "start_page": 1427,
        "chapters": 1,
        "verses_per_chapter": [25],
    },
    {
        "rom": "Hi-beh-lái Náng Cṳ",
        "han": "希伯來儂書",
        "eng": "Hebrews",
        "abbr": "來",
        "start_page": 1428,
        "chapters": 13,
        "verses_per_chapter": [14, 18, 19, 16, 14, 20, 28, 13, 28, 39, 40, 29, 25],
    },
    {
        "rom": "Seo̍-dó Ngâ-go̤h Cṳ",
        "han": "使徒雅各書",
        "eng": "James",
        "abbr": "雅",
        "start_page": 1442,
        "chapters": 5,
        "verses_per_chapter": [27, 26, 18, 17, 20],
    },
    {
        "rom": "Bî-deh Céng-cṳ",
        "han": "彼得前書",
        "eng": "1 Peter",
        "abbr": "彼前",
        "start_page": 1447,
        "chapters": 5,
        "verses_per_chapter": [25, 25, 22, 19, 14],
    },
    {
        "rom": "Bî-deh Hā̤u-cṳ",
        "han": "彼得後書",
        "eng": "2 Peter",
        "abbr": "彼後",
        "start_page": 1453,
        "chapters": 3,
        "verses_per_chapter": [21, 22, 18],
    },
    {
        "rom": "Io̤h-hāng Ih Cṳ",
        "han": "約翰一書",
        "eng": "1 John",
        "abbr": "約一",
        "start_page": 1456,
        "chapters": 5,
        "verses_per_chapter": [10, 29, 24, 21, 21],
    },
    {
        "rom": "Io̤h-hāng Cī Cṳ",
        "han": "約翰二書",
        "eng": "2 John",
        "abbr": "約二",
        "start_page": 1461,
        "chapters": 1,
        "verses_per_chapter": [13],
    },
    {
        "rom": "Io̤h-hāng So̤ⁿ Cṳ",
        "han": "約翰三書",
        "eng": "3 John",
        "abbr": "約三",
        "start_page": 1462,
        "chapters": 1,
        "verses_per_chapter": [14],
    },
    {
        "rom": "Seo̍-dó Iú-dāi Cṳ",
        "han": "使徒猶大書",
        "eng": "Jude",
        "abbr": "猶",
        "start_page": 1463,
        "chapters": 1,
        "verses_per_chapter": [25],
    },
    {
        "rom": "Seo̍-dó Io̤h-hāng Be̍h-sī-le̤̍h",
        "han": "使徒約翰默示錄",
        "eng": "Revelation",
        "abbr": "默",
        "start_page": 1465,
        "chapters": 22,
        "verses_per_chapter": [20, 29, 22, 11, 14, 17, 17, 13, 21, 11, 19, 17, 18, 20, 8, 21, 18, 24, 21, 15, 27, 21],
    },
]

# 合併所有書卷
ALL_BOOKS = FOREWORD_BOOKS + OLD_TESTAMENT_BOOKS + NEW_TESTAMENT_BOOKS

# 創建書名映射字典
ROM_TO_HAN = {book["rom"]: book["han"] for book in ALL_BOOKS}
HAN_TO_ROM = {book["han"]: book["rom"] for book in ALL_BOOKS}
HAN_TO_ENG = {book["han"]: book["eng"] for book in ALL_BOOKS}

# 聖經統計基準
TOTALS = {
    "ot": {"books": 39, "chapters": 929, "verses": 23145},
    "nt": {"books": 27, "chapters": 260, "verses": 7957}
}
TOTALS["all"] = {
    "books": TOTALS["ot"]["books"] + TOTALS["nt"]["books"],
    "chapters": TOTALS["ot"]["chapters"] + TOTALS["nt"]["chapters"],
    "verses": TOTALS["ot"]["verses"] + TOTALS["nt"]["verses"],
}


def get_book_by_page(page_num: int):
    """
    根據頁碼獲取書卷資訊

    Args:
        page_num: 頁碼（數字）

    Returns:
        書卷 dict 或 None
    """
    for i, book in enumerate(ALL_BOOKS):
        start_page = book["start_page"]

        # 檢查下一卷的起始頁
        if i < len(ALL_BOOKS) - 1:
            next_start = ALL_BOOKS[i + 1]["start_page"]
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
        start_page = book["start_page"]

        if i < len(ALL_BOOKS) - 1:
            next_start = ALL_BOOKS[i + 1]["start_page"]
            if start_page <= page_num < next_start:
                return i
        else:
            if page_num >= start_page:
                return i

    return None


def get_book_by_name(name: str):
    """
    根據書名（羅馬字、漢字或英文）獲取書卷資訊

    Args:
        name: 書名

    Returns:
        書卷 dict 或 None
    """
    for book in ALL_BOOKS:
        if name in (book["rom"], book["han"], book["eng"]):
            return book
    return None


if __name__ == '__main__':
    # 測試
    test_pages = [9, 72, 1153, 1465]

    for page in test_pages:
        book = get_book_by_page(page)
        if book:
            print(f"第 {page} 頁 → {book['han']} ({book['rom']}) [{book['abbr']}]")

    # 測試章數驗證
    print("\n章數驗證：")
    ot_chapters = sum(book["chapters"] for book in OLD_TESTAMENT_BOOKS)
    nt_chapters = sum(book["chapters"] for book in NEW_TESTAMENT_BOOKS)
    print(f"舊約章數：{ot_chapters} (預期 929)")
    print(f"新約章數：{nt_chapters} (預期 260)")

    # 測試節數驗證
    print("\n節數驗證：")
    ot_verses = sum(sum(book["verses_per_chapter"]) for book in OLD_TESTAMENT_BOOKS)
    nt_verses = sum(sum(book["verses_per_chapter"]) for book in NEW_TESTAMENT_BOOKS)
    print(f"舊約節數：{ot_verses} (預期 23145)")
    print(f"新約節數：{nt_verses} (預期 7957)")
