# 部署

同一個 workflow（`.github/workflows/deploy.yml`）部署兩個站：

| 站 | 平台 | base | 網址 |
|----|------|------|------|
| 主站 | GitHub Pages | `/hinghua-singging/` | https://tesiniong.github.io/hinghua-singging/ |
| 鏡像 | Cloudflare Pages | `/` | repository variable `MIRROR_SITE_URL`（自訂網域） |

鏡像是給中國大陸讀者的：github.io 在大陸時常連不上或極慢。鏡像不依賴任何 GitHub
或 Google 資源（字型全部隨站附帶），只要網域解析得到就能開。

## 流程

推送到 `main` 後自動執行：

1. 安裝 npm 相依套件
2. `npm run lint`
3. 重跑建置腳本，比對 `data/` 與 `website/public/` 是否有差異
4. `npm run build` 兩次：主站用預設值；鏡像用 `VITE_BASE=/` 與
   `VITE_SITE_URL=<鏡像網址>`，輸出到 `website/dist-mirror/`
5. 上傳 `website/dist/` 並部署到 GitHub Pages
6. 以 wrangler 把 `website/dist-mirror/` 部署到 Cloudflare Pages
   （repository variable `CF_PAGES_PROJECT` 未設定時略過）

**任一步失敗就不會部署。** Pull request 會跑前四步；主站不部署，鏡像若 PR 來自同一倉庫
會部署為預覽版（`<分支>.<專案>.pages.dev`）。

首次部署約 5–10 分鐘，之後通常 2–3 分鐘。鏡像第一次會上傳全部約 1,500 個檔案（約 300 MB），
之後 wrangler 只上傳雜湊有變的檔案。

## base path 與站台網址

寫死路徑的地方只剩 `website/.env`：

```
VITE_BASE=/hinghua-singging/
VITE_SITE_URL=https://tesiniong.github.io/hinghua-singging/
```

- `vite.config.js` 讀 `VITE_BASE` 當 `base`；同名的環境變數會覆寫 `.env` 的值。
- `src/` 底下一律用 `import.meta.env.BASE_URL` 組路徑。
- `index.html`、`404.html` 用 `%BASE_URL%`、`%VITE_SITE_URL%` 佈景值，Vite 建置時代入
  （canonical、og:url、og:image、SPA 重導向路徑）。
- `404.html` 放在 `website/` 根目錄、列為 Vite 的 HTML 入口，圖示路徑會自動套上 base。
  `public/` 底下的檔案不經 Vite 處理，不要再把 HTML 放進去。

本機模擬鏡像建置：

```bash
cd website
VITE_BASE=/ VITE_SITE_URL=https://example.org/ npm run build -- --outDir dist-mirror
npx vite preview --outDir dist-mirror
```

## 一次性設定：GitHub Pages

GitHub repository → Settings → Pages → Source 選 **GitHub Actions**。

## 一次性設定：鏡像站（Cloudflare Pages）

Cloudflare 免費方案不需要信用卡。整個流程只有 eu.org 網域要等人工審核，
所以**先做網域那兩步**，等待期間做其餘設定。

### 1. Cloudflare 帳號與 zone

1. 到 https://dash.cloudflare.com/sign-up 建帳號，只要 email。
2. 首頁 → **Add a domain** → 輸入預定的網域，例如 `hinghua.eu.org` → 選 **Free** 方案。
3. Cloudflare 會給兩個 name server，形如 `xxx.ns.cloudflare.com`，記下來。
   zone 會停在「Pending Nameserver Update」，直到下一步的網域核准。

### 2. 免費網域：eu.org

1. 到 https://nic.eu.org/ → **Register** 建立帳號（contact handle）。
2. 登入後 **Domains → New domain**：Domain name 填 `hinghua.eu.org`，
   Name servers 填上一步的兩個 Cloudflare NS，其餘留空，送出。
3. 等審核 email。快則幾天，慢則幾週；期間先做第 3、4 步。
4. 核准後回 Cloudflare 的 zone 頁按 **Check nameservers**，狀態變 Active 即可。

注意：Cloudflare 會刪掉停在 Pending 超過約四週的 zone。若發生，重新 Add a domain；
若新配到的 NS 與當初填給 eu.org 的不同，到 nic.eu.org 該網域頁面把 NS 改成新的。

