# 部署

網站由 GitHub Actions 自動部署到 GitHub Pages，設定在 `.github/workflows/deploy.yml`。

## 流程

推送到 `main` 後自動執行：

1. 安裝 npm 相依套件
2. `npm run lint`
3. 重跑建置腳本，比對 `data/` 與 `website/public/` 是否有差異
4. `npm run build`
5. 上傳 `website/dist/` 並部署

**任一步失敗就不會部署。** Pull request 會跑前四步，但不上傳也不部署。

首次部署約 5–10 分鐘，之後通常 2–3 分鐘。

## 一次性設定

GitHub repository → Settings → Pages → Source 選 **GitHub Actions**。

## 常見失敗

**「生成的資料與 data/ 的來源文本不同步」**
改過 `data/han.txt` 或 `data/rom.txt` 卻沒有重新建置。
本機執行 `python scripts/build_all.py`，把產生的變更一併提交。

**lint 失敗**
本機 `cd website && npm run lint` 重現。

**建置失敗**
先在本機 `cd website && npm run build`。若只在 CI 失敗，
檢查 `website/package-lock.json` 是否與 `package.json` 同步（CI 用 `npm ci`）。

**頁面 404**
確認 Pages 的 Source 設為 GitHub Actions，且 `website/vite.config.js` 的
`base` 與 repository 名稱一致（目前是 `/hinghua-singging/`）。

**圖片或字型載不出來**
多半是 base path 問題。`website/public/` 底下的檔案不經 Vite 處理，
其中的絕對路徑要自己寫成 `/hinghua-singging/…`。

## 本機預覽正式版

```bash
cd website
npm run build
npm run preview
```

## 換自訂網域

1. Settings → Pages → Custom domain 設定網域
2. DNS 加一筆 `CNAME`：`www` → `tesiniong.github.io`
3. 把 `website/vite.config.js` 的 `base` 改成 `'/'`
4. 同步更新 `website/index.html` 與 `website/public/404.html` 中寫死的
   canonical、og:url、og:image 與圖示路徑，以及 `404.html` 內的重導向路徑

## 額度

GitHub Pages 站台上限 1 GB、每月流量 100 GB。
目前掃描圖約 270 MB，尚有餘裕，但重新處理圖片會讓倉庫與站台快速增長。
