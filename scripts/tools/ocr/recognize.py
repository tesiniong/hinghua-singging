#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用訓練好的 kraken 模型辨識行圖。需在有 kraken 的環境執行（conda env `hinghua-ocr`）。

  recognize.py -m models/hinghua_best.mlmodel --pages 0030-0045 0100
      → WORK/recognized/<page>.json，每頁的行依「欄、由上到下」排序
  recognize.py -m models/hinghua_best.mlmodel --manifest dataset/test.txt -o recognized/test.json
      → 對清單中的行圖辨識，供 evaluate.py 使用
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _paths import PUBLIC  # noqa: E402
from common import WORK, erase_rule, nfc, page_lines, tight_crop  # noqa: E402


def load_model(path, device="cuda:0"):
    from kraken.lib import models
    return models.load_any(str(path), device=device)


def recognize_line(net, im, name="line"):
    """辨識一張行圖，回傳 (文字, 平均信心, 最低信心)。"""
    from kraken import rpred
    from kraken.containers import BBoxLine, Segmentation
    seg = Segmentation(type="bbox", imagename=name, text_direction="horizontal-lr", script_detection=False,
                       lines=[BBoxLine(id="l0", bbox=(0, 0, im.width, im.height))])
    try:
        rec = next(rpred.rpred(net, im, seg))
    except StopIteration:
        return "", 0.0, 0.0
    confs = [float(c) for c in rec.confidences]
    return nfc(rec.prediction), (round(sum(confs) / len(confs), 4) if confs else 0.0), (round(min(confs), 4) if confs else 0.0)


def recognize_images(net, paths):
    out = []
    for p in paths:
        text, conf, conf_min = recognize_line(net, Image.open(p), str(p))
        out.append({"img": str(p), "text": text, "conf": conf, "conf_min": conf_min})
    return out


def recognize_page(net, page, pad=8):
    """依合併後的行框從整頁圖裁切並辨識，回傳依閱讀順序排好的行。"""
    im = Image.open(PUBLIC / "images" / f"{page}.webp").convert("L")
    boxes, rx = page_lines(page, im)
    im = erase_rule(im, rx)
    out = []
    for b in boxes:
        crop = tight_crop(im, b["x0"], b["y0"] - pad, b["x1"], b["y1"] + pad)
        text, conf, conf_min = recognize_line(net, crop, f"{page}:{b['idx']}")
        out.append({"idx": b["idx"], "col": b["col"], "y": round(b["y"]), "x0": b["x0"], "x1": b["x1"],
                    "dropcap": b["dropcap"], "header": b["header"], "footer": b["footer"],
                    "text": text, "conf": conf, "conf_min": conf_min})
    return out, rx


def expand_pages(specs):
    pages = []
    for s in specs:
        if "-" in s:
            a, b = s.split("-")
            pages.extend(f"{i:04d}" for i in range(int(a), int(b) + 1))
        else:
            pages.append(f"{int(s):04d}")
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", required=True)
    ap.add_argument("-d", "--device", default="cuda:0")
    ap.add_argument("--pages", nargs="*", default=[])
    ap.add_argument("--manifest")
    ap.add_argument("-o", "--output")
    args = ap.parse_args()
    net = load_model(args.model, args.device)
    if args.manifest:
        paths = [ln.strip() for ln in open(args.manifest, encoding="utf-8") if ln.strip()]
        res = recognize_images(net, paths)
        out = Path(args.output or WORK / "recognized" / "manifest.json")
        out.parent.mkdir(parents=True, exist_ok=True)
        json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        print(f"{len(res)} lines → {out}")
    outdir = WORK / "recognized"
    outdir.mkdir(parents=True, exist_ok=True)
    for page in expand_pages(args.pages):
        res, rx = recognize_page(net, page)
        json.dump({"page": page, "model": str(args.model), "rule_x": rx, "lines": res},
                  open(outdir / f"{page}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        print(f"{page}: {len(res)} lines")


if __name__ == "__main__":
    main()
