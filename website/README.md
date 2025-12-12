# 興化語聖經網站 Hinghua Bible Website

這是興化語聖經數位化專案的網站部分，使用 React + Vite 構建。

This is the website component of the Hinghua Bible Digital Project, built with React + Vite.

## 快速開始 Quick Start

```bash
# 安裝依賴 Install dependencies
npm install

# 啟動開發伺服器 Start dev server
npm run dev

# 構建生產版本 Build for production
npm run build

# 預覽生產版本 Preview production build
npm run preview
```

## 技術棧 Tech Stack

- **React 18** - UI 框架
- **Vite** - 構建工具
- **React Router v6** - 路由管理
- **CSS Modules** - 樣式管理

## 專案結構 Project Structure

```
website/
├── public/                 # 靜態資源
│   ├── images/             # 1485 張 WebP 掃描圖片
│   ├── bible_data.json     # 聖經數據
│   └── *.json              # 其他數據文件
├── src/
│   ├── pages/              # 頁面組件
│   │   ├── Home.jsx
│   │   ├── AboutBible.jsx
│   │   └── AboutLanguage.jsx
│   ├── components/         # React 組件
│   │   ├── Navbar.jsx
│   │   ├── ThemeToggle.jsx
│   │   ├── BibleReader.jsx
│   │   └── ...
│   ├── assets/
│   │   └── fonts/          # 本地字體
│   ├── App.jsx             # 路由容器
│   └── main.jsx            # 應用入口
└── vite.config.js          # Vite 配置
```

## 開發說明 Development Notes

- Base URL 設定為 `/hinghua-singging/`，適用於 GitHub Pages 部署
- 字體檔案存放在 `src/assets/fonts/`
- 圖片和數據文件存放在 `public/`
- 支援明亮/黑暗/系統主題切換
- 導航欄支援自動隱藏/顯示

## 更多資訊 More Information

詳細的專案說明請參閱根目錄的 `CLAUDE.md` 和 `README.md`。

For detailed project documentation, see `CLAUDE.md` and `README.md` in the root directory.
