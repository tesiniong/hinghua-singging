# 資料格式

## 經文文本格式

`data/rom.txt` 與 `data/han.txt` 是手動維護的正本，使用 Markdown 風格的標記。

**羅馬字版 `rom.txt`**：

```markdown
# Cho̤̍ng-sa̤-gi̍
## 1
### 上帝其創造
1 Kî-táu Siō̤ng-Da̤̍ cho̤̍ng-cho̤̍ ting-dā̤.
2 Dā̤ sī ko̤ng-hṳ, o-bū-bū...
```

**漢字版 `han.txt`**：

```markdown
# 創世記
## 1
### 上帝其創造
1 起頭，上帝創造天地。
2 地是空虛，烏瞀々...
```

| 標記 | 用途 | 範例 |
|------|------|------|
| `#` | 書名 | `# 創世記` |
| `##` | 章號 | `## 1` |
| `###` | 段落小標 | `### 上帝其創造` |
| `{}` | 專名標記 | `{亞當}` → `proper_name: true` |
| `「」` | 合音字（多漢字對應一音節） | `「第一」` → da̍i |

- **音節分隔**：連字號 `-` 或空格
- **特殊符號**：含聲調符號（̤ ̍ ̄ ̆ ̂ ̃ 等），見 [romanization.md](romanization.md)
- **標點**：支援中文標點與 Unicode 引號
- 兩個文本各自解析後，透過 `scripts/book_info.py` 的書名對照表對齊。
  **書名拼寫必須與對照表完全一致**，否則該書卷會被跳過。

---

## `bible_data.json`

```json
{
  "books": [{
    "name_han": "創世記",
    "name_rom": "Cho̤̍ng-sa̤-gi̍",
    "name_eng": "Genesis",
    "chapters": [{
      "chapter": 1,
      "chapter_title_han": "第一章",
      "chapter_title_rom": "Dā̤ 1 Ca̤uⁿ",
      "sections": [
        { "type": "section_title", "han": "上帝其創造", "rom": "", "tokens": [] },
        {
          "type": "verse",
          "verse": 1,
          "han": "起頭，上帝創造天地。",
          "rom": "Kî-táu Siō̤ng-Da̤̍ cho̤̍ng-cho̤̍ ting-dā̤.",
          "tokens": [
            { "type": "word", "han": "起頭", "rom": "Kî-táu", "form": "phrase", "proper_name": false },
            { "type": "punct", "han": "，", "rom": "" }
          ]
        }
      ]
    }]
  }]
}
```

| 欄位 | 說明 |
|------|------|
| `name_eng` | 英文書名，取自 `book_info.py` |
| `sections` | 混合 `section_title` 與 `verse` 兩種項目 |
| `verse.rom` / `verse.han` | 完整經文，供雙欄與單語言模式直接渲染 |
| `verse.tokens` | Token 陣列，**僅** Ruby 模式使用 |
| `token.form` | `single`、`phrase`、`compound_single` |
| `token.proper_name` | 是否為專名 |

所有 token 都有 `han` 與 `rom` 欄位（其中一個可能是空字串），前端統一用這兩個欄位處理。

單一章節可能只有羅馬字或只有漢字——多數章節目前如此。前端須容忍任一邊為空。

---

## `page-ocr-results.json`

記錄每一掃描頁的**起始經節**，用來反查經節對應的掃描頁。

```json
{
  "0012": {
    "chapter": 3,
    "verse": 16,
    "book_rom": "Cho̤̍ng-sa̤̍-gi̍",
    "book_han": "創世記",
    "book_english": "Genesis"
  }
}
```

**查找邏輯**：取最後一個「起始位置 ≤ 目標經節」的頁面。
例如第 12 頁從 3:16 開始、第 13 頁從 4:17 開始，則 4:1–4:16 落在第 12 頁，4:17 之後落在第 13 頁。

此檔為**手動維護**，OCR 只涵蓋約半數頁面，其餘需要人工補。

`chapter-page-mapping.json` 由 `page-ocr-results.json` 衍生，網站只在序言頁用到它。

---

## `bookList.json`

書卷選擇器用的清單，含每卷的羅馬字／漢字／英文名、簡稱、章數、所屬約，
以及 `hasContent` 標記——沒有內容的書卷在選擇器中會顯示為停用。

---

## 掃描圖片

| 項目 | 說明 |
|------|------|
| 原始位置 | `pics/`（未提交至 Git） |
| 數量 | 1485 張 |
| 原始格式 | TIF（Group 4 壓縮，黑白二值），3980 × 5828 |
| 檔名 | `0001.tif` ～ `1485.tif` |
| 網站格式 | WebP（無損），約 270 MB，位於 `website/public/images/` |

前 8 張是封面、圖書館館藏章與序言，創世記 1:1 從第 0009 頁開始。
