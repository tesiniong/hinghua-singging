#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""專案內共用的路徑常數。

腳本一律透過本模組定位檔案，而不是寫死相對路徑，
這樣從任何工作目錄執行都會讀寫到同一批檔案。
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data"
SCRIPTS = ROOT / "scripts"
WEBSITE = ROOT / "website"
PUBLIC = WEBSITE / "public"
WEBSITE_DATA = WEBSITE / "src" / "data"
FONTS = WEBSITE / "src" / "assets" / "fonts"
PICS = ROOT / "pics"


def add_scripts_to_path():
    """讓 build/ 與 tools/ 下的腳本能匯入 scripts/ 的共用模組。"""
    path = str(SCRIPTS)
    if path not in sys.path:
        sys.path.insert(0, path)
