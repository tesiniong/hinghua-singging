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
| `verse.rom_draft` | 只在羅馬字是 OCR 草稿的節出現：校對旗標陣列（可為空陣列），來自 `ocr-draft.json` |
| `chapter.draft_verses` / `chapter.draft_flagged` | 只在本章含草稿時出現：草稿節數、其中有旗標的節數 |

所有 token 都有 `han` 與 `rom` 欄位（其中一個可能是空字串），前端統一用這兩個欄位處理。

單一章節可能只有羅馬字或只有漢字——多數章節目前如此。前端須容忍任一邊為空。

---

## `ocr-draft.json`

由掃描頁 OCR 填入 `rom.txt`、**尚未人工校對**的節（見 [ocr.md](ocr.md)「辨識草稿」）。
鍵是英文書名與「章:節」，值是 `assemble.py` 給的校對旗標；沒有旗標的節是空陣列。

```json
{
 "Genesis": {
  "21:1": ["首節（首字放大）"],
  "21:2": []
 }
}
```

`assemble.py --write` 填入經文時自動加入，校對完用 `scripts/tools/ocr/draft.py --clear` 移除。
`bible_data.py` 據此在 `bible_data.json` 標 `rom_draft`，網站顯示「OCR 辨識草稿，未經校對」；
`rom_to_han_dict.py`、`homophone_table.py` 與 OCR 訓練標籤都不採用草稿節。
`stats.json` 的 `rom.*.draft_verses` 是各約羅馬字節數中屬於草稿的數量。

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

## `hinghua-finals.txt`

興化平話字所有合法的「韻母＋聲調」組合（230 個，NFC，一行一個），由使用者的生成器
`~/projects/wiktionary-scripts/python-scripts/hinghwa2.py` 產生；調符位置的規則都在裡面
（例如 a̤uh 的調符標在 u 上、-h 韻尾不配尖音符）。乘上 15 個聲母得到 3,420 個合法音節，
供 `scripts/tools/check_rom_syllables.py` 檢查正本，也供 OCR 解碼限制輸出。

## 未納入建置流程的參考檔

`data/` 底下有兩個檔案目前沒有被任何腳本或前端讀取，保留作參考：

| 檔案 | 內容 |
|------|------|
| `bible-verse-count.json` | 66 卷書逐章的節數（含英文書名與簡稱）。`book_info.py` 的章節數應該源自於此。 |
| `vocab_from_bible.yaml` | Rime 格式的詞庫，註明是「從興化平話字聖經提取的詞彙」。與建置用的 `borhlang_bannuaci.dict.yaml` 不同，後者才是轉換字典的來源。 |

若確認不再需要，可以刪除；若日後要用，請在這裡補上用途說明。

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
