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

---

## 2026-09-02 鏡像站（Cloudflare Pages）與字型本機化

主要受眾在莆田、仙遊，而 github.io 在中國大陸時常連不上；決定另建鏡像。
方案比較後排除境內託管（需 ICP 備案，且發布經文內容受《互聯網宗教信息服務管理辦法》
限制，個人無法取得許可），也不選阿里雲香港 OSS（不想在該處留金融資訊），
採 Cloudflare Pages 免費方案配 eu.org 免費網域。

- **base 參數化**：`vite.config.js` 的 base 與 `index.html`、`404.html` 內的絕對網址
  改由 `website/.env` 的 `VITE_BASE`、`VITE_SITE_URL` 提供，CI 以環境變數覆寫。
  `404.html` 從 `public/` 移到 `website/` 並列為 Vite 入口，圖示路徑不再手寫前綴。
- **字型**：Gentium Plus 改為本機 woff2（SIL 6.200 原版，Regular／Bold），移除 Google Fonts
  的 `@import`。這也修掉主站在大陸首次繪製會卡到 CDN 連線逾時的問題。
- **CI**：同一個 workflow 多建一次鏡像版並以 wrangler 部署；未設定 `CF_PAGES_PROJECT`
  時略過，行為與先前相同。同倉庫的 PR 會部署鏡像預覽版。
- **決定**：鏡像的 canonical 指向自己而非主站，否則百度會把讀者導回打不開的 github.io。

未做：網域與 Cloudflare、GitHub secrets 設定待專案擁有者完成（步驟見 deployment.md）；
網域下來前鏡像的 canonical 暫指 `<專案>.pages.dev`。

網域選項後來重查了一輪，結論與最初的假設不同：

- **js.org 與 is-a.dev 都不適用**。兩者都限定與軟體開發／JavaScript 社群直接相關的專案，
  本專案是經文數位化，只是恰好用 React 寫，會被審核拒絕。is-a.dev 的服務條款另外明文
  反對用 AI 產生 pull request 並點名 Claude Code，違反可能封鎖作者帳號。
- **eu.org 降為備案**。無官方停止公告，但社群回報審核要數週到數月甚至無下文；
  且有省級封鎖的回報（河北整片擋 eu.org 並顯示詐騙警告），與「大陸能開」的目的相衝。
  另外 nic.eu.org 明言 Gmail 會退掉它的驗證信，註冊信箱不能用 Gmail。
- **改以 DigitalPlat FreeDomain 的 `.dpdns.org` 為免費首選**，它給真正的 NS 委派、
  沒有專案性質限制，代價是每年要手動續期。自購網域仍是唯一沒有存續風險的選項。
