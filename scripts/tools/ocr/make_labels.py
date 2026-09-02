#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 PaddleOCR 的零樣本輸出對齊 rom.txt，為行圖自動產生帶符號的訓練標籤。

只處理 rom.txt 已有經文的頁面。輸出：
  WORK/labels/auto_labels.json    自動標籤 [{img, page, book, text, ocr, ned}]
  WORK/labels/manual_clean.json   前次人工標註的清理結果（附狀態）

加 --page-crops 則改用整頁圖依合併行框裁切（與辨識時相同的裁法），輸出
  WORK/pagecrops/、labels/auto_labels_pages.json、labels/manual_pages.json
再加 --from-recognized 則不跑 PaddleOCR，改拿 recognize.py 已產生的辨識結果來對齊
（模型比 PaddleOCR 準，能對上更多行），輸出 labels/auto_labels_pages_recognized.json
"""

import glob
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (GAP, LINE_IMAGES, WORK, base, clusters, lev, load_page_map,  # noqa: E402
                    load_rom_verses, nfc, page_text_for, semi_global, snap)

MANUAL = Path("/home/siniong/projects/buc_ocr/data/manual_labels.json")
MAX_NED = 0.3
MIN_LEN = 8


def ocr_lines(paths):
    from paddleocr import TextRecognition
    model = TextRecognition(model_name="latin_PP-OCRv5_mobile_rec")
    out = []
    for i in range(0, len(paths), 64):
        for r in model.predict(input=paths[i:i + 64], batch_size=64):
            d = r.json["res"] if hasattr(r, "json") else r
            out.append(d.get("rec_text", ""))
    return out


def align_page(page, eng, text, imgs, ocr):
    cl, pb = clusters(text)
    labels = []
    for img, pr in zip(imgs, ocr):
        _, lb = clusters(pr)
        if len(lb) < MIN_LEN:
            continue
        d, s, t = semi_global(pb, lb)
        if d / len(lb) > MAX_NED:
            continue
        s, t = snap(pb, s, t, lb)
        span = pb[s:t]
        if GAP in span or (s > 0 and pb[s - 1] == GAP) or (t < len(pb) and pb[t] == GAP):
            continue  # 貼著缺文邊界的行，標籤可能不完整
        label = nfc("".join(cl[s:t])).strip()
        lbase = base(label)
        if abs(len(lbase) - len(lb)) > max(3, 0.25 * len(lb)):
            continue  # 長度差太多：行圖含有標籤外的文字，或切割有誤
        labels.append({"img": str(img), "page": page, "book": eng, "text": label,
                       "ocr": pr, "ned": round(lev(lbase, lb) / len(lb), 3)})
    return labels


def clean_manual(auto):
    """把前次人工標註分類：ok / ok-text（無自動標籤但與經文相符）/ offbyone / bad。"""
    if not MANUAL.exists():
        return []
    ml = json.load(open(MANUAL, encoding="utf-8"))
    by_img = {a["img"]: a["text"] for a in auto}
    pm, pages = load_page_map()
    filled = load_rom_verses()
    texts = {}
    out = []
    for m in ml:
        img = str(LINE_IMAGES / m["filename"])
        page, idx = re.match(r"(\d+)/\d+_line_(\d+)\.png", m["filename"]).groups()
        idx = int(idx)
        gt = nfc(m["ground_truth"]).strip()
        gb = base(gt)
        own = by_img.get(img)
        status = "bad"
        if own is not None:
            status = "ok" if lev(base(own), gb) / max(len(gb), 1) <= 0.15 else "bad"
        if status == "bad":
            for k in (idx - 1, idx + 1):
                nb = by_img.get(str(LINE_IMAGES / page / f"{page}_line_{k:04d}.png"))
                if nb and lev(base(nb), gb) / max(len(gb), 1) <= 0.1:
                    status = "offbyone"
        if status == "bad" and own is None and len(gb) >= MIN_LEN:
            if page not in texts:
                texts[page] = clusters(page_text_for(pm, pages, page, filled)[2])[1]
            d, _, _ = semi_global(texts[page], gb)
            if d / len(gb) <= 0.1:
                status = "ok-text"
        out.append({"img": img, "page": page, "idx": idx, "text": gt, "status": status})
    return out


def make_page_crops(targets, pm, pages, filled, from_recognized=False):
    """用整頁圖依合併後的行框裁切（與 recognize.py 相同的裁法），產生標籤與對應的測試集。

    輸出 WORK/pagecrops/<page>/<page>_<k>.png、labels/auto_labels_pages.json、labels/manual_pages.json。
    """
    from PIL import Image
    from common import PUBLIC, erase_rule, page_lines, tight_crop
    manual = {}
    if MANUAL.exists():
        for m in json.load(open(MANUAL, encoding="utf-8")):
            page, idx = re.match(r"(\d+)/\d+_line_(\d+)\.png", m["filename"]).groups()
            manual[(page, int(idx))] = nfc(m["ground_truth"]).strip()
    all_imgs, by_page, manual_pages = [], {}, []
    for p, eng, text in targets:
        im = Image.open(PUBLIC / "images" / f"{p}.webp").convert("L")
        boxes, rx = page_lines(p, im)
        im = erase_rule(im, rx)
        d = WORK / "pagecrops" / p
        d.mkdir(parents=True, exist_ok=True)
        paths = []
        for k, b in enumerate(boxes):
            out = d / f"{p}_{k:03d}.png"
            if not out.exists():
                tight_crop(im, b["x0"], b["y0"] - 8, b["x1"], b["y1"] + 8).save(out)
            paths.append(str(out))
            if len(b["idx"]) == 1 and (p, b["idx"][0]) in manual:
                manual_pages.append({"img": str(out), "page": p, "text": manual[(p, b["idx"][0])]})
        by_page[p] = paths
        all_imgs.extend(paths)
    print(f"page crops: {len(all_imgs)}; manual-labelled crops: {len(manual_pages)}")
    if from_recognized:
        # 用自己訓練好的模型的辨識結果（recognize.py 的輸出）當對齊依據，比 PaddleOCR 準，能對上更多行
        ocr = {}
        for p, _, _ in targets:
            f = WORK / "recognized" / f"{p}.json"
            if f.exists():
                lines = json.load(open(f, encoding="utf-8"))["lines"]
                for path, ln in zip(by_page[p], lines):
                    ocr[path] = ln["text"]
        out_name = "auto_labels_pages_recognized.json"
    else:
        ocr = dict(zip(all_imgs, ocr_lines(all_imgs)))
        out_name = "auto_labels_pages.json"
    auto = []
    for p, eng, text in targets:
        auto.extend(align_page(p, eng, text, by_page[p], [ocr.get(i, "") for i in by_page[p]]))
    json.dump(auto, open(WORK / "labels" / out_name, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    json.dump(manual_pages, open(WORK / "labels" / "manual_pages.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"auto labels (page crops): {len(auto)}")


def main():
    import sys as _sys
    pm, pages = load_page_map()
    filled = load_rom_verses()
    targets = []
    for p in pages:
        eng, vs, text = page_text_for(pm, pages, p, filled)
        if vs and any(x in filled.get(eng, {}) for x in vs):
            targets.append((p, eng, text))
    print(f"pages with ground truth: {len(targets)}")
    (WORK / "labels").mkdir(parents=True, exist_ok=True)
    if "--page-crops" in _sys.argv:
        make_page_crops(targets, pm, pages, filled, from_recognized="--from-recognized" in _sys.argv)
        return
    all_imgs = []
    for p, _, _ in targets:
        all_imgs.extend(sorted(glob.glob(str(LINE_IMAGES / p / "*.png"))))
    print(f"line images to OCR: {len(all_imgs)}")
    ocr = dict(zip(all_imgs, ocr_lines(all_imgs)))
    auto = []
    for p, eng, text in targets:
        imgs = sorted(glob.glob(str(LINE_IMAGES / p / "*.png")))
        auto.extend(align_page(p, eng, text, imgs, [ocr[i] for i in imgs]))
    (WORK / "labels").mkdir(parents=True, exist_ok=True)
    json.dump(auto, open(WORK / "labels" / "auto_labels.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"auto labels: {len(auto)}")
    manual = clean_manual(auto)
    json.dump(manual, open(WORK / "labels" / "manual_clean.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    from collections import Counter
    print("manual labels by status:", Counter(m["status"] for m in manual))


if __name__ == "__main__":
    main()
