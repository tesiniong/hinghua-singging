#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test tokenize function"""

import sys
sys.path.insert(0, 'scripts')
from parse_text_v3 import BibleTextParserV3

parser = BibleTextParserV3()

# Test verse 3
han_text = '上帝講："着有光"，即有光。'
rom_text = 'Siō̤ng-Da̤̍ gô̤ng, Da̤u̍h ū gng: cuh ū gng.'

print("Testing tokenization...")
print("\nHan tokens:")
han_tokens = parser._tokenize_hanci(han_text)
for i, t in enumerate(han_tokens):
    typ = t['type']
    txt_len = len(t['text'])
    txt_hex = ' '.join([hex(ord(c)) for c in t['text']])
    print(f"  {i}: type={typ}, len={txt_len}, hex={txt_hex}")

print("\n" + "="*60)
print("Rom tokens:")
rom_tokens = parser._tokenize_lomaci(rom_text)
for i, t in enumerate(rom_tokens):
    typ = t['type']
    txt_len = len(t['text'])
    print(f"  {i}: type={typ}, len={txt_len}")
