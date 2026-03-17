# Personal Page

個人網站專案，包含前端應用與後台內容管理系統。

## 專案架構

### 📱 frontend/
**Vercel 部署的前端應用**

- **技術棧：** Vue.js + Vite + Tailwind CSS
- **部署平台：** Vercel
- **網域：** 主網域（待設定）
- **說明：** 個人網站的前端介面，包含首頁、作品集、部落格等頁面

**部署步驟：**
1. 推送程式碼到 GitHub
2. 在 Vercel 連接 GitHub 儲存庫
3. 設定建置指令：`cd frontend && npm run build`
4. 設定輸出目錄：`frontend/dist`
5. 配置自訂網域（如需要）

### 🗄️ cms/
**Railway 部署的 PocketBase CMS**

- **技術棧：** PocketBase (Go-based headless CMS)
- **部署平台：** Railway
- **網域：** cms.taizanthebar.com
- **說明：** 無頭式內容管理系統，提供 API 給前端使用

**部署步驟：**
1. 推送程式碼到 GitHub
2. 在 Railway 建立新專案並連接儲存庫
3. 設定服務目錄為 `cms/`
4. 新增 Volume 並掛載到 `/pb/pb_data`
5. 設定自訂網域：cms.taizanthebar.com
6. 首次訪問後台建立管理員帳號
7. 配置 CORS 允許前端網域存取

## 系統架構說明

這個 repository 目前是典型的分離式網站架構：

- `frontend/` 是 Vue 3 + Vite 單頁應用，負責 UI、路由、樣式與頁面渲染，適合部署到 Vercel。
- `cms/` 是 PocketBase 容器服務，負責內容資料、媒體檔案與 API，適合部署到 Railway 並掛載 persistent volume。
- GitHub 是單一原始碼來源，前端與 CMS 的部署都從同一個 repository 觸發。

資料流目前也很直接：

1. 使用者瀏覽前端頁面。
2. `frontend/src/composables/usePB.ts` 直接連到 `https://cms.taizanthebar.com`。
3. 前端從 PocketBase collections 讀取 `site_settings`、`pages`、`projects` 等資料。
4. Vercel 負責前端建置與發佈，Railway 負責 PocketBase 容器與資料持久化。

以目前程式來看，系統邊界如下：

- 前端應用入口在 [frontend/src/main.js](/Users/codyloveyou/code/personal_page/frontend/src/main.js)。
- 前端路由集中在 [frontend/src/router/index.js](/Users/codyloveyou/code/personal_page/frontend/src/router/index.js)。
- PocketBase API 封裝在 [frontend/src/composables/usePB.ts](/Users/codyloveyou/code/personal_page/frontend/src/composables/usePB.ts)。
- CMS Docker 部署設定在 [cms/Dockerfile](/Users/codyloveyou/code/personal_page/cms/Dockerfile)。

這代表 AI pipeline 最合理的切入點是 GitHub Actions：

- 由 GitHub Issue 當作需求輸入。
- GitHub Actions 在 repository 內執行 AI agent。
- AI agent 只產出 branch 與 PR，不直接改 `main`。
- 合併 PR 後，既有的 Vercel / Railway Git-based deployment 流程自然接手。
- 若 issue 屬於 CMS 內容更新，則由 AI agent 額外呼叫 PocketBase API。

## AI 開發流程

新增的 AI pipeline 會使用 GitHub Issue 作為觸發來源：

1. 使用者建立新的 GitHub Issue。
2. GitHub Actions 執行 `.github/workflows/ai-dev.yml`。
3. workflow 讀取 `GITHUB_EVENT_PATH` 內的 issue payload。
4. `scripts/ai_dev.py` 呼叫 OpenAI 產生建議檔案內容。
5. 腳本建立 `ai/issue-<number>-<slug>` branch。
6. 套用檔案變更、commit、push。
7. 透過 GitHub API 自動建立 Pull Request。
8. PR merge 後，由既有的 Vercel / Railway 部署機制觸發部署。
9. 若 issue 被判定為 content-related，且有設定 `POCKETBASE_API`，腳本會額外送出 PocketBase 更新請求。

## AI Pipeline 檔案

### `.github/workflows/ai-dev.yml`

- 觸發條件：`issues.opened`
- 功能：checkout repo、安裝 Python、安裝 OpenAI SDK、執行 `scripts/ai_dev.py`
- 權限：允許寫入 branch 與建立 PR

### `scripts/ai_dev.py`

- 讀取 GitHub issue event
- 蒐集 repository 文字檔內容當作模型上下文
- 呼叫 OpenAI API 產生檔案更新計劃
- 只允許寫入 repository 內的文字檔
- 建立 branch、commit、push
- 使用 GitHub REST API 建立 Pull Request
- 可選擇性呼叫 `POCKETBASE_API`
- 遇到錯誤時記錄 log 並以非零狀態結束

## GitHub Secrets / Variables

請在 GitHub repository settings 中設定以下 secrets：

- `OPENAI_API_KEY`: 必填，提供 AI agent 呼叫 OpenAI API。
- `GITHUB_TOKEN`: GitHub Actions 內建可用，workflow 會用來 push branch 與建立 PR。
- `POCKETBASE_API`: 選填，提供內容型 issue 的 PocketBase 更新 endpoint。

可選的 Actions variable：

- `OPENAI_MODEL`: 指定使用的模型名稱；若未設定，預設使用 `gpt-4.1`。

## AI Pipeline 安全設計

- 不直接 commit 到 `main`
- 每次 issue 都建立獨立 branch
- 只允許寫入 repository 內檔案
- 保留詳細 logging
- 若模型沒有產生安全的檔案變更，腳本會直接結束，不建立 branch
- PocketBase 更新失敗不會回滾已建立的 PR，但會在 log 中明確標記

## 開發環境設定

### 前端開發
```bash
cd frontend
npm install
npm run dev
```

### CMS 本地測試（使用 Docker）
```bash
cd cms
docker build -t personal-cms .
docker run -p 8080:8080 personal-cms
```

## 資料備份

### PocketBase 資料備份
- **重要：** 定期下載 `/pb/pb_data` 目錄（包含 SQLite 資料庫）
- **Railway Volume：** 確保資料持久化不會遺失
- **建議：** 設定自動備份到雲端儲存

## 環境變數

### Frontend (Vercel)
```env
VITE_API_URL=https://cms.taizanthebar.com
```

### CMS (Railway)
```env
PORT=8080  # Railway 自動注入
```

## 技術文件

- [Vue.js 文件](https://vuejs.org/)
- [Tailwind CSS 文件](https://tailwindcss.com/)
- [PocketBase 文件](https://pocketbase.io/docs/)
- [Vercel 部署指南](https://vercel.com/docs)
- [Railway 部署指南](https://docs.railway.app/)

## 授權

MIT License - 詳見 [LICENSE](cms/LICENSE) 檔案
