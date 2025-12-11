#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check quote characters"""

# Read the actual text
with open('hanci.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Find quotes
quotes = set()
for char in text:
    if ord(char) in range(0x2018, 0x201F):  # Unicode quote range
        quotes.add((char, hex(ord(char))))

print("Found quotes:")
for char, code in sorted(quotes):
    print(f"  '{char}' = {code}")

# Check if our punct string includes them
punct_str = '。，、；：！？（）「」….,;:!?()\'"""''\u201C\u201D\u2018\u2019'
print(f"\nPunctuation string includes:")
for char, code in sorted(quotes):
    if char in punct_str:
        print(f"  '{char}' = {code} [OK]")
    else:
        print(f"  '{char}' = {code} [MISSING]")
