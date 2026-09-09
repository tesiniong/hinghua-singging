#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""從和合本（eBible.org 的 cmn-cu89t USFM，公有領域）算出每節的漢字數，寫成 data/cuv-verse-lengths.json。

沒有漢字版的書卷切節時沒有長度線索；和合本每節字數乘上約 0.75 再加 5 可以預測羅馬字音節數
（1,511 節正本上平均誤差 3.9 音節、九成在 8 音節內），assemble.py 拿它當軟性線索。

  curl -LO https://ebible.org/Scriptures/cmn-cu89t_usfm.zip && unzip cmn-cu89t_usfm.zip -d cuv
  python scripts/tools/ocr/cuv_lengths.py cuv/          # → data/cuv-verse-lengths.json

輸出格式：{英文書名: {章: [第 1 節字數, 第 2 節字數, …]}}；只數漢字，標點不算。
"""

import glob
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import book_info as B  # noqa: E402
from common import DATA  # noqa: E402

USFM_CODES = ("GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH EST JOB PSA PRO ECC SNG ISA JER LAM "
              "EZK DAN HOS JOL AMO OBA JON MIC NAM HAB ZEP HAG ZEC MAL MAT MRK LUK JHN ACT ROM 1CO 2CO GAL EPH PHP "
              "COL 1TH 2TH 1TI 2TI TIT PHM HEB JAS 1PE 2PE 1JN 2JN 3JN JUD REV").split()
OUT = DATA / "cuv-verse-lengths.json"


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "cuv")
    books = B.OLD_TESTAMENT_BOOKS + B.NEW_TESTAMENT_BOOKS
    assert len(books) == len(USFM_CODES) == 66
    out = {}
    for code, book in zip(USFM_CODES, books):
        files = glob.glob(str(src / f"*{code}*.usfm"))
        if not files:
            raise SystemExit(f"找不到 {code} 的 USFM 檔")
        counts, ch, key = {}, None, None
        for line in open(files[0], encoding="utf-8"):
            m = re.match(r"\\c (\d+)", line)
            if m:
                ch, key = int(m.group(1)), None
                continue
            m = re.match(r"\\v (\d+)[a-z]?(?:-(\d+)[a-z]?)?\s*(.*)", line)
            if m and ch:
                key, text = (ch, int(m.group(1))), m.group(3)
                span = int(m.group(2) or m.group(1)) - int(m.group(1)) + 1  # \v 3-4：合併的節，字數平分
                if span > 1:
                    key = (ch, int(m.group(1)), span)
            elif key and re.match(r"\\(q\d?|p|m|b|pi\d?|li\d?|nb)?\b", line) and not re.match(r"\\[a-z]+\d?", line.split(" ")[0][1:]):
                text = line  # 詩體（\q1）與段落（\p）續行屬於目前這節；\s1 \r \d 等標題不算
            elif key and not line.startswith("\\"):
                text = line
            else:
                continue
            text = re.sub(r"\\f .*?\\f\*|\\x .*?\\x\*", "", text)  # 註腳、串珠整段去掉
            text = re.sub(r"\\\w+\*?", "", text)  # 其餘標記（\pn 人名等）只去掉標記、留文字
            counts[key] = counts.get(key, 0) + sum(1 for c in text if "一" <= c <= "鿿")
        by_ch = {}
        for k, n in counts.items():
            c, v, span = (k + (1,))[:3]
            for i in range(span):
                by_ch.setdefault(c, {})[v + i] = by_ch.get(c, {}).get(v + i, 0) + n // span
        out[book["eng"]] = {str(c): [vs.get(v, 0) for v in range(1, max(vs) + 1)] for c, vs in sorted(by_ch.items())}
        vpc = book["verses_per_chapter"]
        diff = [(c, vpc[c - 1], len(out[book["eng"]].get(str(c), []))) for c in range(1, len(vpc) + 1)
                if vpc[c - 1] != len(out[book["eng"]].get(str(c), []))]
        if diff:
            print(f"{book['eng']}: 節數與本書不同，這些章不用作線索 {diff}")
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"{sum(len(v) for b in out.values() for v in b.values())} verses → {OUT}")


if __name__ == "__main__":
    main()
