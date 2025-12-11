#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check verse 13 tokenization"""

import json

# Load bible data
with open('bible_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find verse 13
v13 = [v for v in data['books'][0]['chapters'][0]['verses'] if v['verse'] == 13][0]

# Write to output file
with open('verse13_analysis.txt', 'w', encoding='utf-8') as out:
    out.write("[Verse 13]\n")
    out.write(f"Han: {v13['han']}\n")
    out.write(f"Rom: {v13['rom']}\n")

    # Write tokens
    out.write("\n[Tokens]\n")
    for i, token in enumerate(v13['tokens']):
        if token['type'] == 'word':
            out.write(f"  {i}: {token['han']}/{token['rom']} (form={token['form']})\n")
        else:
            out.write(f"  {i}: [{token['type']}] '{token['han']}'\n")

    # Check specific phrases
    out.write("\n[Analysis]\n")
    phrases = [t for t in v13['tokens'] if t.get('form') == 'phrase']
    out.write(f"Found {len(phrases)} phrase tokens:\n")
    for p in phrases:
        out.write(f"  - {p['han']}/{p['rom']}\n")

print("[OK] Verse 13 analysis written to verse13_analysis.txt")
