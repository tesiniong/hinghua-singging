# 興化語聖經數位化專案 Hinghua Bible Digital Project

[![GitHub Pages](https://img.shields.io/badge/demo-live-brightgreen)](https://tesiniong.github.io/hinghua-singging/)

1912 年出版的興化語（莆仙語）聖經數位化網站專案。
Digital preservation of the 1912 Hinghua (Puxian Min) Bible.

---

## 專案簡介 Project Overview

本專案的目標是保存並展示 1912 年出版的興化語聖經，這是一份珍貴的語言學資料，保存了 19-20 世紀莆仙語音韻和詞彙。
This project aims to preserve and showcase the 1912 Hinghua Bible, a valuable linguistic resource capturing the phonology and vocabulary of Puxian Min from the 19th-20th centuries.

**線上網址 Live Demo**: https://tesiniong.github.io/hinghua-singging/

---

## 如何參與 How to Participate

發現錯字、想提供建議、或願意協助錄入經文？歡迎您的參與！
Found a typo, have suggestions, or want to help transcribe texts? We welcome your participation!

### 對於不熟悉 GitHub 的朋友 For Those New to GitHub

**不需要會寫程式！** 您只需要：
**No programming skills needed!** You just need to:

1. **報告錯誤或提出建議 Report Errors or Suggestions**
   - 點擊這裡 → [**提交問題或建議**](https://github.com/tesiniong/hinghua-singging/issues/new) ← Click here
   - 描述您發現的問題（例如：哪一卷、哪一章、哪一節有錯字）
   - 如果有建議的修正方式，也請告訴我們
   - Describe the issue (e.g., which book, chapter, verse has an error)

2. **查看已知問題 View Known Issues**
   - 點擊這裡 → [**查看所有問題討論**](https://github.com/tesiniong/hinghua-singging/issues) ← Click here
   - 看看是否有人已經報告過相同的問題
   - 您也可以在別人的問題下留言補充資訊

### 對於熟悉 GitHub 的朋友 For GitHub Users

歡迎直接提交 Pull Request！詳細的技術貢獻指南請見下方「參與貢獻」章節。
Feel free to submit Pull Requests directly! See the "Contributing" section below for detailed technical guidelines.

---

## 主要功能 Key Features

### 多種閱讀模式 Multiple Reading Modes
- **雙欄對照 Dual-Column**: 羅馬字與漢字並列 (Romanization | Han characters)
- **Ruby 注音 Ruby Annotation**: 漢字上標羅馬字 (Romanization above Han)
- **單一語言 Single Language**: 僅羅馬字或僅漢字 (Romanization only or Han only)

### 主題切換 Theme Support
- ☀️ 明亮模式 Light Mode
- 🌙 黑暗模式 Dark Mode
- 💻 系統設定 System Default

### 導航與搜尋 Navigation & Search
- 固定頂端導航欄（自動隱藏/顯示） Fixed navbar with auto-hide
- 多頁面路由（首頁、聖經介紹、語音介紹） Multi-page routing
- 全文搜尋（羅馬字/漢字） Full-text search (Romanization/Chinese)

### 原始掃描頁面 Original Scans
- 點擊 📖 圖示查看原書掃描 Click 📖 icon to view original scans
- 支援縮放、平移功能 Zoom and pan support

### 響應式設計 Responsive Design
- 適配桌面、平板、手機 Desktop, tablet, and mobile friendly

---

## 快速開始 Quick Start

### 安裝依賴 Install Dependencies

```bash
cd website
npm install
```

### 啟動開發伺服器 Start Development Server

```bash
npm run dev
```

開啟瀏覽器訪問 Open browser at: http://localhost:5173/hinghua-singging/

### 構建生產版本 Build for Production

```bash
npm run build
```

構建產物生成在 `website/dist/` 目錄。
Build artifacts are generated in the `website/dist/` directory.

---

## 參與貢獻 Contributing

我們歡迎各種形式的貢獻！
We welcome all forms of contributions!

### 如何貢獻 How to Contribute

1. **文本錄入 Text Input**: 協助錄入剩餘 61 本書的經文 (Help transcribe the remaining 61 books)
2. **校對修正 Proofreading**: 校對已錄入的文本，修正錯誤 (Proofread existing texts and fix errors)
3. **功能開發 Feature Development**: 改進網站功能和使用者體驗 (Improve website features and UX)
4. **語言學資料 Linguistic Data**: 提供興化語相關研究資料 (Provide Hinghua language research materials)
5. **翻譯 Translation**: 協助翻譯介紹頁面內容 (Help translate introduction pages)

### 提交方式 How to Submit

1. Fork 本專案 (Fork this repository)
2. 創建您的功能分支 (Create your feature branch)
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. 提交您的變更 (Commit your changes)
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. 推送到分支 (Push to the branch)
   ```bash
   git push origin feature/AmazingFeature
   ```
5. 開啟 Pull Request (Open a Pull Request)

或者 **開 Issue** 討論您的想法！
Or **open an Issue** to discuss your ideas!

---

## 技術架構 Tech Stack

- **前端框架 Frontend**: React 18 + Vite
- **路由 Routing**: React Router v6
- **字體 Fonts**: Noto Sans TC, DejaVu Sans
- **圖片格式 Images**: WebP (~270MB)
- **部署 Deployment**: GitHub Pages

---

## 專案狀態 Project Status

### 已完成 Completed
- 全部掃描圖片處理 (All scan pages processed)
- 5 本書文本數位化 (5 books digitized):
  - 創世記 Genesis
  - 馬太福音 Matthew
  - 約翰二書 2 John
  - 約翰三書 3 John
  - 使徒猶大書 Jude
- 網站核心功能實現 (Core website features implemented)

### 進行中 In Progress
- 剩餘 61 本書的文本錄入 (Text transcription for remaining 61 books)

---

## 授權 License

本專案為非商業性學術研究專案，以保存和推廣興化語文化遺產為目標。
This is a non-commercial academic project aimed at preserving and promoting Hinghua cultural heritage.

---

## 聯絡 Contact

- **GitHub Issues**: [提問或建議 Questions or Suggestions](https://github.com/tesiniong/hinghua-singging/issues)
- **維護者 Maintainers**: Siniong, 桃泽

---

## 相關資源 Related Resources

- [臺灣大學圖書館數位典藏 NTU Digital Archives](https://dl.lib.ntu.edu.tw/s/westrare/item/129333)
- [HathiTrust Digital Library](https://hdl.handle.net/2027/uc1.31822025315045)
- [維基百科 - 莆仙語](https://zh.wikipedia.org/wiki/%E8%8E%86%E4%BB%99%E8%AF%9D) [Wikipedia - Puxian Min](https://zh.wikipedia.org/wiki/%E8%8E%86%E4%BB%99%E8%AF%9D)
- [維基詞典 - 莆仙語](https://zh.wiktionary.org/wiki/Wiktionary:%E6%BC%A2%E8%AA%9E%E8%A9%9E%E6%A2%9D%E7%B7%A8%E5%AF%AB%E8%A6%8F%E7%AF%84/%E8%8E%86%E4%BB%99%E8%AA%9E) [Wiktionary - Puxian Min](https://en.wiktionary.org/wiki/Wiktionary:Chinese_entry_guidelines/Puxian_Min)

---

**最後更新 Last Updated**: 2025-12-16