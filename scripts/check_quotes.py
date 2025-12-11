#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check if Unicode quotes are correctly identified as punctuation
"""
import json

with open('bible_data.json', encoding='utf-8') as f:
    data = json.load(f)

quote_chars = '\u201C\u201D\u2018\u2019'
quote_count = 0
word_with_quote = []

for book in data['books']:
    for ch in book['chapters']:
        for sec in ch['sections']:
            if sec.get('tokens'):
                for tok in sec['tokens']:
                    if tok['type'] == 'punct' and tok['han'] in quote_chars:
                        quote_count += 1
                    elif tok['type'] == 'word' and any(q in tok['han'] for q in quote_chars):
                        word_with_quote.append(tok)

print(f"Unicode quote punctuation tokens: {quote_count}")
print(f"Word tokens containing quotes: {len(word_with_quote)}")

if word_with_quote:
    print("\nFirst 5 word tokens with quotes:")
    for tok in word_with_quote[:5]:
        print(f"  {tok}")
