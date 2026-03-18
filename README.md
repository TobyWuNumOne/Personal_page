# Personal Page

個人網站專案，包含前端應用、PocketBase CMS，以及圍繞 GitHub 的 AI 輔助開發流程。

## 專案架構

### `frontend/`

- Vue 3 + Vite + Tailwind CSS
- 部署到 Vercel
- 負責首頁、作品集、部落格與個人內容頁面

### `cms/`

- PocketBase 容器設定
- 部署到 Railway
- 提供內容資料、媒體檔案與 API

## 系統邊界

- `frontend/` 是主要應用程式，從 PocketBase 讀取 `site_settings`、`pages`、`projects` 等內容。
- `cms/` 是內容與媒體來源，不應由一般 code PR 直接做 production 寫入。
- GitHub 是程式碼、issue、PR 與 AI 協作的入口。
- Vercel 與 Railway 延續既有 Git-based deployment。

## AI 開發策略

這個 repo 採用「Copilot 主流程，Codex 補位」：

- `GitHub Copilot Agentic Workflows` 處理小型、可審查的 issue-to-PR 工作。
- `Codex` 由開發者手動介入，用於跨檔重構、複雜除錯、部署與 AI 流程本身的實作。
- 一般 coding PR 不直接寫 production PocketBase。

### Copilot 指引檔

- Repo-wide 規則：[`copilot-instructions.md`](/Users/codyloveyou/code/personal_page/.github/copilot-instructions.md)
- Frontend 規則：[`frontend.instructions.md`](/Users/codyloveyou/code/personal_page/.github/instructions/frontend.instructions.md)
- Workflow 規則：[`workflows.instructions.md`](/Users/codyloveyou/code/personal_page/.github/instructions/workflows.instructions.md)
- CMS 規則：[`cms.instructions.md`](/Users/codyloveyou/code/personal_page/.github/instructions/cms.instructions.md)
- Agent 共用規則：[`AGENTS.md`](/Users/codyloveyou/code/personal_page/AGENTS.md)

## CMS 更新流程

內容更新不再走自由 prompt 的自動 agent。改為受控的 CMS workflow：

- Workflow: [`cms-sync.yml`](/Users/codyloveyou/code/personal_page/.github/workflows/cms-sync.yml)
- Auto-preview workflow: [`cms-preview-from-issue.yml`](/Users/codyloveyou/code/personal_page/.github/workflows/cms-preview-from-issue.yml)
- Script: [`cms_sync.py`](/Users/codyloveyou/code/personal_page/scripts/cms_sync.py)
- Proposal parser: [`cms_proposal.py`](/Users/codyloveyou/code/personal_page/scripts/cms_proposal.py)

### 設計原則

- 使用結構化輸入：`collection`、`record_id` 或 `filter`、`updates_json`
- 預設支援 preview，再由明確 apply 執行寫入
- 使用 PocketBase superuser token 或 email/password 驗證
- 將 CMS 寫入與一般 code PR 分離

### 第一版自動化

- 建立或更新帶有 `content` label 的 issue
- workflow 會從 issue 內的 `Structured CMS Inputs` 解析 `collection`、`record_id` 或 `filter`、`updates_json`
- 自動執行 preview，並把結果 comment 回 issue
- 正式寫入仍由你手動執行 `CMS Sync` workflow 並設定 `apply=true`

### 需要設定的 GitHub Secrets

- `POCKETBASE_URL`
- `POCKETBASE_SUPERUSER_EMAIL`
- `POCKETBASE_SUPERUSER_PASSWORD`
- 或 `POCKETBASE_SUPERUSER_TOKEN`

## 開發與驗證

### 前端開發

```bash
cd frontend
npm install
npm run dev
```

### 前端建置驗證

```bash
npm --prefix frontend run build
```

### CMS 本地測試

```bash
cd cms
docker build -t personal-cms .
docker run -p 8080:8080 personal-cms
```

## 資料備份

- 定期下載 `/pb/pb_data`
- 確認 Railway Volume 持久化設定
- 建議另外做雲端備份

## 環境變數

### Frontend (Vercel)

```env
VITE_API_URL=https://cms.taizanthebar.com
```

### CMS (Railway)

```env
PORT=8080
```

## 技術文件

- [Vue.js 文件](https://vuejs.org/)
- [Tailwind CSS 文件](https://tailwindcss.com/)
- [PocketBase 文件](https://pocketbase.io/docs/)
- [Vercel 部署指南](https://vercel.com/docs)
- [Railway 部署指南](https://docs.railway.app/)

## 授權

MIT License - 詳見 [LICENSE](cms/LICENSE)。
