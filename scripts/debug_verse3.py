#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug verse 3"""

import re

# Read actual verse 3 from hanci.txt
with open('hanci.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find verse 3
verse3_line = None
for line in lines:
    if re.search(r'3[^0-9]', line):
        # Extract verse 3
        match = re.search(r'3([^4]+)', line)
        if match:
            verse3_line = match.group(1)
            break

if verse3_line:
    print("Verse 3 actual text:")
    print("Length:", len(verse3_line))
    print("\nCharacters:")
    for i, c in enumerate(verse3_line[:30]):  # First 30 chars
        print(f"  {i:2d}: U+{ord(c):04X} ({c if c.isprintable() and ord(c) < 0x7F else '?'})")
