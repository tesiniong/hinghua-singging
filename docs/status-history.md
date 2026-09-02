# 歷史進度紀錄

Append-only。新的紀錄加在最上面，**不要修改或刪除既有條目**。

任何含日期的進度敘述都寫在這裡，`CLAUDE.md` 只描述現況。
`CLAUDE.md` 的「當前狀態」被覆寫掉的內容，若值得留存就搬到這裡。

格式：一則一個 `## YYYY-MM-DD 標題`，內容以「做了什麼、為什麼」為主，
不要貼完整的程式碼或測試清單——那些看 git 歷史。

---

## 2026-09-02 例行維護：清理、修正與工作流重整

本機落後遠端 27 個 commit，同步後對整個專案做了一輪稽核與修整。

- **倉庫清理**：移除誤加的 `data/20251206175847.pdf`、巢狀的 `website/website/`、
  版控中的 `__pycache__`；補上 `LICENSE`（MIT）與 `NOTICE.md`
  （文本 CC BY 4.0、字型 OFL／Bitstream Vera）。原本散佈 OFL 字型卻無任何授權聲明。
- **SEO 與圖示**：canonical 網址原本是 `https://github.io/...`（少了使用者名稱），
  指向不存在的網域；favicon 仍是 Vite 預設圖；宣告了 `summary_large_image`
  卻沒有 og:image。三者都補齊，圖示由 `scripts/build/site_icons.py` 生成。
- **移除首頁的隱藏區塊**：原本以 `display:none` 藏著一段「保留給搜尋引擎」的文字，
  屬於 cloaking，且內容是聖經介紹頁的劣化重複版。
- **程式碼**：修掉 `BookSelector` 在提前 return 之後呼叫 Hook 的問題；
  清掉全部 23 個 lint 錯誤，其中四個「在 effect 內同步 state」改為 render 期間推導
  或移到事件處理器。
- **搜尋**：新增精確／模糊切換與輸入式羅馬字支援。原本必須打得出調符才搜得到
  羅馬字，等於半部語料無法檢索。
- **工作流重整**：15 支平鋪的腳本分成 `scripts/build/` 與 `scripts/tools/`，
  新增單一入口 `scripts/build_all.py`。舊腳本依賴當前工作目錄，換個目錄執行會
  默默讀寫錯檔案，現在統一經由 `scripts/_paths.py`。
- **修好 `incremental_update.py`**：`parse_text_v4.py` 更名為 `build_bible_data.py`
  時沒更新它的 import，此後每次執行都是 ModuleNotFoundError。
- **建置可重現**：`rom_to_han_dict.py` 直接走訪 `set` 決定輸出順序，
  連跑三次得到三個不同的檔案。排序後才讓 CI 能比對產物。
- **CI**：加入 lint 與「生成資料是否與來源文本同步」的檢查，PR 也會跑。
- **文件**：`CLAUDE.md` 從 29 KB 縮到 4.4 KB，細節移入 `docs/`，並訂出維護規則。

`chapter-page-mapping.json` 順帶修正了兩個鍵：馬太與馬可先前仍寫作「瑪太」「瑪可」，
與 `book_info.py`、`han.txt` 不一致。

---

## 2025-12-13 引入 Gentium Plus，調整韻母表字級

為國際音標引入 Gentium Plus（Google Fonts CDN 載入），定義 `--font-ipa`
變數並套用於聲母表的音標欄、韻母表的音價欄與各方言點音值欄。
備援順序為 Gentium Plus → DejaVu Sans → Courier New → monospace。

同時縮小韻母表字級（基礎 0.95rem → 0.85rem，韻母字欄 1.1rem → 0.95rem），
平板降至 0.8rem、手機 0.75rem，減少橫向捲動。

未做、留待日後：把 Gentium Plus 下載至本機以擺脫 CDN 依賴
（中國大陸使用者可能取不到）、字型子集化。

## 2026-09-02 羅馬字 OCR 管線

- 評估三條路（微調通用 OCR／專用模型／視覺語言模型）後採 kraken 專用模型；訓練資料由 PaddleOCR 零樣本輸出對齊 `rom.txt` 自動產生。
- 三階段訓練後測試頁行級 CER 1.6%；創世記 1–20 章端到端逐節 CER 3.5%、82% 的節兩個字元內可修好。
- 切節靠頁面對應表的節號序列、上標數字的編輯距離對齊，以及「漢字版字數＝羅馬字音節數」的長度限制。
- 創世記 21–33 章（467 節）由 OCR 填入 `rom.txt`，待校對；細節見 `docs/ocr.md`。
