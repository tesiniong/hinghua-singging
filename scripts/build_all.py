#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""完整建置流程的單一入口。

依序執行 scripts/build/ 下的各步驟，把 data/ 的來源檔轉成
website/ 需要的資料檔。從任何工作目錄執行都可以。

    python scripts/build_all.py              # 全部執行
    python scripts/build_all.py --list       # 只列出步驟
    python scripts/build_all.py --only bible_data
    python scripts/build_all.py --skip site_icons

改過 data/han.txt 或 data/rom.txt 之後一定要跑一次，
否則網站上讀到的還是舊資料。
"""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paths import ROOT, SCRIPTS

BUILD = SCRIPTS / "build"

# (名稱, 說明, 腳本, 是否可在相依套件缺席時跳過)
STEPS = [
    ("bible_data", "經文資料、書目清單、進度統計", BUILD / "bible_data.py", False),
    ("rom_to_han_dict", "羅馬字轉漢字字典", BUILD / "rom_to_han_dict.py", False),
    ("homophone_table", "同音字表", BUILD / "homophone_table.py", False),
    ("rhyme_table", "韻母表（需 openpyxl）", BUILD / "rhyme_table.py", True),
    ("site_icons", "網站圖示與社群預覽圖（需 Pillow）", BUILD / "site_icons.py", True),
]

NAMES = [name for name, _, _, _ in STEPS]


def run_step(name, description, script):
    print(f"\n{'=' * 64}\n[{name}] {description}\n{'=' * 64}")
    result = subprocess.run([sys.executable, str(script)], cwd=ROOT)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="執行完整建置流程")
    parser.add_argument("--only", nargs="+", metavar="STEP", help=f"只執行指定步驟：{', '.join(NAMES)}")
    parser.add_argument("--skip", nargs="+", metavar="STEP", help="跳過指定步驟")
    parser.add_argument("--list", action="store_true", help="列出所有步驟後結束")
    args = parser.parse_args()

    if args.list:
        for name, description, _, optional in STEPS:
            print(f"  {name:<18} {description}{'（可跳過）' if optional else ''}")
        return 0

    for given in (args.only or []) + (args.skip or []):
        if given not in NAMES:
            parser.error(f"未知的步驟 {given!r}，可用的有：{', '.join(NAMES)}")

    selected = [s for s in STEPS if (not args.only or s[0] in args.only) and s[0] not in (args.skip or [])]
    if not selected:
        print("沒有選到任何步驟")
        return 1

    done, skipped, failed = [], [], []
    for name, description, script, optional in selected:
        if run_step(name, description, script):
            done.append(name)
        elif optional:
            # 韻母表與圖示的來源極少變動，缺套件時不該擋住整條流程
            skipped.append(name)
        else:
            failed.append(name)
            break

    print(f"\n{'=' * 64}\n建置摘要\n{'=' * 64}")
    for name in done:
        print(f"  [OK]   {name}")
    for name in skipped:
        print(f"  [SKIP] {name}（步驟失敗，可能缺少相依套件）")
    for name in failed:
        print(f"  [FAIL] {name}")

    if failed:
        print("\n建置中止。")
        return 1
    print("\n建置完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
