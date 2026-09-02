#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用模型辨識已錄入經文所在的頁面，逐節與 rom.txt 正本比對，產生附掃描裁切圖的校對報告。

  proofread.py [--book Genesis] [--no-images]
  → WORK/recognized/proofread.html（含裁圖）與 proofread.md（摘要）

差異分為：A 疑似正本錯誤（正本的音節在語料中罕見、OCR 的常見）、B 兩者皆常見需判斷、
C 多半是 OCR 錯（OCR 的音節罕見）、D 標點與空格。OCR 明顯切錯節的不比對，另列。
前置：recognize.py 已產生相關頁面的 WORK/recognized/<page>.json。
"""

import argparse
import base64
import collections
import difflib
import html
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _paths import PUBLIC  # noqa: E402
from assemble import Assembler, han_syllables, load_han_verses, pages_for, syllables  # noqa: E402
from common import (BOOKS, WORK, as_printed, clusters, load_errata, load_page_map, load_rom_verses,  # noqa: E402
                    nfc, nfd, page_lines)

MARKS = {"̤": "下加兩點", "̍": "上直線", "̄": "長音符", "̂": "揚抑符", "́": "尖音符", "ⁿ": "鼻化"}


def token_at(cl, i):
    """叢集列表中第 i 個叢集所屬的音節（以空格、連字號、標點為界）。"""
    def is_sep(c):
        return c[0] in " -" or not (c[0].isalnum() or c[0] == "ⁿ")
    if i >= len(cl) or is_sep(cl[i]):
        return ""
    a = i
    while a > 0 and not is_sep(cl[a - 1]):
        a -= 1
    b = i
    while b < len(cl) and not is_sep(cl[b]):
        b += 1
    return nfc("".join(cl[a:b])).lower()


def diff_verse(ocr, gt):
    """回傳差異列表 [(ocr 片段, 正本片段, 正本叢集起訖, OCR 叢集起訖, 類別)]。"""
    ca, ba = clusters(ocr)
    cb, bb = clusters(gt)
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ba, bb, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                x, y = ca[i1 + k], cb[j1 + k]
                if x != y:
                    out.append((x, y, (j1 + k, j1 + k + 1), (i1 + k, i1 + k + 1), "符號"))
            continue
        a, b = "".join(ca[i1:i2]), "".join(cb[j1:j2])
        if all(c in " -" for c in a + b):
            kind = "空格"
        elif all(not (c.isalnum() or c == "ⁿ") and not unicodedata.combining(c) for c in a + b):
            kind = "標點"
        else:
            kind = "字母"
        out.append((a, b, (j1, j2), (i1, i2), kind))
    return out


def classify(item, cl_ocr, cl_gt, freq):
    a, b, (j1, j2), (i1, i2), kind = item
    if kind in ("標點", "空格"):
        return "D"
    if len(a) >= 8 or len(b) >= 8:
        return "S"  # 整段多出或缺少：切節或漏行的問題，不是打字錯
    tg = token_at(cl_gt, j1 if j1 < len(cl_gt) else len(cl_gt) - 1)
    to = token_at(cl_ocr, i1 if i1 < len(cl_ocr) else len(cl_ocr) - 1)
    fg, fo = freq.get(tg, 0), freq.get(to, 0)
    if fo <= 1:
        return "C"
    if fg <= 1:
        return "A"
    return "B"


def mark_text(cl, spans, tag="mark"):
    """把差異處用 <mark> 標出。"""
    spans = sorted(spans)
    out, pos = [], 0
    for a, b in spans:
        a, b = max(a, pos), max(b, a)
        out.append(html.escape(nfc("".join(cl[pos:a]))))
        out.append(f"<{tag}>{html.escape(nfc(''.join(cl[a:b])))}</{tag}>")
        pos = b
    out.append(html.escape(nfc("".join(cl[pos:]))))
    return "".join(out)


def crop_lines(page_cache, refs, width=700):
    """把一節用到的行裁下來疊成一張圖，回傳 PNG 的 base64。"""
    from PIL import Image
    from common import erase_rule, tight_crop
    rows = []
    for page, line_no in refs:
        if page not in page_cache:
            im = Image.open(PUBLIC / "images" / f"{page}.webp").convert("L")
            boxes, rx = page_lines(page, im)
            rec = json.load(open(WORK / "recognized" / f"{page}.json", encoding="utf-8"))
            by_idx = {tuple(b["idx"]): b for b in boxes}
            page_cache[page] = (erase_rule(im, rx), [by_idx.get(tuple(ln["idx"])) for ln in rec["lines"]])
        im, boxes = page_cache[page]
        b = boxes[line_no] if line_no < len(boxes) else None
        if not b:
            continue
        crop = tight_crop(im, b["x0"], b["y0"] - 8, b["x1"], b["y1"] + 8)
        crop = crop.resize((width, max(1, int(crop.height * width / crop.width))))
        rows.append(crop)
    if not rows:
        return ""
    canvas = Image.new("L", (width, sum(r.height + 4 for r in rows)), 200)
    y = 0
    for r in rows:
        canvas.paste(r, (0, y))
        y += r.height + 4
    buf = io.BytesIO()
    canvas.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", help="只處理這卷（英文書名）")
    ap.add_argument("--no-images", action="store_true")
    ap.add_argument("--rom", help="正本來源；預設用 git HEAD 的 data/rom.txt，避免比到 OCR 自己填進去的經文")
    args = ap.parse_args()
    pm, pages = load_page_map()
    if args.rom:
        filled = load_rom_verses(args.rom)
    else:
        import subprocess, tempfile
        from _paths import ROOT
        txt = subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:data/rom.txt"], capture_output=True, text=True, check=True).stdout
        tmp = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
        tmp.write(txt)
        tmp.close()
        filled = load_rom_verses(tmp.name)
    errata = load_errata()
    freq = collections.Counter(s.lower() for verses in filled.values() for t in verses.values() for s in syllables(t))
    rows, skipped, missing_pages = [], [], []
    stats = collections.Counter()
    page_cache = {}
    for eng, verses in filled.items():
        if args.book and eng != args.book:
            continue
        chapters = sorted({c for c, _ in verses})
        plist = pages_for(pm, pages, eng, chapters)
        plist = [p for p in plist if (WORK / "recognized" / f"{p}.json").exists() or missing_pages.append((eng, p))]
        if not plist:
            continue
        han = load_han_verses(eng)
        asm = Assembler(eng, {k: han_syllables(v) for k, v in han.items()})
        for p in plist:
            rec = json.load(open(WORK / "recognized" / f"{p}.json", encoding="utf-8"))
            i = pages.index(p)
            nxt = pm[pages[i + 1]] if i + 1 < len(pages) else None
            next_start = (nxt["chapter"], nxt["verse"]) if nxt and nxt["book_english"] == eng else (10**6, 1)
            asm.feed_page(p, rec, (pm[p]["chapter"], pm[p]["verse"]), next_start)
        for key in sorted(verses):
            ocr = asm.verse_text(key)
            gt = verses[key]
            printed = as_printed(eng, key, gt, errata)  # 勘誤表列出的地方：OCR 讀成印法或規範寫法都算對
            if printed != gt and ocr and len(diff_verse(ocr, printed)) < len(diff_verse(ocr, gt)):
                gt = printed
            stats["verses"] += 1
            if not ocr or abs(len(nfd(ocr)) - len(nfd(gt))) > max(6, 0.25 * len(nfd(gt))):
                skipped.append((eng, key, len(nfd(ocr)), len(nfd(gt))))
                stats["skipped"] += 1
                continue
            items = diff_verse(ocr, gt)
            if not items:
                stats["identical"] += 1
                continue
            cl_o, _ = clusters(ocr)
            cl_g, _ = clusters(gt)
            cats = [classify(it, cl_o, cl_g, freq) for it in items]
            for c in cats:
                stats["item_" + c] += 1
            if "S" in cats:
                skipped.append((eng, key, len(nfd(ocr)), len(nfd(gt))))
                stats["skipped"] += 1
                continue
            best = min(cats)  # A < B < C < D
            stats["verse_" + best] += 1
            rows.append({"book": eng, "key": key, "cat": best, "items": items, "cats": cats, "ocr": ocr, "gt": gt,
                         "refs": asm.lines.get(key, []), "cl_o": cl_o, "cl_g": cl_g})
    rows.sort(key=lambda r: (r["cat"], r["book"], r["key"]))
    # ---------- HTML ----------
    parts = ["<!doctype html><meta charset='utf-8'><title>羅馬字正本校對</title>",
             "<style>body{font-family:'DejaVu Sans',sans-serif;max-width:1100px;margin:auto;padding:1em}"
             "table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:6px;vertical-align:top}"
             "mark{background:#ffd54f}img{max-width:100%;border:1px solid #999}.cat{font-weight:bold}"
             "tr.A td:first-child{border-left:6px solid #d32f2f}tr.B td:first-child{border-left:6px solid #f9a825}"
             "tr.C td:first-child{border-left:6px solid #9e9e9e}tr.D td:first-child{border-left:6px solid #90caf9}</style>",
             "<h1>羅馬字正本校對報告</h1>",
             f"<p>比對 {stats['verses']} 節：完全一致 {stats['identical']}，有差異 {len(rows)}，OCR 切節失敗未比對 {stats['skipped']}。</p>",
             "<p><b>A</b> 疑似正本打錯（正本的音節在全部正本中只出現這一次，OCR 的寫法常見）："
             f"{stats['verse_A']} 節；<b>B</b> 兩種寫法都常見，需看圖判斷：{stats['verse_B']} 節；"
             f"<b>C</b> 多半是 OCR 錯：{stats['verse_C']} 節；<b>D</b> 只差標點或空格：{stats['verse_D']} 節。</p>",
             "<p>每列標出差異處：上為正本（rom.txt），下為 OCR。圖是該節用到的掃描行。</p>",
             "<table><tr><th>類</th><th>章節</th><th>正本 ／ OCR</th><th>差異（OCR → 正本）</th><th>掃描</th></tr>"]
    for r in rows:
        eng, (c, v) = r["book"], r["key"]
        diffs = "<br>".join(f"[{cat}] 「{html.escape(nfc(a))}」→「{html.escape(nfc(b))}」"
                            for (a, b, _, _, kind), cat in zip(r["items"], r["cats"]))
        img = ""
        if not args.no_images and r["cat"] in ("A", "B") and r["refs"]:
            data = crop_lines(page_cache, r["refs"])
            if data:
                img = f"<img src='data:image/png;base64,{data}'>"
        parts.append(f"<tr class='{r['cat']}'><td class='cat'>{r['cat']}</td><td>{BOOKS[eng]['han']}<br>{c}:{v}</td>"
                     f"<td>{mark_text(r['cl_g'], [it[2] for it in r['items']])}<br><span style='color:#555'>"
                     f"{mark_text(r['cl_o'], [it[3] for it in r['items']])}</span></td><td>{diffs}</td><td>{img}</td></tr>")
    parts.append("</table>")
    if skipped:
        parts.append("<h2>OCR 切節失敗，未比對</h2><p>" + "，".join(f"{BOOKS[e]['han']} {c}:{v}" for e, (c, v), _, _ in skipped) + "</p>")
    if missing_pages:
        parts.append("<h2>尚未辨識的頁面</h2><p>" + "，".join(f"{e} {p}" for e, p in missing_pages) + "</p>")
    out = WORK / "recognized" / (f"proofread_{args.book}.html" if args.book else "proofread.html")
    out.write_text("\n".join(parts), encoding="utf-8")
    md = [f"# 羅馬字正本校對摘要", "", f"比對 {stats['verses']} 節：完全一致 {stats['identical']}，有差異 {len(rows)}，未比對 {stats['skipped']}。", "",
          f"- A 疑似正本打錯：{stats['verse_A']} 節（{stats['item_A']} 處）", f"- B 需看圖判斷：{stats['verse_B']} 節（{stats['item_B']} 處）",
          f"- C 多半是 OCR 錯：{stats['verse_C']} 節（{stats['item_C']} 處）", f"- D 標點空格：{stats['verse_D']} 節（{stats['item_D']} 處）", "",
          "| 類 | 章節 | OCR → 正本 |", "|---|---|---|"]
    for r in rows:
        if r["cat"] in ("A", "B"):
            eng, (c, v) = r["book"], r["key"]
            md.append(f"| {r['cat']} | {BOOKS[eng]['han']} {c}:{v} | " + "；".join(f"「{nfc(a)}」→「{nfc(b)}」" for a, b, _, _, _ in r["items"]) + " |")
    out.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{out}  verses={stats['verses']} identical={stats['identical']} A={stats['verse_A']} B={stats['verse_B']} C={stats['verse_C']} D={stats['verse_D']} skipped={stats['skipped']} missing_pages={len(missing_pages)}")


if __name__ == "__main__":
    main()
