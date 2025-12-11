#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成頁碼對應表輔助工具
分析 PDF 或文本，提供初步的章節-頁碼對應建議
"""

import json
import re
from typing import List, Dict

def analyze_text_structure(hanci_file: str) -> List[Dict]:
    """
    分析文本結構，提取書卷和章節資訊
    """
    with open(hanci_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    structure = []
    current_book = None
    current_chapter = None
    line_num = 0

    for line in lines:
        line_num += 1

        # 移除行號前綴
        content = line.split('→', 1)[-1].strip() if '→' in line else line.strip()

        if not content:
            continue

        # 檢查是否是章節引用
        verse_match = re.match(r'(\d+):(\d+)', content)

        if verse_match:
            chapter = int(verse_match.group(1))
            verse = int(verse_match.group(2))

            # 新的章
            if current_chapter is None or current_chapter['chapter'] != chapter:
                if current_chapter:
                    current_chapter['line_end'] = line_num - 1

                current_chapter = {
                    'chapter': chapter,
                    'line_start': line_num,
                    'line_end': None,
                    'first_verse': verse
                }

                if current_book:
                    current_book['chapters'].append(current_chapter)

        else:
            # 可能是書卷名稱或標題
            if len(content) < 15 and not re.search(r'[。，]', content):
                # 新書卷
                if current_chapter:
                    current_chapter['line_end'] = line_num - 1

                current_book = {
                    'name': content,
                    'line_start': line_num,
                    'chapters': []
                }
                structure.append(current_book)
                current_chapter = None

    # 結束最後一章
    if current_chapter:
        current_chapter['line_end'] = line_num

    return structure

def generate_mapping_template(structure: List[Dict], output_file: str = 'page-mapping.csv'):
    """
    生成頁碼對應範本 CSV
    """
    with open(output_file, 'w', encoding='utf-8-sig') as f:
        # 寫入標題行
        f.write('書卷名稱,章,節起,節迄,頁碼起,頁碼迄,行號起,行號迄,備註\n')

        for book in structure:
            book_name = book['name']

            for chapter in book['chapters']:
                chapter_num = chapter['chapter']
                line_start = chapter['line_start']
                line_end = chapter['line_end'] or ''

                # 留空頁碼，供手動填寫
                f.write(f'{book_name},{chapter_num},,,,,{line_start},{line_end},\n')

    print(f"[OK] 已生成頁碼對應範本：{output_file}")
    print(f"  共 {len(structure)} 卷")
    print(f"  共 {sum(len(book['chapters']) for book in structure)} 章")
    print("\n請根據以下資訊填寫頁碼：")
    print("1. 打開 page-mapping.csv")
    print("2. 對照 PDF 掃描檔或圖片")
    print("3. 填寫每章對應的頁碼起迄（如：0001, 0005）")
    print("4. 儲存後即可使用")

def generate_html_editor(structure: List[Dict], output_file: str = 'page-mapping-editor.html'):
    """
    生成 HTML 視覺化編輯器
    """
    html_template = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>興化語聖經 - 頁碼對應編輯器</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: "Noto Sans TC", "Microsoft JhengHei", sans-serif;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 { margin-bottom: 20px; color: #333; }
        .instructions {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #2196F3;
            color: white;
            font-weight: 500;
        }
        input {
            width: 100%;
            padding: 6px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .btn {
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 20px;
        }
        .btn:hover { background: #45a049; }
        .book-section {
            background: #f9f9f9;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📖 興化語聖經 - 頁碼對應編輯器</h1>
        <div class="instructions">
            <h3>使用說明：</h3>
            <ol>
                <li>在右側「頁碼起」和「頁碼迄」欄位填寫對應的圖片檔名（如：0001, 0005）</li>
                <li>填寫完成後點擊「匯出 CSV」按鈕</li>
                <li>將匯出的內容儲存為 page-mapping.csv</li>
            </ol>
        </div>

        <table id="mappingTable">
            <thead>
                <tr>
                    <th>書卷</th>
                    <th>章</th>
                    <th>行號起</th>
                    <th>行號迄</th>
                    <th>頁碼起</th>
                    <th>頁碼迄</th>
                    <th>備註</th>
                </tr>
            </thead>
            <tbody id="tableBody">
                <!-- 將由 JavaScript 生成 -->
            </tbody>
        </table>

        <button class="btn" onclick="exportCSV()">📥 匯出 CSV</button>
    </div>

    <script>
        const structure = ''' + json.dumps(structure, ensure_ascii=False) + ''';

        function renderTable() {
            const tbody = document.getElementById('tableBody');
            let html = '';

            structure.forEach(book => {
                // 書卷標題行
                html += `
                    <tr class="book-section">
                        <td colspan="7">${book.name}</td>
                    </tr>
                `;

                // 各章
                book.chapters.forEach(chapter => {
                    html += `
                        <tr>
                            <td>${book.name}</td>
                            <td>${chapter.chapter}</td>
                            <td>${chapter.line_start}</td>
                            <td>${chapter.line_end || ''}</td>
                            <td><input type="text" class="page-start" placeholder="0001" /></td>
                            <td><input type="text" class="page-end" placeholder="0005" /></td>
                            <td><input type="text" class="note" placeholder="備註" /></td>
                        </tr>
                    `;
                });
            });

            tbody.innerHTML = html;
        }

        function exportCSV() {
            let csv = '書卷名稱,章,節起,節迄,頁碼起,頁碼迄,行號起,行號迄,備註\\n';

            const rows = document.querySelectorAll('#tableBody tr:not(.book-section)');
            rows.forEach(row => {
                const cells = row.querySelectorAll('td, input');
                const bookName = cells[0].textContent;
                const chapter = cells[1].textContent;
                const lineStart = cells[2].textContent;
                const lineEnd = cells[3].textContent;
                const pageStart = cells[4].value;
                const pageEnd = cells[5].value;
                const note = cells[6].value;

                csv += `${bookName},${chapter},,,${pageStart},${pageEnd},${lineStart},${lineEnd},${note}\\n`;
            });

            // 下載 CSV
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'page-mapping.csv';
            link.click();
        }

        // 初始化
        renderTable();
    </script>
</body>
</html>
'''

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"\n[OK] 已生成視覺化編輯器：{output_file}")
    print("  請用瀏覽器開啟此檔案，即可視覺化編輯頁碼對應")


if __name__ == '__main__':
    print("分析文本結構...")
    structure = analyze_text_structure('hanci.txt')

    print("\n生成輔助工具...")
    generate_mapping_template(structure)
    generate_html_editor(structure)

    print("\n[DONE] 完成！")
