#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""管理 data/ocr-draft.json（OCR 填入、尚未校對的節）。

  draft.py                                   # 各書卷的草稿節數與有旗標的節數
  draft.py --list Genesis 21                 # 列出某章的草稿節與旗標
  draft.py --clear Genesis 21-25             # 校對完：把這幾章從草稿清單移除
  draft.py --clear Genesis 21:5 21:7-9       # 或只移除個別節／節範圍
  draft.py --check                           # 找出清單裡在 rom.txt 沒有內容的節（過時的標記）

改完要重跑 python scripts/build_all.py，網站的標記才會更新。
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import BOOKS, DRAFT_FILE, load_draft, load_rom_verses, save_draft  # noqa: E402


def parse_targets(eng, specs):
    """'21' / '21-25' → 整章；'21:5' / '21:7-9' → 個別節。回傳 (章集合, 節集合)。"""
    chapters, verses = set(), set()
    for spec in specs:
        if ":" in spec:
            c, vs = spec.split(":")
            a, _, b = vs.partition("-")
            verses.update((int(c), v) for v in range(int(a), int(b or a) + 1))
        else:
            a, _, b = spec.partition("-")
            chapters.update(range(int(a), int(b or a) + 1))
    return chapters, verses


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", nargs=2, metavar=("BOOK", "CHAPTER"))
    ap.add_argument("--clear", nargs="+", metavar="ARG", help="英文書名，接章或節的範圍")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    draft = load_draft()
    if args.list:
        eng, ch = args.list[0], int(args.list[1])
        for (c, v), flags in sorted(draft.get(eng, {}).items()):
            if c == ch:
                print(f"{c}:{v}\t{'；'.join(flags)}")
        return
    if args.clear:
        eng, specs = args.clear[0], args.clear[1:]
        if eng not in BOOKS:
            raise SystemExit(f"未知書卷 {eng}；請用 book_info.py 的英文名，如 Genesis")
        chapters, verses = parse_targets(eng, specs)
        before = len(draft.get(eng, {}))
        draft[eng] = {k: f for k, f in draft.get(eng, {}).items() if k[0] not in chapters and k not in verses}
        save_draft(draft)
        print(f"{eng}: removed {before - len(draft[eng])} draft marks, {len(draft[eng])} left → {DRAFT_FILE}")
        return
    if args.check:
        filled = load_rom_verses(exclude_draft=False)
        stale = [(eng, k) for eng, vs in draft.items() for k in vs if k not in filled.get(eng, {})]
        for eng, (c, v) in stale:
            print(f"stale: {eng} {c}:{v}（rom.txt 沒有內容）")
        print(f"{len(stale)} stale marks")
        return
    total = 0
    for eng, vs in draft.items():
        flagged = sum(1 for f in vs.values() if f)
        chapters = sorted({c for c, _ in vs})
        print(f"{eng}: {len(vs)} draft verses ({flagged} flagged), chapters {chapters[0]}–{chapters[-1]}")
        total += len(vs)
    print(f"total {total}")


if __name__ == "__main__":
    main()
