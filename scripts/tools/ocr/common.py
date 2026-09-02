#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OCR 工具共用模組：路徑、平話字文字處理、對齊演算法、頁面與經節對應。

行圖與模型都放在 repo 外，位置可用環境變數覆寫：
  HINGHUA_OCR_LINES  行圖目錄（<page>/<page>_line_NNNN.png）
  HINGHUA_OCR_SEG    kraken 版面切割 JSON（<page>.json，與行圖同序）
  HINGHUA_OCR_WORK   工作目錄（標籤、資料集、模型、辨識結果）
"""

import json
import os
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _paths import DATA, PUBLIC  # noqa: E402
import book_info as B  # noqa: E402

LINE_IMAGES = Path(os.environ.get("HINGHUA_OCR_LINES", "/home/siniong/projects/buc_ocr/output/line_images"))
SEG_JSON = Path(os.environ.get("HINGHUA_OCR_SEG", "/home/siniong/projects/buc_ocr/output/json_results"))
WORK = Path(os.environ.get("HINGHUA_OCR_WORK", "/home/siniong/projects/hinghua-ocr-work"))

BOOKS = {b["eng"]: b for b in B.OLD_TESTAMENT_BOOKS + B.NEW_TESTAMENT_BOOKS}
ROM_TO_ENG = {unicodedata.normalize("NFC", b["rom"]): b["eng"] for b in BOOKS.values()}
GAP = "§"  # 頁面文字中「此處經文尚未錄入」的哨兵


# ---------- 文字 ----------

def nfd(s):
    return unicodedata.normalize("NFD", s)


def nfc(s):
    return unicodedata.normalize("NFC", s)


def clusters(text):
    """把 NFD 文字切成「基底字元 + 後續組合符號」叢集。

    回傳 (叢集列表, 去符號字串)。去符號字串裡 ⁿ 視為 n，供對齊與比對用。
    """
    out = []
    for ch in nfd(text):
        if unicodedata.combining(ch) and out:
            out[-1] += ch
        else:
            out.append(ch)
    base_str = "".join("n" if c[0] == "ⁿ" else c[0] for c in out)
    return out, base_str


def base(text):
    return clusters(text)[1]


def lev(a, b):
    """一般 Levenshtein 距離（短字串用）。"""
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def cer(pairs):
    """[(pred, gt)] → (含符號 CER, 去符號 CER)。"""
    e = tot = eb = totb = 0
    for pred, gt in pairs:
        e += lev(nfd(pred or ""), nfd(gt))
        tot += len(nfd(gt))
        eb += lev(base(pred or ""), base(gt))
        totb += len(base(gt))
    return e / max(tot, 1), eb / max(totb, 1)


# ---------- 對齊 ----------

def _sg_end(hay, needle, anchored=False):
    """needle 對 hay 任一子字串的最小編輯距離（向量化 DP）。

    anchored=True 時子字串必須從 hay 開頭開始。回傳 (距離, 子字串結尾索引)。
    """
    H = np.frombuffer(hay.encode("utf-32-le"), dtype=np.uint32)
    n = len(H)
    idx = np.arange(n + 1)
    prev = idx.astype(np.int32).copy() if anchored else np.zeros(n + 1, dtype=np.int32)
    for ch in needle:
        sub = prev[:-1] + (H != ord(ch))
        dele = prev[1:] + 1
        full = np.concatenate(([prev[0] + 1], np.minimum(sub, dele)))
        prev = np.minimum.accumulate(full - idx) + idx  # 插入：cur[j] = min(cur[j-1]+1, …)
    t = int(np.argmin(prev))
    return int(prev[t]), t


def semi_global(hay, needle):
    """回傳 (距離, 起點, 終點)：needle 與 hay[起點:終點] 的編輯距離最小。"""
    d, t = _sg_end(hay, needle)
    _, t2 = _sg_end(hay[:t][::-1], needle[::-1], anchored=True)
    return d, t - t2, t


def snap(page_base, s, t, line_base, window=3):
    """把對齊區間吸附到詞界（空格或連字號）；行尾若斷在連字號前則把連字號納入。"""
    n = len(page_base)

    def is_start(k):
        return k == 0 or page_base[k - 1] in " -" + GAP

    def is_end(k):
        return k == n or page_base[k] in " -" + GAP or page_base[k - 1] == "-"

    starts = [k for k in range(max(0, s - window), min(n, s + window) + 1) if is_start(k)] or [s]
    ends = [k for k in range(max(0, t - window), min(n, t + window) + 1) if is_end(k)] or [t]
    best = None
    for a in starts:
        for b in ends:
            if b <= a:
                continue
            key = (lev(page_base[a:b], line_base), abs(a - s) + abs(b - t))
            if best is None or key < best[0]:
                best = (key, a, b)
    if best is None:
        return s, t
    _, a, b = best
    if b < n and page_base[b] == "-":
        b += 1
    return a, b


# ---------- 頁面與經節 ----------

def load_page_map():
    pm = json.load(open(DATA / "page-ocr-results.json", encoding="utf-8"))
    return pm, sorted(pm)


def load_rom_verses(path=None):
    """rom.txt → {英文書名: {(章, 節): 經文}}，只收有內容的節。"""
    filled = {}
    book = ch = None
    key = None
    for line in open(path or DATA / "rom.txt", encoding="utf-8"):
        if line.startswith("# "):
            book = ROM_TO_ENG.get(nfc(line[2:].strip()))
            key = None
        elif line.startswith("## "):
            ch = int(line[3:])
            key = None
        elif line.startswith("###") or not line.strip():
            key = None
        else:
            m = re.match(r"^(\d+)\s*(.*)", line)
            if m and book:
                key = (ch, int(m.group(1)))
                if m.group(2).strip():
                    filled.setdefault(book, {})[key] = m.group(2).strip()
                else:
                    key = None
            elif key and book:  # 詩歌體的續行
                filled[book][key] += " " + line.strip()
    return filled


def verses_on_page(pm, pages, p):
    """回傳 (英文書名, [(章, 節), …])：該頁自起始經節到下一頁起始經節之前。"""
    i = pages.index(p)
    e = pm[p]["book_english"]
    if e not in BOOKS:
        return e, []
    nxt = pm[pages[i + 1]] if i + 1 < len(pages) else None
    end = (nxt["chapter"], nxt["verse"]) if nxt and nxt["book_english"] == e else (10**6, 1)
    vpc = BOOKS[e]["verses_per_chapter"]
    out = []
    c, v = pm[p]["chapter"], pm[p]["verse"]
    while (c, v) < end and c <= len(vpc):
        out.append((c, v))
        v += 1
        if v > vpc[c - 1]:
            c, v = c + 1, 1
    return e, out


def prev_verse(eng, c, v):
    """(章, 節) 的前一節；第一章第一節回傳 None。"""
    if v > 1:
        return (c, v - 1)
    if c > 1:
        return (c - 1, BOOKS[eng]["verses_per_chapter"][c - 2])
    return None


def page_text_for(pm, pages, p, filled):
    """整頁文字。頁面對應表記的是該頁第一個「節號」，頁首通常還有前一節的尾巴，故把前一節一併納入。"""
    eng, vs = verses_on_page(pm, pages, p)
    if not vs:
        return eng, vs, ""
    pv = prev_verse(eng, *vs[0])
    full = ([pv] if pv else []) + vs
    return eng, vs, page_text(eng, full, filled)


def chapter_heading(c):
    return f"Dā̤ {c} Ca̤uⁿ."


def page_text(eng, verses, filled):
    """依印刷慣例組出整頁文字：章標題、節號（第 1 節不印），缺文處放哨兵。"""
    parts = []
    for c, v in verses:
        if v == 1:
            parts.append(chapter_heading(c))
        text = filled.get(eng, {}).get((c, v))
        if text is None:
            if parts and parts[-1] != GAP:
                parts.append(GAP)
            continue
        parts.append(text if v == 1 else f"{v} {text}")
    return " ".join(parts)


def line_order(page):
    """讀 kraken 切割 JSON，回傳行索引依「欄、由上到下」排序後的列表，以及每行的欄與 y。"""
    d = json.load(open(SEG_JSON / f"{page}.json", encoding="utf-8"))
    info = []
    xs = []
    for i, ln in enumerate(d["lines"]):
        pts = ln["boundary"] or ln["baseline"]
        x0, x1 = min(x for x, _ in pts), max(x for x, _ in pts)
        y = sum(y for _, y in ln["baseline"]) / len(ln["baseline"])
        info.append([i, (x0 + x1) / 2, y, x1 - x0])
        xs.append((x0 + x1) / 2)
    mid = (min(xs) + max(xs)) / 2 if xs else 0
    for row in info:
        row.append(0 if row[1] < mid else 1)
    info.sort(key=lambda r: (r[4], r[2]))
    return [{"idx": r[0], "col": r[4], "y": r[2], "xmid": r[1], "width": r[3]} for r in info]


# ---------- 整頁的行框 ----------

RULE_MARGIN = 2  # 行框與欄溝中心保持的距離（像素）


def column_rule(im):
    """找出雙欄之間的欄溝中心 x：對頁面中段各直欄的黑點數做移動平均後取最小值。"""
    ink = (np.asarray(im.convert("L")) < 128).sum(axis=0).astype(np.float64)
    w = len(ink)
    lo, hi = int(w * 0.35), int(w * 0.65)
    k = 41
    smooth = np.convolve(ink[lo - k:hi + k], np.ones(k) / k, mode="same")[k:-k]
    return lo + int(np.argmin(smooth))


def erase_rule(im, rx, band=150, halfwidth=10):
    """把欄線塗白。欄線可能略斜或斷續，故分段偵測：每段在欄溝附近找墨量超過段高三成的直欄。"""
    arr = np.array(im.convert("L"))
    h, w = arr.shape
    lo, hi = max(0, rx - 40), min(w, rx + 41)
    for y0 in range(0, h, band):
        seg = arr[y0:y0 + band, lo:hi] < 128
        ink = seg.sum(axis=0)
        if ink.max() > 0.3 * seg.shape[0]:
            x = lo + int(np.argmax(ink))
            arr[y0:y0 + band, max(0, x - halfwidth):x + halfwidth + 1] = 255
    return Image.fromarray(arr)


def tight_crop(im, x0, y0, x1, y1, margin=12, min_ink=3):
    """在框內找墨跡的左右範圍，貼著墨跡裁切（訓練用的行圖就是這樣切的）。"""
    x0, y0, x1, y1 = int(x0), int(max(0, y0)), int(min(im.width, x1)), int(min(im.height, y1))
    arr = np.asarray(im.crop((x0, y0, x1, y1))) < 128
    cols = np.where(arr.sum(axis=0) >= min_ink)[0]
    if len(cols) == 0:
        return im.crop((x0, y0, x1, y1))
    left = max(x0, x0 + int(cols[0]) - margin)
    right = min(x1, x0 + int(cols[-1]) + margin + 1)
    return im.crop((left, y0, right, y1))


def page_lines(page, im=None):
    """讀切割 JSON，把被欄線切碎的行框合併回整行。

    前次切割先以亮度切欄再各自切行，欄線附近的最後一個詞常被切成獨立碎片，
    也常出現只含欄線的垃圾框。這裡把框限制在欄線的同一側、丟掉太窄的框，
    再把同欄同基線的框取聯集。回傳 (依欄與 y 排序的框列表, 欄線 x)。
    每個框：idx（原始行索引列表）、col、x0、x1、y0、y1、y（基線）、dropcap、header、footer。
    """
    seg = json.load(open(SEG_JSON / f"{page}.json", encoding="utf-8"))["lines"]
    im = im or Image.open(PUBLIC / "images" / f"{page}.webp")
    rx = column_rule(im)
    boxes = []
    for i, ln in enumerate(seg):
        pts = ln["boundary"] or ln["baseline"]
        x0, x1 = min(x for x, _ in pts), max(x for x, _ in pts)
        y0, y1 = min(y for _, y in pts), max(y for _, y in pts)
        yb = sum(y for _, y in ln["baseline"]) / len(ln["baseline"])
        col = 0 if (x0 + x1) / 2 < rx else 1
        if x1 - x0 < 50:
            continue
        # 前次切欄的位置不一定貼著欄線，行框一律拉到欄溝中心，讓裁切涵蓋整行（欄線另外塗白）
        if col == 0:
            x1 = rx - RULE_MARGIN
        else:
            x0 = rx + RULE_MARGIN
        boxes.append({"idx": [i], "col": col, "x0": x0, "x1": x1, "y0": y0, "y1": y1, "y": yb, "dropcap": False})
    heights = sorted(b["y1"] - b["y0"] for b in boxes)
    med_h = heights[len(heights) // 2] if heights else 100
    kept = []
    for b in boxes:
        tall = b["y1"] - b["y0"] > 1.6 * med_h
        if tall and 0.5 * med_h <= b["x1"] - b["x0"] < 3 * med_h:
            b["dropcap"] = True  # 章首放大字母：獨立成框，排在該行之前
            b["y"] = b["y0"] + med_h * 0.5
        elif tall:
            continue  # 太高又不像放大字母：欄線碎片、館藏章之類的垃圾
        kept.append(b)
    boxes = kept
    # 切割多邊形的高度有時只涵蓋半行：以基線為準，把每個框至少撐到本頁典型的行高
    normal = [b for b in boxes if not b["dropcap"]]
    if len(normal) >= 5:
        above = sorted(b["y"] - b["y0"] for b in normal)[len(normal) // 2]
        below = sorted(b["y1"] - b["y"] for b in normal)[len(normal) // 2]
        for b in normal:
            b["y0"] = min(b["y0"], b["y"] - above)
            b["y1"] = max(b["y1"], b["y"] + below)
    # 切割多邊形常漏掉行首的上標節號與行尾的短詞：每欄的行框一律拉到該欄的左右邊界
    for col in (0, 1):
        wide = [b for b in boxes if b["col"] == col and not b["dropcap"] and b["x1"] - b["x0"] > 8 * med_h]
        if len(wide) < 3:
            continue
        # 外緣取整欄最寬的行再加一點餘裕；用百分位數會把最長幾行的行尾字元切掉
        left = min(b["x0"] for b in wide) - 6
        right = max(b["x1"] for b in wide) + 6
        for b in boxes:
            if b["col"] == col and not b["dropcap"]:
                b["x0"], b["x1"] = max(0, min(b["x0"], left)), max(b["x1"], right)
    boxes.sort(key=lambda b: (b["col"], b["y"], b["x0"]))
    merged = []
    for b in boxes:
        m = merged[-1] if merged else None
        if m and not b["dropcap"] and not m["dropcap"] and m["col"] == b["col"] and abs(m["y"] - b["y"]) <= 40:
            if b["x1"] - b["x0"] > m["x1"] - m["x0"]:
                m["y"], m["y0"], m["y1"] = b["y"], b["y0"], b["y1"]  # 垂直範圍以最寬的那塊為準
            m["x0"], m["x1"] = min(m["x0"], b["x0"]), max(m["x1"], b["x1"])
            m["idx"] += b["idx"]
        else:
            merged.append(dict(b))
    # 頁眉與頁碼：每欄最上／最下一行若與相鄰行的距離明顯大於行距，就是頁眉／頁碼
    for col in (0, 1):
        rows = [b for b in merged if b["col"] == col and not b["dropcap"]]
        if len(rows) < 4:
            continue
        gaps = sorted(rows[i + 1]["y"] - rows[i]["y"] for i in range(len(rows) - 1))
        pitch = gaps[len(gaps) // 2]
        if rows[1]["y"] - rows[0]["y"] > 1.6 * pitch:
            rows[0]["header"] = True
        if rows[-1]["y"] - rows[-2]["y"] > 1.3 * pitch:
            rows[-1]["footer"] = True
    for b in merged:
        b.setdefault("header", False)
        b.setdefault("footer", False)
    return merged, rx
