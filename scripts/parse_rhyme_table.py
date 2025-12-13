#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析韵母表HTML文件并生成JSON数据
"""

from bs4 import BeautifulSoup
import json
import re
import sys

def clean_html_text(html_text):
    """清理HTML文本，保留必要的格式"""
    if not html_text:
        return ''
    # 移除多余的空格
    text = re.sub(r'\s+', ' ', html_text).strip()
    # 处理特殊字符
    text = text.replace('&atilde;', 'ã')
    text = text.replace('&oslash;', 'ø')
    text = text.replace('&oslash;&#771;', 'ø̃')
    text = text.replace('&#771;', '̃')
    text = text.replace('&#603;', 'ɛ')
    text = text.replace('&#7869;', 'ẽ')
    text = text.replace('&#297;', 'ĩ')
    text = text.replace('&#339;', 'œ')
    text = text.replace('&#7929;', 'ủ')
    text = text.replace('&#594;', 'ɔ')
    text = text.replace('&#596;', 'ɔ')
    text = text.replace('&#804;', '̤')  # 底线
    text = text.replace('&#8319;', 'ⁿ')  # 上标n
    return text

def extract_cell_content(cell):
    """提取单元格内容，包括HTML格式"""
    if not cell:
        return '-'

    # 获取cell的所有文本和HTML
    html_content = str(cell)

    # 提取div中的内容（如果有）
    div = cell.find('div')
    if div:
        content = ''.join(str(c) for c in div.contents)
    else:
        content = ''.join(str(c) for c in cell.contents)

    # 清理内容
    content = clean_html_text(content)
    content = content.replace('<font class="font10">', '')
    content = content.replace('<font class="font11">', '')
    content = content.replace('<font class="font9">', '')
    content = content.replace('<font class="font6">', '')
    content = content.replace('</font>', '')
    content = content.strip()

    return content if content else '-'

def parse_rhyme_table(html_file):
    """解析韵母表HTML文件"""

    # 读取文件（Big5编码）
    with open(html_file, 'r', encoding='big5', errors='ignore') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # 找到表格
    table = soup.find('table')
    if not table:
        print("未找到表格")
        return []

    rows = table.find_all('tr')

    # 跳过前两行（表头）
    data_rows = rows[2:]

    result = []
    current_rowspan_info = {}  # 记录跨行信息

    for row_idx, row in enumerate(data_rows):
        cells = row.find_all(['td', 'th'])

        if len(cells) < 3:
            continue

        cell_idx = 0
        row_data = {
            'letter': '',
            'examples': '',
            'phonetic': '',
            'dialectValues': [''] * 16,
            'rowSpan': 1,
            'hasBorder': False
        }

        # 检查第一个单元格是否有rowspan
        first_cell = cells[cell_idx]
        rowspan = first_cell.get('rowspan')
        if rowspan:
            rowspan = int(rowspan)
            row_data['rowSpan'] = rowspan
            current_rowspan_info['letter'] = extract_cell_content(first_cell)
            current_rowspan_info['rowspan_remaining'] = rowspan - 1
            row_data['letter'] = current_rowspan_info['letter']
            cell_idx += 1
        elif 'rowspan_remaining' in current_rowspan_info and current_rowspan_info['rowspan_remaining'] > 0:
            # 使用之前的rowspan值
            row_data['letter'] = current_rowspan_info['letter']
            row_data['rowSpan'] = 0  # 表示这是被合并的行
            current_rowspan_info['rowspan_remaining'] -= 1
        else:
            row_data['letter'] = extract_cell_content(first_cell)
            cell_idx += 1

        # 检查单元格是否有底线（border-bottom）
        for cell in cells:
            style = cell.get('style', '')
            if 'border-bottom' in style and 'solid black' in style:
                row_data['hasBorder'] = True
                break

        # 例字
        if cell_idx < len(cells):
            row_data['examples'] = extract_cell_content(cells[cell_idx])
            cell_idx += 1

        # 音价
        if cell_idx < len(cells):
            row_data['phonetic'] = extract_cell_content(cells[cell_idx])
            cell_idx += 1

        # 16个方言点的音值
        dialect_idx = 0
        while cell_idx < len(cells) and dialect_idx < 16:
            cell = cells[cell_idx]
            cell_rowspan = cell.get('rowspan')

            if cell_rowspan and int(cell_rowspan) > 1:
                # 这个单元格跨多行
                value = extract_cell_content(cell)
                row_data['dialectValues'][dialect_idx] = value
                # 记录这个方言点需要在后续行中使用相同的值
                if dialect_idx not in current_rowspan_info:
                    current_rowspan_info[dialect_idx] = {}
                current_rowspan_info[dialect_idx]['value'] = value
                current_rowspan_info[dialect_idx]['remaining'] = int(cell_rowspan) - 1
            elif dialect_idx in current_rowspan_info and 'remaining' in current_rowspan_info[dialect_idx] and current_rowspan_info[dialect_idx]['remaining'] > 0:
                # 使用之前的rowspan值
                row_data['dialectValues'][dialect_idx] = current_rowspan_info[dialect_idx]['value']
                current_rowspan_info[dialect_idx]['remaining'] -= 1
                # 不增加cell_idx，因为这个单元格被跨行了
                dialect_idx += 1
                continue
            else:
                row_data['dialectValues'][dialect_idx] = extract_cell_content(cell)

            cell_idx += 1
            dialect_idx += 1

        result.append(row_data)

    return result

def main():
    html_file = 'data/hinghua_rhymes.files/sheet001.htm'
    output_file = 'website/src/data/rhymeTableData.json'

    print(f"Parsing {html_file}...")
    data = parse_rhyme_table(html_file)

    print(f"Extracted {len(data)} rows")

    # Create output directory
    import os
    os.makedirs('website/src/data', exist_ok=True)

    # Save as JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Data saved to {output_file}")

    # Print first few rows as example
    print("\nFirst 3 rows:")
    for i, row in enumerate(data[:3]):
        print(f"\nRow {i+1}:")
        print(f"  Letter: {row['letter']}")
        print(f"  Examples: {row['examples'][:20] if len(row['examples']) > 20 else row['examples']}")
        print(f"  Phonetic: {row['phonetic']}")
        print(f"  Putian: {row['dialectValues'][0]}")
        print(f"  Xianyou: {row['dialectValues'][11]}")
        print(f"  RowSpan: {row['rowSpan']}")
        print(f"  HasBorder: {row['hasBorder']}")

if __name__ == '__main__':
    main()
