#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用訓練好的 kraken 模型辨識行圖。需在有 kraken 的環境執行（conda env `hinghua-ocr`）。

  recognize.py -m models/hinghua_best.mlmodel --pages 0030-0045 0100
      → WORK/recognized/<page>.json，每頁的行依「欄、由上到下」排序
  recognize.py -m models/hinghua_best.mlmodel --manifest dataset/test.txt -o recognized/test.json
      → 對清單中的行圖辨識，供 evaluate.py 使用

預設用 decode.py 的受限 beam search（只出合法音節、加音節 bigram）；--decoder greedy 用 kraken 的貪婪解碼。
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


class BeamRecognizer:
    """用 net.forward 拿到每格的機率，再交給 decode.py 的受限解碼；介面同 recognize_line。"""

    def __init__(self, net, pages=(), **kw):
        import numpy as np
        from decode import line_decoder, verses_on_pages
        from kraken.lib.dataset import ImageInputTransforms
        batch, channels, height, width = net.nn.input
        self.net = net
        self.ts = ImageInputTransforms(batch, height, width, channels, (16, 0), True)
        # 目標頁上已錄入的經節不拿來估 bigram：評估時才不會看過答案；新頁沒有正本，不影響
        self.decode = line_decoder(net, exclude=verses_on_pages(pages), **kw)
        self.np = np

    def __call__(self, im, name="line"):
        t = self.ts(im.convert("L") if im.mode != "L" else im)
        if t.max() == t.min():
            return "", 0.0, 0.0
        o, _ = self.net.forward(t.unsqueeze(0))
        return self.decode(self.np.asarray(o)[0])


def recognize_line(net, im, name="line"):
    """辨識一張行圖（kraken 貪婪解碼），回傳 (文字, 平均信心, 最低信心)。"""
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


def recognize_images(net, paths, rec=None):
    rec = rec or (lambda im, name: recognize_line(net, im, name))
    out = []
    for p in paths:
        text, conf, conf_min = rec(Image.open(p), str(p))
        out.append({"img": str(p), "text": text, "conf": conf, "conf_min": conf_min})
    return out


def recognize_page(net, page, pad=8, rec=None):
    """依合併後的行框從整頁圖裁切並辨識，回傳依閱讀順序排好的行。"""
    rec = rec or (lambda im, name: recognize_line(net, im, name))
    im = Image.open(PUBLIC / "images" / f"{page}.webp").convert("L")
    boxes, rx = page_lines(page, im)
    im = erase_rule(im, rx)
    out = []
    for b in boxes:
        crop = tight_crop(im, b["x0"], b["y0"] - pad, b["x1"], b["y1"] + pad)
        text, conf, conf_min = rec(crop, f"{page}:{b['idx']}")
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
    ap.add_argument("--decoder", choices=["beam", "greedy"], default="beam")
    ap.add_argument("--lm-weight", type=float, default=0.7)
    ap.add_argument("--beam", type=int, default=8)
    args = ap.parse_args()
    net = load_model(args.model, args.device)
    target_pages = set(expand_pages(args.pages))
    if args.manifest:
        target_pages |= {Path(ln.strip()).parent.name for ln in open(args.manifest, encoding="utf-8") if ln.strip()}
    rec = BeamRecognizer(net, pages=target_pages, beam=args.beam, lm_weight=args.lm_weight) if args.decoder == "beam" else None
    decoder_tag = f"beam{args.beam}-lm{args.lm_weight}" if rec else "greedy"
    if args.manifest:
        paths = [ln.strip() for ln in open(args.manifest, encoding="utf-8") if ln.strip()]
        res = recognize_images(net, paths, rec)
        out = Path(args.output or WORK / "recognized" / "manifest.json")
        out.parent.mkdir(parents=True, exist_ok=True)
        json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        print(f"{len(res)} lines → {out}")
    outdir = WORK / "recognized"
    outdir.mkdir(parents=True, exist_ok=True)
    for page in expand_pages(args.pages):
        res, rx = recognize_page(net, page, rec=rec)
        json.dump({"page": page, "model": str(args.model), "decoder": decoder_tag, "rule_x": rx, "lines": res},
                  open(outdir / f"{page}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        print(f"{page}: {len(res)} lines")


if __name__ == "__main__":
    main()
