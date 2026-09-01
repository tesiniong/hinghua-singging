#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""產生網站圖示與社群預覽圖 (og:image)。

輸出至 website/public/：
  favicon-32.png, favicon-192.png, apple-touch-icon.png, og-image.png

字型取自 website/src/assets/fonts/，與網站本身使用的字型一致；
平話字的組合變音符號由 Pillow 的 Raqm 排版引擎處理。

用法：python scripts/generate_site_icons.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "website" / "src" / "assets" / "fonts"
OUT = ROOT / "website" / "public"

# 與 website/src/index.css 的 CSS 變數一致
TEXT_PRIMARY = "#333333"
TEXT_SECONDARY = "#666666"
BG_PRIMARY = "#ffffff"
BORDER = "#e0e0e0"

# 與 website/src/pages/Home.jsx 的標題區塊一致
TITLE_HAN = "舊新約全書　興化平話"
TITLE_ROM = "GŪ-SING-IO̤H CÉ̤ⁿ-CṲ HING-HUA̍ BÁⁿ-UĀ"
TITLE_ENG = "THE HOLY BIBLE"
TITLE_SUB = "in the HINGHWA DIALECT, ROMANIZED"
TITLE_YEAR = "anno domini 1912"


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def draw_centred(draw, y, text, fnt, fill, width):
    draw.text((width // 2, y), text, font=fnt, fill=fill, anchor="mm")


def make_og_image():
    """1200x630 社群預覽卡，重現網站首頁的標題區塊。"""
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), BG_PRIMARY)
    draw = ImageDraw.Draw(img)

    # 雙線外框，呼應原書扉頁
    draw.rectangle([28, 28, w - 29, h - 29], outline=BORDER, width=2)
    draw.rectangle([38, 38, w - 39, h - 39], outline=BORDER, width=1)

    draw_centred(draw, 176, TITLE_HAN, font("NotoSansTC-Bold.ttf", 66), TEXT_PRIMARY, w)
    # 平話字用 DejaVu Sans：與網站的 --font-roman 一致，且完整覆蓋組合變音符號
    # （TauhuOo 缺 U+0324 與 U+1E72，會出現豆腐格）
    draw_centred(draw, 256, TITLE_ROM, font("DejaVuSans.ttf", 30), TEXT_SECONDARY, w)

    draw.line([(430, 322), (770, 322)], fill=BORDER, width=1)

    draw_centred(draw, 386, TITLE_ENG, font("DejaVuSans-Bold.ttf", 34), TEXT_PRIMARY, w)
    draw_centred(draw, 438, TITLE_SUB, font("DejaVuSans.ttf", 22), TEXT_SECONDARY, w)
    draw_centred(draw, 478, TITLE_YEAR, font("DejaVuSans.ttf", 22), TEXT_SECONDARY, w)

    img.save(OUT / "og-image.png", optimize=True)
    return OUT / "og-image.png"


def make_icon(size):
    """深色圓角方塊配白色「興」字，在明暗兩種分頁列上都清楚。"""
    scale = 4  # 先放大繪製再縮小，取得平滑邊緣
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.18), fill=TEXT_PRIMARY)
    fnt = font("NotoSansTC-Bold.ttf", int(s * 0.72))
    draw.text((s // 2, int(s * 0.54)), "興", font=fnt, fill="#ffffff", anchor="mm")
    return img.resize((size, size), Image.LANCZOS)


def main():
    written = [make_og_image()]
    for size, name in ((32, "favicon-32.png"), (192, "favicon-192.png"), (180, "apple-touch-icon.png")):
        path = OUT / name
        make_icon(size).save(path, optimize=True)
        written.append(path)

    for path in written:
        print(f"  [OK] {path.relative_to(ROOT)} ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
