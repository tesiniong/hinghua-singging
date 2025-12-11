# GitHub Pages 部署指南

## 前置準備

1. 確認您的 GitHub repository 名稱
2. 如果不是 `hinghua-singging`，需要修改 `website/vite.config.js` 中的 `base` 設定

## 部署步驟

### 1. 初始化 Git Repository

```bash
git init
git add .
git commit -m "Initial commit: 興化語聖經數位化專案"
```

### 2. 連接 GitHub Remote

```bash
git remote add origin https://github.com/YOUR_USERNAME/hinghua-singging.git
git branch -M main
git push -u origin main
```

### 3. 啟用 GitHub Pages

1. 前往 GitHub repository 設定頁面
2. 點擊左側選單的 **Pages**
3. 在 **Source** 下拉選單中選擇：
   - Source: **GitHub Actions**

### 4. 自動部署

推送程式碼到 `main` 分支後，GitHub Actions 會自動：
- 安裝依賴
- 構建專案
- 部署到 GitHub Pages

查看部署進度：
- 前往 repository 的 **Actions** 頁籤
- 點擊最新的 workflow run 查看詳細資訊

### 5. 訪問網站

部署完成後，網站會發佈在：
```
https://YOUR_USERNAME.github.io/hinghua-singging/
```

## 疑難排解

### 構建失敗

1. 檢查 Actions 頁籤的錯誤訊息
2. 確認 `website/package.json` 中的依賴版本正確
3. 本地測試構建：
   ```bash
   cd website
   npm run build
   ```

### 頁面顯示 404

1. 確認 GitHub Pages 已啟用
2. 檢查 `vite.config.js` 中的 `base` 路徑是否與 repository 名稱一致
3. 確認 `main` 分支有最新的程式碼

### 圖片或字體無法載入

1. 檢查瀏覽器控制台的錯誤訊息
2. 確認 `base` 路徑設定正確
3. 確認 `website/public/` 目錄下有 `images/` 和 `fonts/` 資料夾

## 本地預覽生產版本

```bash
cd website
npm run build
npm run preview
```

這會啟動一個本地伺服器來預覽生產版本的網站。

## 手動部署（不使用 GitHub Actions）

如果您想手動部署：

```bash
cd website
npm run build
# 將 dist/ 目錄的內容上傳到 gh-pages 分支
```

## 更新網站

只需推送新的程式碼到 `main` 分支：

```bash
git add .
git commit -m "Update website"
git push
```

GitHub Actions 會自動重新構建和部署。

## 注意事項

- **首次部署**可能需要 5-10 分鐘
- **後續部署**通常 2-3 分鐘即可完成
- 清除瀏覽器快取以查看最新版本
- GitHub Pages 有流量限制（每月 100GB），但對一般使用足夠

## 自訂網域（可選）

如果您有自己的網域：

1. 在 repository 設定的 Pages 頁面中設定 Custom domain
2. 在網域服務商處設定 DNS：
   ```
   Type: CNAME
   Name: www
   Value: YOUR_USERNAME.github.io
   ```
3. 更新 `vite.config.js` 中的 `base` 為 `'/'`
