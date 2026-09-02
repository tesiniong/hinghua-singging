#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""比對 recognize.py --manifest 的輸出與 .gt.txt，計算 CER 並列出最常見的混淆。

  evaluate.py recognized/test.json
"""

import collections
import difflib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import cer, clusters, nfd  # noqa: E402


def main():
    res = json.load(open(sys.argv[1], encoding="utf-8"))
    pairs = []
    conf = collections.Counter()
    for r in res:
        gt = Path(r["img"]).with_suffix(".gt.txt").read_text(encoding="utf-8").strip()
        pairs.append((r["text"], gt))
        a, _ = clusters(r["text"])
        b, _ = clusters(gt)
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if tag != "equal":
                conf[("".join(a[i1:i2]), "".join(b[j1:j2]))] += 1
    full, b = cer(pairs)
    exact = sum(nfd(p).strip() == nfd(g).strip() for p, g in pairs) / len(pairs)
    print(f"lines={len(pairs)}  CER_full={full:.4f}  CER_base={b:.4f}  line_exact={exact:.3f}")
    print("most common confusions (predicted → truth):")
    for (p, g), n in conf.most_common(25):
        print(f"  {n:4d}  {p!r} → {g!r}")


if __name__ == "__main__":
    main()
