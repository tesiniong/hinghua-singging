#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""列出 rom.txt 裡不合法的音節：多個調符、多個下加兩點、調符位置不對、韻母不存在、漏了連字號等。

  python scripts/tools/check_rom_syllables.py            # 人工正本（不含 OCR 草稿）
  python scripts/tools/check_rom_syllables.py --draft    # 只看 OCR 草稿

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
                    found[s].append(f"{BOOKS[eng]['han']} {c}:{v}")
    n = sum(len(r) for r in found.values())
    print(f"音節 {total}，不合法 {n}（{n / max(total, 1):.2%}）\n")
    print("| 音節 | 判斷 | 次數 | 位置 |\n|---|---|---|---|")
    for s, refs in sorted(found.items(), key=lambda x: (-len(x[1]), x[0])):
        print(f"| {s} | {why(s, valid)} | {len(refs)} | {'、'.join(refs[:6])}{'…' if len(refs) > 6 else ''} |")


if __name__ == "__main__":
    main()
