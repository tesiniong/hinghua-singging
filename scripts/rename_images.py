#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
圖片重命名腳本
將亂序的 TIF 檔案重新命名為純數字流水號
"""

import os
import shutil
from pathlib import Path
from natsort import natsorted

def rename_images(input_dir: str, output_dir: str, start_num: int = 1):
    """
    重新命名圖片為流水號

    Args:
        input_dir: 輸入目錄
        output_dir: 輸出目錄
        start_num: 起始編號（預設為 1）
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # 獲取所有 TIF 檔案並自然排序
    tif_files = list(input_path.glob('*.tif'))
    tif_files = natsorted(tif_files)

    print(f"找到 {len(tif_files)} 個圖片檔案")
    print("前 10 個檔案（排序後）：")
    for i, f in enumerate(tif_files[:10], 1):
        print(f"  {i}. {f.name}")

    print("\n開始重命名...")

    # 重命名並複製
    for i, tif_file in enumerate(tif_files, start_num):
        new_name = f"{i:04d}.tif"  # 使用 4 位數字，如 0001.tif
        new_path = output_path / new_name

        shutil.copy2(tif_file, new_path)

        if i <= 10 or i % 100 == 0:
            print(f"  {tif_file.name} → {new_name}")

    print(f"\n完成！共重命名 {len(tif_files)} 個檔案")
    print(f"輸出目錄：{output_path}")

if __name__ == '__main__':
    # 您可能需要先安裝 natsort: pip install natsort
    rename_images(
        input_dir='pics',
        output_dir='pics_renamed',
        start_num=1
    )