備選：is-a.dev（https://github.com/is-a-dev/register）走 GitHub PR，一兩天就過，
但它不提供 NS 委派，只能填 CNAME 指到 `<專案>.pages.dev`，且大陸可達性沒有實測資料。

### 3. Cloudflare Pages 專案與 API token

1. 建專案（Direct Upload；名稱之後要填進 `CF_PAGES_PROJECT`）：
   ```bash
   cd website
   npx wrangler login
   npx wrangler pages project create hinghua-singging --production-branch main
   ```
   或在控制台 Workers & Pages → Create → Pages → Upload assets 建立。
2. Account ID：`npx wrangler whoami`，或控制台 Workers & Pages 總覽頁右側。
3. API token：控制台右上頭像 → My Profile → **API Tokens** → Create Token →
   Create Custom Token，權限只給 **Account → Cloudflare Pages → Edit**。

### 4. GitHub 的 secrets 與 variables

Repository → Settings → Secrets and variables → Actions：

| 類型 | 名稱 | 值 |
|------|------|----|
| Secret | `CLOUDFLARE_API_TOKEN` | 上一步的 token |
| Secret | `CLOUDFLARE_ACCOUNT_ID` | Account ID |
| Variable | `CF_PAGES_PROJECT` | 專案名稱，例如 `hinghua-singging` |
| Variable | `MIRROR_SITE_URL` | 網域核准後才設，例如 `https://hinghua.eu.org/`，結尾要有斜線 |

設好 `CF_PAGES_PROJECT` 後，下一次推 `main`，或在 Actions 頁對 main 按 **Run workflow**，
就會部署鏡像。`MIRROR_SITE_URL` 設定之前，鏡像的 canonical 暫時指向 `<專案>.pages.dev`。

### 5. 綁自訂網域

網域核准、zone 變 Active 之後：Workers & Pages → 該專案 → **Custom domains** →
Set up a custom domain → 填 `hinghua.eu.org`。Cloudflare 會自動加 CNAME 並簽憑證，幾分鐘生效。
然後設定 `MIRROR_SITE_URL`，重跑一次 workflow 讓 canonical 與 og:url 換成正式網址。

### 6. 從大陸驗證

`*.pages.dev` 在大陸受 DNS 污染，只能用自訂網域測。請莆田的協作者開鏡像網址，重點看：
首頁載入時間、翻頁掃描圖、韻母表的音標是否為 Gentium Plus（襯線體）而非 DejaVu Sans。
也可用 https://www.17ce.com/ 之類的多地測速服務看福建節點。

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
確認 Pages 的 Source 設為 GitHub Actions，且 `website/.env` 的 `VITE_BASE`
與 repository 名稱一致（目前是 `/hinghua-singging/`）。

**圖片或字型載不出來**
多半是 base path 問題。`src/` 內組路徑一律用 `import.meta.env.BASE_URL`，
HTML 入口用 `%BASE_URL%`；不要寫死 `/hinghua-singging/`。

**鏡像沒有部署**
Actions 記錄裡「Deploy mirror to Cloudflare Pages」顯示 skipped：`CF_PAGES_PROJECT` 沒設。
失敗且訊息為 project not found：變數值與 Cloudflare 上的專案名稱不一致。
Authentication error：token 權限不足或 `CLOUDFLARE_ACCOUNT_ID` 錯。

**鏡像的 canonical 或 og:url 指向 pages.dev**
`MIRROR_SITE_URL` 沒設，或設了之後沒重跑 workflow。

## 本機預覽正式版

```bash
cd website
npm run build
npm run preview
```

## 主站換自訂網域

1. Settings → Pages → Custom domain 設定網域
2. DNS 加一筆 `CNAME`：`www` → `tesiniong.github.io`
3. 把 `website/.env` 的 `VITE_BASE` 改成 `/`、`VITE_SITE_URL` 改成新網址，重新建置即可，
   不必再動任何 HTML

## 額度

GitHub Pages 站台上限 1 GB、每月流量 100 GB。
Cloudflare Pages 免費方案每站 20,000 個檔案、單檔 25 MiB，流量不設上限。
目前站台約 1,515 個檔案、300 MB，其中掃描圖 270 MB；重新處理圖片會讓倉庫與兩個站台一起變大。
