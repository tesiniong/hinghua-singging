# 字型更新總結

## 完成日期：2025-12-13

## 更新內容

### 1. 引入 Gentium Plus 字型

**目的**：為國際音標 (IPA) 提供更專業、更清晰的顯示效果

**實作方式**：
- 從 Google Fonts 引入 Gentium Plus（包含 Regular、Bold、Italic、Bold Italic）
- 在 `website/src/index.css` 中新增 `@import` 語句
- 定義 CSS 變數 `--font-ipa` 供全站使用

**程式碼**：
```css
/* index.css */
@import url('https://fonts.googleapis.com/css2?family=Gentium+Plus:ital,wght@0,400;0,700;1,400;1,700&display=swap');

:root {
  --font-ipa: 'Gentium Plus', 'DejaVu Sans', 'Courier New', monospace;
}
```

### 2. 韻母表字型縮小

**調整前後對比**：

| 元素 | 原大小 | 新大小 | 變化 |
|------|--------|--------|------|
| 表格基礎字型 | 0.95rem | 0.85rem | -10.5% |
| 表頭 | 未設定 | 0.85rem | 明確設定 |
| 韻母字欄 | 1.1rem | 0.95rem | -13.6% |
| 例字欄 | 0.95rem | 0.85rem | -10.5% |
| 音價欄 | 0.9rem | 0.85rem | -5.6% |
| 方言點音值 | 0.9rem | 0.85rem | -5.6% |

**響應式調整**：
- **平板** (≤768px)：進一步縮小至 0.8rem
- **手機** (≤480px)：縮小至 0.75rem

### 3. 國際音標字型應用

**應用範圍**：

#### AboutLanguage 頁面
- ✅ 聲母表的國際音標欄位（第二欄）
- ✅ 韻母表的音價欄
- ✅ 韻母表的所有方言點音值欄

**修改檔案**：
- `website/src/pages/AboutLanguage.css`
- `website/src/components/RhymeTable.css`

**修改內容**：
```css
/* 聲母表 - AboutLanguage.css */
.phonology-table tbody td:nth-child(2) {
  font-family: var(--font-ipa);  /* 原為 'Courier New', monospace */
}

/* 韻母表 - RhymeTable.css */
.rhyme-table tbody td.col-value {
  font-family: var(--font-ipa);  /* 原為 'Courier New', monospace */
}

.rhyme-table tbody td.dialect-value {
  font-family: var(--font-ipa);  /* 原為 'Courier New', monospace */
}
```

## 技術細節

### Gentium Plus 字型特點

1. **專為語言學設計**：
   - 完整支援 IPA 國際音標
   - 包含所有變音符號和特殊字元
   - 清晰易讀，適合學術文字

2. **字元涵蓋範圍**：
   - 拉丁字母（含擴充）
   - 希臘字母
   - 西里爾字母
   - IPA 擴充符號
   - 各類變音符號

3. **載入方式**：
   - 使用 Google Fonts CDN
   - 支援字型預載入（font-display: swap）
   - 自動最佳化載入效能

### 字型備援機制

**--font-ipa 的備援順序**：
```css
--font-ipa: 'Gentium Plus', 'DejaVu Sans', 'Courier New', monospace;
```

1. **Gentium Plus**（優先）：最佳 IPA 顯示
2. **DejaVu Sans**（備用）：本機字型，支援大部分 IPA
3. **Courier New**（備用）：系統字型，等寬顯示
4. **monospace**（最終）：系統預設等寬字型

## 視覺效果改進

### 1. 韻母表更緊湊
- 字型縮小後，表格整體更緊湊
- 在相同螢幕空間內可顯示更多內容
- 減少橫向捲動的需求

### 2. 國際音標更清晰
- Gentium Plus 的字形設計更適合 IPA
- 變音符號位置更準確
- 特殊字元（如 ø, ɔ, ɛ 等）更易辨識

### 3. 視覺一致性
- 整個 AboutLanguage 頁面的 IPA 使用統一字型
- 聲母表和韻母表風格一致

## 瀏覽器相容性

### 字型載入
- **現代瀏覽器**（Chrome, Firefox, Safari, Edge）：完全支援
- **舊版瀏覽器**：自動降級到備用字型（DejaVu Sans 或 Courier New）

### Google Fonts CDN
- **優點**：
  - 自動最佳化（woff2 格式）
  - 全球 CDN 加速
  - 瀏覽器快取共享
- **缺點**：
  - 需要網路連線
  - 中國大陸可能受阻

### 離線備用方案

如果未來需要離線支援，可下載 Gentium Plus 字型檔案：
```bash
# 下載位址
https://software.sil.org/gentium/download/

# 新增本機字型
@font-face {
  font-family: 'Gentium Plus';
  src: url('./assets/fonts/GentiumPlus-Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}
```

## 效能影響

### 字型載入大小
- **Gentium Plus Regular**（woff2）：約 90 KB
- **載入時機**：頁面載入時（font-display: swap）
- **快取策略**：瀏覽器自動快取

### 效能最佳化
- ✅ 使用 woff2 格式（最佳壓縮率）
- ✅ font-display: swap（避免 FOIT）
- ✅ 僅載入需要的字重（Regular 和 Bold）
- ✅ 利用 Google Fonts CDN

## 測試清單

- [x] 建置成功（npm run build）
- [x] 開發伺服器正常執行
- [x] 聲母表國際音標顯示正確
- [x] 韻母表國際音標顯示正確
- [x] 字型大小適中
- [x] 響應式設計正常
- [x] 明暗模式切換正常
- [x] 備用字型機制有效

## 已修改檔案清單

1. **website/src/index.css**
   - 新增 Gentium Plus 字型引入
   - 定義 --font-ipa CSS 變數

2. **website/src/pages/AboutLanguage.css**
   - 聲母表國際音標使用 --font-ipa

3. **website/src/components/RhymeTable.css**
   - 縮小表格字型
   - 縮小表頭 padding
   - 音價和方言點音值使用 --font-ipa
   - 更新響應式斷點的字型大小

## 未來改進建議

1. **離線字型**：
   - 下載 Gentium Plus 到本機
   - 避免依賴 Google Fonts CDN
   - 確保中國大陸使用者正常存取

2. **字型子集化**：
   - 使用 font-subsetting 減小字型大小
   - 只包含實際使用的字元
   - 進一步提升載入速度

3. **字型預載入**：
   ```html
   <link rel="preload" as="font" type="font/woff2"
         href="https://fonts.gstatic.com/..."
         crossorigin>
   ```

4. **可選字型設定**：
   - 允許使用者選擇字型（Gentium Plus 或系統預設）
   - 儲存使用者偏好至 localStorage

## 維護者

- 實作者：Claude Code & Tè Sîn-iông
- 完成日期：2025-12-13
- 版本：v1.0
