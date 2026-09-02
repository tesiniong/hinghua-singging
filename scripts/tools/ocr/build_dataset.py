#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把標籤整理成 kraken `-f path` 格式的資料集（圖檔 symlink + .gt.txt），並寫出清單檔。

測試集固定用人工標註過的 0017–0022 頁，訓練／驗證集不含這些頁面。
另外產生 train_digits.txt（含數字的行重複三次）供第二階段微調節號辨識，
以及 train_boost.txt（含數字、含大寫加調符的行各重複三次）供之後的續訓。
  --page-crops                    整頁裁切版（labels/auto_labels_pages.json → dataset/pages_*，
                                  另出 pages_test_auto.txt 與 pages_test_auto_labels.json：測試頁上抄自 rom.txt 的標籤）
  --page-crops --from-recognized  同上，但標籤取自 labels/auto_labels_pages_recognized.json
"""

import json
import random
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORK  # noqa: E402

TEST_PAGES = {f"{p:04d}" for p in range(17, 23)}
VAL_RATIO = 0.08


def write_split(name, items):
    d = WORK / "dataset" / name
    d.mkdir(parents=True, exist_ok=True)
    paths = []
    for it in items:
        src = Path(it["img"])
        dst = d / f"{src.parent.name}_{src.stem.split('_')[-1]}.png"
        if dst.is_symlink() or dst.exists():
            dst.unlink()
        dst.symlink_to(src)
        dst.with_suffix(".gt.txt").write_text(unicodedata.normalize("NFD", it["text"]) + "\n", encoding="utf-8")
        paths.append(str(dst))
    (WORK / "dataset" / f"{name}.txt").write_text("\n".join(paths) + "\n", encoding="utf-8")
    return len(paths)


def main():
    import sys
    if "--page-crops" in sys.argv:  # 整頁裁切版：資料集另放 pages_*/
        # --from-recognized：用自家模型辨識結果對齊出的標籤（make_labels.py --page-crops --from-recognized）
        name = "auto_labels_pages_recognized.json" if "--from-recognized" in sys.argv else "auto_labels_pages.json"
        auto = json.load(open(WORK / "labels" / name, encoding="utf-8"))
        manual = json.load(open(WORK / "labels" / "manual_pages.json", encoding="utf-8"))
        prefix = "pages_"
        train = [a for a in auto if a["page"] not in TEST_PAGES]
        test = [m for m in manual if m["page"] in TEST_PAGES]
        # 同幾頁、標籤抄自 rom.txt 的測試組：人工標註與整頁裁切的行框有少數對不上，比較模型時用這組
        test_auto = [a for a in auto if a["page"] in TEST_PAGES]
        (WORK / "dataset" / "pages_test_auto.txt").write_text("\n".join(a["img"] for a in test_auto) + "\n", encoding="utf-8")
        json.dump({a["img"]: a["text"] for a in test_auto}, open(WORK / "dataset" / "pages_test_auto_labels.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=0)
        print("test_auto", len(test_auto))
    else:
        auto = json.load(open(WORK / "labels" / "auto_labels.json", encoding="utf-8"))
        manual = json.load(open(WORK / "labels" / "manual_clean.json", encoding="utf-8"))
        prefix = ""
        auto_imgs = {a["img"] for a in auto}
        train = [a for a in auto if a["page"] not in TEST_PAGES]
        train += [m for m in manual if m["status"] == "ok-text" and m["page"] not in TEST_PAGES and m["img"] not in auto_imgs]
        test = [m for m in manual if m["status"] in ("ok", "ok-text") and m["page"] in TEST_PAGES]
    random.Random(0).shuffle(train)
    n_val = int(len(train) * VAL_RATIO)
    val, train = train[:n_val], train[n_val:]
    print("train", write_split(prefix + "train", train), "val", write_split(prefix + "val", val),
          "test", write_split(prefix + "test", test))
    # 上標節號的數字樣本少，另出一份把含數字的行重複三次的清單，供第二階段微調；
    # 大寫字母加調符（Î、A̍）的樣本也少，模型常整個漏掉，再出一份數字與大寫加調符都重複三次的清單
    import re
    lines = [ln.strip() for ln in open(WORK / "dataset" / f"{prefix}train.txt", encoding="utf-8") if ln.strip()]
    gts = {ln: Path(ln).with_suffix(".gt.txt").read_text(encoding="utf-8") for ln in lines}
    digits = [ln for ln in lines if any(ch.isdigit() for ch in gts[ln])]
    caps = [ln for ln in lines if re.search(r"[A-Z][\u0300-\u036f]", gts[ln])]
    (WORK / "dataset" / f"{prefix}train_digits.txt").write_text("\n".join(lines + digits + digits) + "\n", encoding="utf-8")
    print("train_digits", len(lines) + 2 * len(digits), f"({len(digits)} lines with digits, x3)")
    boost = lines + digits + digits + caps + caps
    (WORK / "dataset" / f"{prefix}train_boost.txt").write_text("\n".join(boost) + "\n", encoding="utf-8")
    print("train_boost", len(boost), f"({len(digits)} with digits x3, {len(caps)} with capital+tone mark x3)")


if __name__ == "__main__":
    main()
