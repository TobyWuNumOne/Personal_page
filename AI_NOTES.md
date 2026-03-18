# AI Notes — 個人網站（PocketBase + Railway + Vercel）

> 單一真相來源（SSOT）給 Cody / 助理 AI / Copilot 共同參考，集中記錄目前狀態、待辦與 AI 自動化進度。

## Current State

- 網站架構：`frontend` 為 Vue 3 + Vite + Tailwind，`cms` 為 PocketBase on Railway。
- 內容來源：前端主要從 PocketBase 讀取 `site_settings`、`pages`、`projects` 等資料。
- AI 策略：`Copilot 主流程，Codex 補位`。
- 一般 code PR 不直接寫 production PocketBase。
- PocketBase schema / content 參考文件：`POCKETBASE_CONTENT_REFERENCE.md`。

## AI Automation Status

### 已完成

- 移除舊的自製 OpenAI coding pipeline
- 建立 repo-wide Copilot instructions、path-specific instructions、`AGENTS.md`
- 建立 `CMS Sync` workflow，可做 PocketBase preview / apply
- 建立 `[Content]` issue 自動產生 CMS preview comment
- 建立 `[Bug]` / `[Feature]` issue eligibility gate 與自動指派 Copilot coding agent workflow
- 已實測 `[Bug]` issue 可成功指派給 Copilot，並建立 linked PR 與 Vercel preview
- 建立 `.github/AI_REVIEW_HEURISTICS.md` 作為人工審查 AI PR 的基準

### 目前限制

- `scripts/cms_proposal.py` 仍是 parser / translator，不是 AI content generator
- code issue workflow 只適合小而清楚的工作；高風險 issue 仍應轉 Codex / manual
- Copilot 開出的 PR 目前仍可能是 draft / WIP，merge 仍須人工處理

### AI Automation 待辦

- [ ] 將 `cms_proposal.py` 升級為 AI proposal generator
- [ ] 讓 content issue 以自然語言描述需求，由 AI 自動生成 `collection`、`filter`、`updates_json`
- [ ] 補強 Copilot PR 後續流程，例如 reviewer / ready-for-review / PR polish
- [ ] 根據實際 review 經驗持續收斂 Copilot instructions 與 frontend instructions

## Product / Site Tasks

### 近期優先

- [ ] `Blog.vue` 改讀 `posts` collection
- [ ] `Home.vue` 改讀 `pages` (`slug="home"`) + `site_settings.links`
- [ ] 新增部落格文章詳細頁面

### 已完成

- [x] Railway 部署 PocketBase（含 Volume）
- [x] 自訂網域 `cms.taizanthebar.com`
- [x] 匯入最小 collections
- [x] 設定 `pages` / `posts` / `projects` 的 preview token 規則
- [x] 填 `site_settings` 第一筆資料（`nav` / `links` / `logo` + `skills` relation）
- [x] 建立 `pages: about`
- [x] 建立 `projects` 測試資料
- [x] 前端安裝 PocketBase SDK 並建立 `usePB.ts`
- [x] 設定公開可讀規則：`site_settings` / `tags` / `skills` / `media_assets`
- [x] 手動測試公開 API 可讀
- [x] `Navbar` 改讀 `site_settings.nav`
- [x] `MyProject` 改讀 `projects` collection（含 `skills` / `tags` / `gallery`）
- [x] 新增個別專案頁面（`ProjectDetail.vue`）
- [x] `Profile` 改讀 `site_settings` + `pages` (`slug="about"`)
- [x] 修正 `MyProject` 圖片顯示問題（gallery expand）
- [x] `Profile` 頭像整合 PocketBase 圖片 API
- [x] 專案 YouTube 影片嵌入功能

### 產品待辦

- [ ] 建立 `posts` 測試內容
- [ ] `Blog.vue` 改讀 `posts` collection
- [ ] `Home.vue` 改讀 `pages` (`slug="home"`) + `site_settings.links`
- [ ] 新增部落格文章詳細頁面
- [ ] 新增分頁功能
- [ ] 圖片最佳化與 lazy loading
- [ ] SEO meta tags 整合
- [ ] 搜尋與篩選功能

## Blockers

- 目前無明確 blocker

## Decision Log

- **2025-09-08** — 後端選型：PocketBase on Railway  
  Why: 輕量、內建 Admin、成本低、易展示技術

- **2025-09-08** — 網域策略：`cms.taizanthebar.com` 指向 Railway  
  Why: 與前台解耦；CORS 明確

- **2026-03-18** — AI 開發策略切換為 `Copilot 主流程，Codex 補位`  
  Why: 降低自建 agent 維護成本，直接利用 GitHub 原生 issue-to-PR 能力

## Notes / Learnings

- relation 欄位需先建立目標 collection 才能選；避免手動步驟可用 import collections
- relation 欄位通常需配合 `expand` 參數取得關聯資料，例如 `expand=skills,tags,gallery`
- `media_assets` 圖片 URL 格式為 `https://cms.taizanthebar.com/api/files/media_assets/[id]/[filename]`
- `Profile` 頁面已採混合資料來源模式：`site_settings` + `pages`
- AI 產生的 PR 需用 `.github/AI_REVIEW_HEURISTICS.md` 做人工審查

## Useful Links

- CMS: https://cms.taizanthebar.com
- Pages API: https://cms.taizanthebar.com/api/collections/pages/records
- Projects API: https://cms.taizanthebar.com/api/collections/projects/records
