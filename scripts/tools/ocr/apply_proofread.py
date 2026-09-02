#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把校對者對 proofread.html 的決定套用到 data/rom.txt。

校對者看 proofread.html（proofread.py 的輸出）後，用一個決定檔說哪些節要照 OCR 改：

  創世記 3:3                 # 這一節「差異」欄列的每一項都照 OCR 改
  創世記 4:23	3            # 只套用第 3 項（依「差異」欄的順序，從 1 起算）
  馬太 2:16	1,3          # 只套用第 1、3 項
  # 沒列出的節一律不動

  apply_proofread.py decisions.txt                 # 乾跑：逐節印出會套用的差異
  apply_proofread.py decisions.txt --write         # 寫入 data/rom.txt
  apply_proofread.py decisions.txt --report recognized/proofread_2026-09-02.html   # 指定校對者看的那份報告

報告裡每節的差異順序與 <mark> 標記一一對應，所以能精確定位；詩體多行節會對應回正確的那一行。
套用後請跑 python scripts/build_all.py，並把 rom.txt 與生成檔一起 commit。
"""

import argparse
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import book_info as B  # noqa: E402
from common import DATA, WORK, nfc  # noqa: E402

HAN_TO_ROM = {nfc(b["han"]): nfc(b["rom"]) for b in B.OLD_TESTAMENT_BOOKS + B.NEW_TESTAMENT_BOOKS}
ROW_RE = re.compile(r"<tr class='([ABCD])'><td class='cat'>[ABCD]</td><td>(.*?)<br>(\d+):(\d+)</td>"
                    r"<td>(.*?)<br><span style='color:#555'>(.*?)</span></td><td>(.*?)</td><td>", re.S)


def parse_report(path):
    rows = {}
    for cat, han, c, v, gt_marked, _ocr, diffs in ROW_RE.findall(open(path, encoding="utf-8").read()):
        items = [(html.unescape(a), html.unescape(b)) for _, a, b in re.findall(r"\[([ABCDS])\] 「(.*?)」→「(.*?)」", diffs)]
        marks = [html.unescape(m) for m in re.findall(r"<mark>(.*?)</mark>", gt_marked, flags=re.S)]
        segs = [html.unescape(x) for x in re.split(r"<mark>.*?</mark>", gt_marked, flags=re.S)]
        if len(marks) != len(items):
            print(f"!! {han} {c}:{v}: 標記數 {len(marks)} 與差異數 {len(items)} 不符，略過", file=sys.stderr)
            continue
        rows[(nfc(han), int(c), int(v))] = (segs, marks, items)
    return rows


def parse_decisions(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.split("#")[0].strip()
        if not line:
            continue
        ref, _, sel = line.partition("\t")
        m = re.match(r"(\S+)\s+(\d+):(\d+)$", ref.strip())
        if not m:
            raise SystemExit(f"看不懂：{line}")
        picks = {int(x) for x in re.split(r"[,\s]+", sel.strip()) if x} if sel.strip() else None
        out.append(((nfc(m.group(1)), int(m.group(2)), int(m.group(3))), picks))
    return out


def apply_to_rom(changes, path, write):
    lines = open(path, encoding="utf-8").read().split("\n")
    starts = {nfc(l[2:].strip()): i for i, l in enumerate(lines) if l.startswith("# ")}
    n = 0
    for (han, c, v), (segs, marks, edits, applied) in sorted(changes.items()):
        b0 = starts[HAN_TO_ROM[han]]
        b1 = min([i for i in starts.values() if i > b0] + [len(lines)])
        ch, hit = None, None
        for i in range(b0, b1):
            if lines[i].startswith("## "):
                ch = int(lines[i][3:])
            elif ch == c and re.match(rf"^{v}\s", lines[i]):
                hit = i
                break
        if hit is None:
            print(f"!! {han} {c}:{v} 在 rom.txt 找不到", file=sys.stderr)
            continue
        idxs = [hit]
        while idxs[-1] + 1 < len(lines) and lines[idxs[-1] + 1].strip() and not re.match(r"^\d+\s|^#", lines[idxs[-1] + 1]):
            idxs.append(idxs[-1] + 1)  # 詩體續行
        parts = [nfc(lines[hit][len(str(v)):].strip())] + [nfc(lines[i].strip()) for i in idxs[1:]]
        old = nfc("".join(s + m for s, m in zip(segs, marks)) + segs[-1])
        if nfc(" ".join(parts)) != old:
            print(f"!! {han} {c}:{v}: rom.txt 的內容與報告不同（報告可能過時），略過", file=sys.stderr)
            continue
        bounds, p = [], 0
        for t in parts:
            bounds.append((p, p + len(t)))
            p += len(t) + 1
        for off, gt_frag, ocr_frag in sorted(edits, reverse=True):
            li = next(i for i, (s0, s1) in enumerate(bounds) if s0 <= off <= s1)
            loc = off - bounds[li][0]
            assert parts[li][loc:loc + len(gt_frag)] == gt_frag, (han, c, v, gt_frag)
            parts[li] = parts[li][:loc] + ocr_frag + parts[li][loc + len(gt_frag):]
        lines[hit] = f"{v} {parts[0]}"
        for i, t in zip(idxs[1:], parts[1:]):
            lines[i] = re.match(r"^\s*", lines[i]).group(0) + t
        n += 1
        print(f"{han} {c}:{v}{'（多行）' if len(idxs) > 1 else ''}  {'；'.join(applied)}")
    if write:
        open(path, "w", encoding="utf-8").write("\n".join(lines))
        print(f"written {n} verses → {path}")
    else:
        print(f"dry run: {n} verses would change（加 --write 才寫入）")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("decisions")
    ap.add_argument("--report", default=str(WORK / "recognized" / "proofread.html"))
    ap.add_argument("--rom", default=str(DATA / "rom.txt"))
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    rows = parse_report(args.report)
    changes = {}
    for ref, picks in parse_decisions(args.decisions):
        if ref not in rows:
            print(f"!! {ref[0]} {ref[1]}:{ref[2]} 不在報告裡", file=sys.stderr)
            continue
        segs, marks, items = rows[ref]
        edits, applied, off = [], [], 0
        for k, ((ocr_frag, gt_frag), mark) in enumerate(zip(items, marks), 1):
            off += len(nfc(segs[k - 1]))
            if picks is None or k in picks:
                edits.append((off, nfc(mark), nfc(ocr_frag)))
                applied.append(f"{k}:「{gt_frag}」→「{ocr_frag}」")
            off += len(nfc(mark))
        if picks and (bad := picks - set(range(1, len(items) + 1))):
            print(f"!! {ref[0]} {ref[1]}:{ref[2]} 沒有第 {sorted(bad)} 項（只有 {len(items)} 項）", file=sys.stderr)
        changes[ref] = (segs, marks, edits, applied)
    apply_to_rom(changes, args.rom, args.write)


if __name__ == "__main__":
    main()
