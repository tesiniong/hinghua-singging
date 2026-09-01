#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch convert images from TIF to WebP format
"""

from PIL import Image
import os
from pathlib import Path

def convert_tif_to_webp(input_dir: str, output_dir: str, quality: int = 90):
    """
    Batch convert TIF to WebP

    Args:
        input_dir: Input directory containing TIF files
        output_dir: Output directory for WebP files
        quality: WebP quality (0-100, recommended 85-95, ignored for lossless)
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    tif_files = sorted(list(input_path.glob('*.tif')), key=lambda x: x.stem)
    total = len(tif_files)

    print(f"Found {total} TIF files")
    print(f"Converting to WebP (lossless mode)...\n")

    total_original_size = 0
    total_webp_size = 0

    for i, tif_file in enumerate(tif_files, 1):
        try:
            # Open TIF file
            img = Image.open(tif_file)

            # Convert to WebP
            webp_file = output_path / f"{tif_file.stem}.webp"

            # For B/W images, use lossless mode
            img.save(webp_file, 'WEBP', lossless=True, method=6)

            # Statistics
            original_size = tif_file.stat().st_size
            webp_size = webp_file.stat().st_size

            total_original_size += original_size
            total_webp_size += webp_size

            size_change = (webp_size / original_size - 1) * 100

            if i % 100 == 0 or i == total:
                print(f"[{i}/{total}] {tif_file.name}: {original_size/1024:.1f} KB -> {webp_size/1024:.1f} KB ({size_change:+.1f}%)")

        except Exception as e:
            print(f"[ERROR] Failed to process {tif_file.name}: {e}")

    print("\n" + "="*60)
    print("[DONE] Conversion complete!")
    print(f"Total original size: {total_original_size/1024/1024:.2f} MB")
    print(f"Total WebP size: {total_webp_size/1024/1024:.2f} MB")
    size_diff = (total_webp_size / total_original_size - 1) * 100
    print(f"Size change: {size_diff:+.1f}%")

if __name__ == '__main__':
    convert_tif_to_webp(
        input_dir='pics',
        output_dir='pics_webp',
        quality=92  # Quality parameter (ignored for lossless mode)
    )
