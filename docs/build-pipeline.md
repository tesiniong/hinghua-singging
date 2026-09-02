# 建置流程

所有腳本都以 `scripts/_paths.py` 定位檔案，**從任何工作目錄執行都可以**。

## 一鍵建置

```bash
python scripts/build_all.py           # 全部步驟
python scripts/build_all.py --list    # 只列出步驟
python scripts/build_all.py --only bible_data
python scripts/build_all.py --skip site_icons
```

步驟依序執行，前一步的產物是後一步的輸入：

| 步驟 | 腳本 | 產出 | 相依 |
|------|------|------|------|
| `bible_data` | `scripts/build/bible_data.py` | `bible_data.json`、`bookList.json`、`stats.json` | 標準函式庫 |
| `rom_to_han_dict` | `scripts/build/rom_to_han_dict.py` | `romToHanDict.json` | 標準函式庫 |
| `homophone_table` | `scripts/build/homophone_table.py` | `homophoneData.json` | 標準函式庫 |
| `rhyme_table` | `scripts/build/rhyme_table.py` | `rhymeTableData.json` | `openpyxl` |
| `site_icons` | `scripts/build/site_icons.py` | favicon、`og-image.png` | `Pillow` |

後兩步的來源極少變動，缺少套件時會被跳過而不中斷流程。

**建置必須可重現。** CI 會重跑前三步並比對產物，有差異就讓 workflow 失敗——
這是用來擋「改了經文卻忘記重建」的情況。若修改腳本，注意不要引入非決定性
（例如直接走訪 `set` 來決定輸出順序）。

## 各腳本說明

### `scripts/build/bible_data.py` — 主建置腳本

**輸入**：`data/rom.txt`、`data/han.txt`、`data/foreword-en.txt`、`data/foreword-cpx.txt`
**輸出**：`data/bible_data.json`、`data/bookList.json`、`website/public/stats.json`，
並把相關 JSON 複製到 `website/public/`。

處理流程：

1. 解析序言（特殊格式，以段落為單位，不分章節）
2. 以 `scripts/book_info.py` 的對照表匹配書名
3. Token 層級對齊（1 漢字 ↔ 1 羅馬字音節）
4. 處理合音字（`「」`）與專名（`{}`）
5. 生成章節標題（中文數字 + 羅馬字）
6. 生成舊約／新約進度統計

核心函數：

- `tokenize_han()`：識別漢字中夾雜的羅馬字，拆為 `rom_in_han` token
- `align_tokens()`：以羅馬字詞為單位消耗對應的漢字單元
- Unicode NFC 正規化：解決組合字元順序不一致的比對問題

### `scripts/book_info.py` — 書目對照表（共用）

66 卷聖經 + 2 篇序言的羅馬字／漢字／英文名稱、簡稱、起始頁碼、章數、每章節數。
提供 `HAN_TO_ROM`、`ROM_TO_HAN`、`HAN_TO_ENG` 對照表與 `get_book_by_page()`、
`get_book_index()`。**新增書卷前，書名必須先出現在這裡。**

### `scripts/romanization_converter.py` — 平話字轉換（共用）

平話字 ↔ 輸入式的後端轉換邏輯，由 `rom_to_han_dict.py` 使用。
前端的對應實作在 `website/src/utils/romanization.js`——**兩邊都改到時要保持一致**。
對照規則見 [romanization.md](romanization.md)。

### `scripts/build/rom_to_han_dict.py`

**輸入**：`data/borhlang_bannuaci.dict.yaml`（輸入法詞典）、`data/bible_data.json`（詞頻）
**輸出**：`website/public/romToHanDict.json`（約 2.3 MB）

詞頻策略：優先採用聖經統計的真實詞頻；詞典有而聖經沒有的詞設為 1；
多音節詞的漢字詞頻按比例分配（2 字詞各 +0.5，3 字詞各 +0.333…）。

合音字（`dai4`→「第一」、`gai4`→「家己」、`dau4`→「豆腐」、`noong2`→「那當」）
先檢查漢字部分，有匹配才消耗多個漢字。

### `scripts/build/homophone_table.py`

**輸入**：`data/cpx-pron-data.lua`（維基詞典發音資料）、`data/bible_data.json`
**輸出**：`data/bible-han-rom-pairs.yaml`（中間檔，可人工編輯）、`website/public/homophoneData.json`
**參數**：預設合併現有資料；`--rebuild-bible-data` 重新從 `bible_data.json` 提取。

### `scripts/build/rhyme_table.py`

`data/hinghua_rhymes.xlsx` → `website/src/data/rhymeTableData.json`。
Excel 中以 `_xxx_` 標記底線，會轉成 HTML `<u>`。

### `scripts/build/site_icons.py`

用倉庫內既有的字型產生 favicon 與 1200×630 社群預覽圖。
平話字那行用 DejaVu Sans——TauhuOo 缺 U+0324 與 U+1E72，會出現豆腐格。

### `scripts/tools/`

一次性或手動執行的工具，不在 `build_all` 流程內：

| 腳本 | 用途 |
|------|------|
| `ocr_page_numbers.py` | OCR 掃描頁的章節號 → `page-ocr-results.json`（需 pytesseract） |
| `regenerate_chapter_mapping.py` | 手動改過 `page-ocr-results.json` 後重生對應表 |
| `format_han.py` | 把 WPS 複製出來的文本整成 Markdown 格式 |
| `incremental_update.py` | 比對兩個版本的文本，產生變更報告 |
| `convert_images.py` / `rename_images.py` | TIF → WebP、批次重新命名 |
| `add_bookmarks.py` | 為 PDF 加書籤 |
| `check_quotes.py` | 檢查 Unicode 引號是否被正確判為標點 |
| `ocr/` | 掃描頁羅馬字 OCR：訓練資料產生、辨識、切節、填入 `rom.txt`，見 [ocr.md](ocr.md) |

---

## 更新經文的完整步驟

### 1. 編輯文本

編輯 `data/rom.txt` 與 `data/han.txt`（格式見 [data-format.md](data-format.md)）。
新書卷的書名必須已存在於 `scripts/book_info.py`。

### 2. 建置

```bash
python scripts/build_all.py
```

確認終端輸出：新章節有被解析、書目順序正確、統計數字合理。

### 3. 補頁面對應（若需要）

新章節若尚未出現在 `data/page-ocr-results.json`，經節旁不會有 📖 圖示。
手動加入該章第一節所在的頁碼：

```json
{
  "0123": {
    "chapter": 50,
    "verse": 1,
    "book_rom": "Cho̤̍ng-sa̤-gi̍",
    "book_han": "創世記",
    "book_english": "Genesis"
  }
}
```

然後重跑步驟 2。

### 4. 測試

```bash
cd website && npm run dev
```

檢查新章節顯示正常、三種閱讀模式都對、📖 連結指向正確頁面。

### 5. 提交

來源文本與生成的資料檔要放在同一個 commit，否則 CI 的一致性檢查會失敗。

### 比對兩個版本的差異

```bash
git show HEAD~1:data/han.txt > /tmp/han_prev.txt
python scripts/tools/incremental_update.py /tmp/han_prev.txt data/han.txt changes_report.txt
```
