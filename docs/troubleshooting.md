# 故障排除

## 資料與建置

**改了經文但網站沒變**
沒有重新建置。跑 `python scripts/build_all.py`。CI 會擋這種情況，但本機開發不會。

**書目順序錯誤，或整卷書沒出現**
書名不在 `scripts/book_info.py` 的對照表中，或拼寫與對照表不完全一致。
建置時終端會印出「在 han.txt 和 rom.txt 中均未找到，已跳過」。

**章節標題顯示「第4章」而非「第四章」**
資料是用舊版腳本產生的。重跑建置，確認 `bible_data.json` 有 `chapter_title_han` 欄位。

**建置產物每次都不一樣**
腳本裡有非決定性的走訪順序（例如直接迭代 `set` 決定輸出順序）。
這會讓 CI 的一致性檢查每次都失敗，必須加上 `sorted()`。

**腳本讀寫到錯的檔案**
應該不會再發生——所有腳本都經由 `scripts/_paths.py` 定位。
若新增腳本，請沿用同一模式，不要寫死相對路徑。

## 顯示

**經節旁沒有 📖 圖示**
`data/page-ocr-results.json` 中沒有該章節的記錄。手動補上該章第一節所在的頁碼。

**📖 連到錯誤的頁面**
早期 OCR 誤判。修正 `page-ocr-results.json` 中的對應頁碼後重新建置。

**Ruby 模式羅馬字黏在一起**
`RubyMode.css` 的字距設定。目前是 margin-right 0.15em + letter-spacing 0.05em。

**Ruby 模式換行位置錯誤**
混淆了「原始字串中的位置」與「不含換行符的累積字元數」。
換行符位置必須換算成後者才能正確插入 `<br>`。

**詩歌體經文的換行失效**
JSX 把 `\n` 當成一般空白。三種模式各有對應的換行處理函式，確認有走到。

**單語言模式每節都被迫換行**
用了 `<sup>` 標籤，它會撐高行高。改用 `<span>` +
`vertical-align: super` + `line-height: 0`。

**標點符號被當成單字**
該標點不在 `scripts/build/bible_data.py` 的識別清單中，補進去。

**羅馬字出現豆腐格（□）**
字型缺少該組合變音符號的字符。覆蓋率見 [romanization.md](romanization.md)。

## 部署

**直接開子頁面出現 404**
GitHub Pages 對 SPA 的限制。確認 `website/public/404.html` 存在，
且 `index.html` 內的 `sessionStorage` 還原腳本正常。

**`public/` 裡的資源在線上 404**
`public/` 的檔案不經 Vite 處理，不會自動加上 base path。
這些檔案內的絕對路徑必須自己寫成 `/hinghua-singging/…`。

**PDF 打不開，只有一百多 bytes**
那是 Git LFS 指標檔，內容沒下載。裝好 `git-lfs` 後執行 `git lfs install && git lfs pull`。
**沒裝 LFS 時不要編輯或提交 PDF**，會把指標檔弄壞。

---

# 已知限制

1. **資料不完整**：163 章中約 36 章尚無內容；多數已錄入的章節只有羅馬字或只有漢字，
   雙欄與 Ruby 模式在這些章節只有半邊。
2. **OCR 覆蓋率約一半**：未識別的頁面需手動補進 `page-ocr-results.json`，
   否則該章節沒有 📖 圖示。
3. **Token 對齊的前提**：假設 1 漢字 ↔ 1 羅馬字音節，合音字要靠 `「」` 特別標記。
4. **圖片體積**：WebP 共約 270 MB 且納入版控，倉庫 `.git` 已接近 300 MB。
   GitHub Pages 站台上限 1 GB、每月流量 100 GB，目前尚可，但重新處理圖片會讓倉庫快速膨脹。
