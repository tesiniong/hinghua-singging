# 前端架構

## 元件樹

```
src/
├── App.jsx                    路由容器（BrowserRouter + Routes）+ 頁尾統計
├── pages/
│   ├── Home.jsx               首頁：標題區塊 + BibleReader
│   ├── AboutBible.jsx         聖經介紹（含自動計算的進度表）
│   ├── AboutLanguage.jsx      語音介紹（含韻母表）
│   ├── HomophoneTable.jsx     同音字表
│   └── RomToHanConverter.jsx  羅馬字轉漢字
├── components/
│   ├── Navbar.jsx             導航欄（捲動自動隱藏／顯示）
│   ├── ThemeToggle.jsx        主題切換
│   ├── BibleReader.jsx        主閱讀器（狀態集中處）
│   ├── BookSelector.jsx       書卷／章節選擇
│   ├── ModeSelector.jsx       閱讀模式切換
│   ├── DualColumn.jsx         雙欄模式
│   ├── RubyMode.jsx           Ruby 模式
│   ├── SingleLanguage.jsx     單語言模式
│   ├── SearchBox.jsx          搜尋
│   ├── ImageViewer.jsx        掃描圖檢視器（獨立入口 viewer.html）
│   └── RhymeTable.jsx         韻母表
└── utils/
    └── romanization.js        平話字 ↔ 輸入式轉換、搜尋折疊（共用）
```

## 路由

| 路徑 | 頁面 |
|------|------|
| `/` | 首頁（聖經閱讀器） |
| `/about-bible` | 聖經介紹 |
| `/about-language` | 莆仙語音系介紹 |
| `/homophone-table` | 同音字表 |
| `/rom-to-han-converter` | 羅馬字轉漢字 |

用 `BrowserRouter`（網址無 `#`），因此 GitHub Pages 需要 spa-github-pages 方案：
`public/404.html` 把路徑存入 `sessionStorage` 並導回首頁，`index.html` 讀回後用
`history.replaceState()` 還原路由。

**注意**：`public/` 的檔案不經 Vite 處理，`404.html` 內的資源路徑必須自己帶
`/hinghua-singging/` 前綴。

---

## 三種閱讀模式

### 雙欄（Dual-Column）
左羅馬字、右漢字，每節一行。直接用 `verse.rom` / `verse.han` 渲染。

### Ruby 注音
羅馬字以 `<ruby>` 標在漢字上方，同章連續排列。**唯一使用 `verse.tokens` 的模式**，
因為需要精確的字元—音節對齊。

- 標點只用漢字標點，移除羅馬字標點（保留連字號），不顯示合音字的「」
- 換行以漢字版的位置為準：先找出 `verseHan` 中所有換行符位置，
  換算成「不含換行符的累積字元數」，再於渲染時插入 `<br>`

### 單一語言
只顯示一種文字，全章連續排版（像紙本聖經）。羅馬字模式在句子間自動補空格。

節號用 `<span>` + `vertical-align: super` + `line-height: 0`，**不用 `<sup>`**——
`<sup>` 會撐高行高，導致每節被迫換行。

英文序（Foreword）只有羅馬字，`BibleReader` 在 render 期間推導出 `rom-only`
模式，`ModeSelector` 同時停用其他按鈕；離開該書卷後會回到使用者原本選的模式。

---

## 搜尋

`SearchBox` 搭配 `utils/romanization.js`。核心想法是**把查詢與經文折疊成同一種可比對的形式**。

- **輸入式自動處理**，不是額外的開關：平話字 `Siō̤ng-Da̤̍` 與輸入式 `sioong5-daa4`
  折疊後相同，兩種打法是同一個搜尋。
- **精確／模糊**是唯一的控制項。精確保留聲調與變韻的區別；
  模糊把兩者都抹掉，因此 `siong` 找得到 `Siō̤ng`、`tinn` 找得到 `tiⁿ`。

這兩件事互相正交，所以不需要 2×2 的勾選組合。

實作細節：

- 音節之間以單一空格相接，連字號與空格因此等價，同時避免跨音節的假命中
- 命中時高亮**整個音節**——只標半個音節會把調符切開
- 折疊在資料載入時做一次（5786 節約 77 ms），不隨每次按鍵重算
- 輸入有 180 ms 緩衝，結果最多渲染 200 筆但回報真實總數

---

## 其他功能

**書卷選擇器**：網格式（4 欄），依聖經順序排列，無內容的書卷與章節顯示為停用。
章節選單 `z-index: 300` 覆蓋書目選單，一行 10 個（平板 8、手機 6）。

**掃描圖檢視**：經節旁的 📖 連到 `viewer.html?page=NNNN`，支援縮放（按鈕、滾輪）
與拖曳平移。頁碼由 `page-ocr-results.json` 反查。

**導航欄**：固定頂端，向下捲動時滑出、向上捲動時滑入，頂部 10px 內恆顯示。
選單在點擊連結、點擊外部、或導航欄因捲動而隱藏時收合（滑鼠移開不收合）。

**主題**：明亮／黑暗／跟隨系統。以 CSS 變數搭配 `[data-theme="dark"]` 切換，
選擇存於 `localStorage`，系統模式監聽 `prefers-color-scheme`。

**韻母表**：16 個方言點可選（預設莆田、仙遊），表頭與第一欄 sticky，支援合併儲存格。

---

## 字體

| 用途 | 字體 | 備用 |
|------|------|------|
| 漢字 | Noto Sans TC | Tauhu-oo, sans-serif |
| 羅馬字 | DejaVu Sans | Arial, sans-serif |
| 國際音標 | Gentium Plus | DejaVu Sans, monospace |

羅馬字用 DejaVu Sans 是因為它完整覆蓋平話字的組合變音符號；
TauhuOo 缺 U+0324（下圓點）與 U+1E72（Ṳ），單獨使用會出現豆腐格。

基礎字級桌面 20px、行動 18px，行高 1.8；Ruby 羅馬字 0.6em / 0.55em。

漢字與羅馬字的字型檔都在倉庫內（`website/src/assets/fonts/`），只有國際音標用的
**Gentium Plus 是從 Google Fonts CDN 載入**（`src/index.css` 的 `@import`）——
這是全站唯一的外部資源依賴，在中國大陸可能取不到，屆時會退回 DejaVu Sans。
若要完全離線，需把 Gentium Plus 下載進 `assets/fonts/` 並改用 `@font-face`。

---

## 技術決策

**為何文本用 Markdown 格式**：層級清楚、易於手動編輯、每節一行便於 diff 與比對。
代價是從 WPS 複製來的文本需要 `format_han.py` 整理。

**為何用 `page-ocr-results.json` 而非 `chapter-page-mapping.json`**：
前者記錄每頁的起始經節，能正確處理跨頁的章節，且所有經節都找得到對應頁面。

**為何用 `sections` 而非 `verses`**：需要容納段落小標，且便於日後擴充（詩歌、旁註等）。

**為何只有 Ruby 模式用 tokens**：其他模式直接顯示完整句子，用 token 拼接反而
會造成字距不一致。

**節內換行**：JSX 會把 `\n` 當成一般空白，因此解析時保留換行符，三種模式各自
用對應的函式轉成 `<br>`。換行位置一律以漢字版為準。

**Unicode 正規化**：前後端都用 NFC，避免變音符號順序不同導致比對失敗。
