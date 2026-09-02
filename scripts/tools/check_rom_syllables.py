#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""列出 rom.txt 裡不合法的音節：多個調符、多個下加兩點、調符位置不對、韻母不存在、漏了連字號等。

  python scripts/tools/check_rom_syllables.py            # 人工正本（不含 OCR 草稿）
  python scripts/tools/check_rom_syllables.py --draft    # 只看 OCR 草稿
  python scripts/tools/check_rom_syllables.py --html out.html   # 附 OCR 讀法與掃描裁圖的校對頁（需已跑過 recognize.py）

合法音節 = data/hinghua-finals.txt 的「韻母＋聲調」× 聲母。正本裡的異常多半是打字錯誤，
但少數可能是原書就印錯，請對照掃描頁。
"""

import collections
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent / "ocr"))
from _paths import DATA  # noqa: E402
from common import BOOKS, load_draft, load_rom_verses, nfc, nfd  # noqa: E402

INITIALS = ["", "b", "p", "m", "d", "t", "n", "l", "g", "k", "ng", "h", "c", "ch", "s"]
TONE_MARKS = {"́", "̂", "̍", "̄"}


def valid_syllables():
    finals = [nfc(l.strip()) for l in open(DATA / "hinghua-finals.txt", encoding="utf-8")
              if l.strip() and not l.startswith("#")]
    return {nfc(i + f) for i in INITIALS for f in finals}


def syllables(text):
    cleaned = re.sub(r"[^\w\s\-̀-ͯ*]", " ", text)
    return [s for s in re.split(r"[\s\-]+", cleaned) if s and not s.isdigit()]


def norm(s):
    return nfc(nfd(s).lower().rstrip("*"))


def why(s, valid):
    d = nfd(norm(s))
    if sum(c in TONE_MARKS for c in d) > 1:
        return "多個調符"
    if d.count("̤") > 1:
        return "多個下加兩點"
    stripped = nfc("".join(c for c in d if c not in TONE_MARKS))
    if stripped in valid:
        return "調符位置或種類不對"
    if any(c.isdigit() for c in d):
        return "含數字"
    return "韻母不存在或漏連字號"


def html_report(found, verses, out_path):
    """每個可疑音節一列：正本（標出音節）、OCR 對同一節的讀法、掃描裁圖。"""
    import html as H
    import json
    from assemble import Assembler, han_syllables, load_han_verses, pages_for
    from common import WORK, load_page_map
    from proofread import crop_lines
    pm, pages = load_page_map()
    asms, cache = {}, {}
    rows = []
    for s, refs in found.items():
        for eng, key in refs:
            if eng not in asms:
                han = load_han_verses(eng)
                asm = Assembler(eng, {k: han_syllables(v) for k, v in han.items()})
                for p in pages_for(pm, pages, eng, sorted({c for c, _ in verses[eng]})):
                    f = WORK / "recognized" / f"{p}.json"
                    if not f.exists():
                        continue
                    i = pages.index(p)
                    nxt = pm[pages[i + 1]] if i + 1 < len(pages) else None
                    ns = (nxt["chapter"], nxt["verse"]) if nxt and nxt["book_english"] == eng else (10**6, 1)
                    asm.feed_page(p, json.load(open(f, encoding="utf-8")), (pm[p]["chapter"], pm[p]["verse"]), ns)
                asms[eng] = asm
            asm = asms[eng]
            gt = verses[eng][key]
            marked = H.escape(gt).replace(H.escape(s), f"<mark>{H.escape(s)}</mark>")
            img = crop_lines(cache, asm.lines.get(key, []))
            rows.append(f"<tr><td>{BOOKS[eng]['han']}<br>{key[0]}:{key[1]}</td><td><b>{H.escape(s)}</b><br>{why(s, valid_syllables())}</td>"
                        f"<td>{marked}<br><span style='color:#555'>{H.escape(asm.verse_text(key))}</span></td>"
                        f"<td>{'<img src=' + chr(39) + 'data:image/png;base64,' + img + chr(39) + '>' if img else ''}</td></tr>")
    doc = ["<!doctype html><meta charset='utf-8'><title>可疑音節</title>",
           "<style>body{font-family:'DejaVu Sans',sans-serif;max-width:1100px;margin:auto;padding:1em}"
           "table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:6px;vertical-align:top}"
           "mark{background:#ffd54f}img{max-width:100%;border:1px solid #999}</style>",
           f"<h1>rom.txt 可疑音節（{len(rows)} 處）</h1><p>上為正本（標出音節），下為 OCR 對同一節的讀法；圖是該節用到的掃描行。</p>",
           "<table><tr><th>章節</th><th>音節</th><th>正本 ／ OCR</th><th>掃描</th></tr>", *rows, "</table>"]
    Path(out_path).write_text("\n".join(doc), encoding="utf-8")
    print(f"→ {out_path}")


def main():
    valid = valid_syllables()
    if "--draft" in sys.argv:
        draft = load_draft()
        allv = load_rom_verses(exclude_draft=False)
        verses = {eng: {k: v for k, v in allv.get(eng, {}).items() if k in draft.get(eng, {})} for eng in draft}
    else:
        verses = load_rom_verses()
    found = collections.defaultdict(list)
    total = 0
    for eng, vs in verses.items():
        for (c, v), text in sorted(vs.items()):
            for s in syllables(text):
                total += 1
                if norm(s) not in valid:
                    found[s].append((eng, (c, v)))
    n = sum(len(r) for r in found.values())
    print(f"音節 {total}，不合法 {n}（{n / max(total, 1):.2%}）\n")
    print("| 音節 | 判斷 | 次數 | 位置 |\n|---|---|---|---|")
    for s, refs in sorted(found.items(), key=lambda x: (-len(x[1]), x[0])):
        where = [f"{BOOKS[e]['han']} {c}:{v}" for e, (c, v) in refs]
        print(f"| {s} | {why(s, valid)} | {len(refs)} | {'、'.join(where[:6])}{'…' if len(refs) > 6 else ''} |")
    if "--html" in sys.argv:
        sys.path.insert(0, str(Path(__file__).resolve().parent / "ocr"))
        html_report(found, verses, sys.argv[sys.argv.index("--html") + 1])


if __name__ == "__main__":
    main()
