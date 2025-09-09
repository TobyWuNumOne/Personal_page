# AI Notes — 個人網站（Pocke-   [x] 前端安裝 pocketbase SDK 並建立 `usePB.ts`
-   [x] 設定公開可讀規則：site_settings/tags/skills/media_assets（List/View = true）
-   [x] 手動測試公開 API（/api/collections/{collection}/records 是否可讀）
-   [x] Navbar 改讀 `site_settings.nav`
-   [x] MyProject 改讀 `projects` collection（含 skills/tags 展開）
-   [x] 新增 ProjectDetail 頁面（支援 Markdown 渲染）
-   [x] Profile 改讀 `site_settings` + `pages` (slug="about")（混合模式 + Markdown）
-   [ ] Blog 改讀 `posts` collectionRailway + Vercel）

> 單一真相來源（SSOT）給 Cody / 助理 AI / Copilot 共同參考 以便於未來的維護和開發。

## 🟢 Now / 🔜 Next / 🧱 Blockers

-   **Now**: PocketBase 已上線；collections 匯入完成（pages/posts/projects/tags/skills/media_assets/site_settings）；pages/posts/projects 已套用 preview token 規則
-   **Next**:
    1. 設定公開可讀規則：site_settings/tags/skills/media_assets（List/View = true）
    2. 填充測試資料（site_settings 一筆、pages: home/about、projects/posts 各 1–2 筆）
    3. 前端頁面改讀 CMS（Phase 1: Navbar → Phase 2: Home/Profile → Phase 3: Projects/Posts）
-   **Blockers**: （無）

## ✅ Tasks

-   [x] Railway 部署 PocketBase（含 Volume）
-   [x] 自訂網域 cms.taizanthebar.com
-   [x] 匯入最小 collections
-   [x] 設定 pages/posts/projects 的 preview token 規則（List/View）
-   [ ] 填 `site_settings` 第一筆資料（nav/links/logo）
-   [ ] 建 `pages: home/about`
-   [ ] 建 `projects` 2 筆（含封面/skills/tags）
-   [ ] 建 `posts` 2 篇（含 tags）
-   [x] 前端安裝 pocketbase SDK 並建立 `usePB.ts`
-   [x] 設定公開可讀規則：site_settings/tags/skills/media_assets（List/View = true）
-   [x] 手動測試公開 API（/api/collections/{collection}/records 是否可讀）
-   [x] Navbar 改讀 `site_settings.nav`
-   [x] MyProject 改讀 `projects` collection（含 skills/tags 展開）
-   [x] 新增 ProjectDetail 頁面（支援 Markdown 渲染）
-   [ ] Profile/About 改讀 `pages`
-   [ ] Blog 改讀 `posts` collection

## 🚀 前端 API 整合計劃

### **Phase 1: 基礎設定與 Navbar（優先）**

- [x] 測試所有 API endpoints 公開訪問
- [x] 增強 `usePB.ts` 增加錯誤處理
- [x] Navbar.vue：改讀 `site_settings.nav` + logo
- [x] 建立全域 site settings composable

### **Phase 2: 內容頁面**

- [ ] Home.vue：改讀 `pages` (slug="home") + `site_settings.links`
- [x] Profile.vue：改讀 `site_settings` + `pages` (slug="about")（混合模式 + Markdown + 技能整合）
- [ ] 處理 Markdown/HTML 內容渲染

### **Phase 3: 動態列表**

- [x] MyProject.vue：改讀 `projects` collection
- [ ] Blog.vue：改讀 `posts` collection
- [x] 新增 skills/tags 顯示
- [ ] 新增分頁功能

### **Phase 4: 進階功能**

- [x] 新增個別專案/文章頁面
- [ ] 圖片最佳化與 lazy loading
- [ ] SEO meta tags 整合
- [ ] 搜尋與篩選功能

## 🧭 Decision Log

-   **2025-09-08** — 後端選型：PocketBase on Railway

    -   _Why_: 輕量、內建 Admin、$0 ～$7/月、易展示技術
    -   _Alternatives_: Sanity（零維運但可控度較低）、Decap（$0 但媒體庫弱）

-   **2025-09-08** — 網域策略：`cms.taizanthebar.com` 指向 Railway
    -   _Why_: 與前台解耦；CORS 明確
    -   _Notes_: CORS 允許 `www.taizanthebar.com`、`cms.taizanthebar.com`

## 📝 Notes / Learnings

-   Relation 欄位需先建立目標 collection 才能選；避免手動步驟可用 `Import collections`
-   Import 格式需含 `id/system/presentable/options` 等欄位，否則報 `Invalid collections configuration`

## 🔗 Links

-   CMS: https://cms.taizanthebar.com
-   Pages API（公開）: https://cms.taizanthebar.com/api/collections/pages/records
-   Projects API（公開）: https://cms.taizanthebar.com/api/collections/projects/records

## 🗓 Changelog

-   2025-09-08 — PocketBase 上線、最小 collections 匯入完成
-   2025-09-08 — 新增 AI_NOTES.md；為 pages/posts/projects 加上預覽規則（previewToken / previewTokenExpiresAt）
-   Export collections

```json
[
    {
        "id": "media01",
        "name": "media_assets",
        "type": "base",
        "system": false,
        "schema": [
            {
                "system": false,
                "id": "ma_file",
                "name": "file",
                "type": "file",
                "required": true,
                "presentable": true,
                "unique": false,
                "options": {
                    "mimeTypes": ["image/*"],
                    "thumbs": null,
                    "maxSelect": 1,
                    "maxSize": 8388608,
                    "protected": false
                }
            },
            {
                "system": false,
                "id": "ma_alt",
                "name": "alt",
                "type": "text",
                "required": true,
                "presentable": true,
                "unique": false,
                "options": {
                    "min": 1,
                    "max": 200,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "ma_caption",
                "name": "caption",
                "type": "text",
                "required": false,
                "presentable": true,
                "unique": false,
                "options": {
                    "min": null,
                    "max": 500,
                    "pattern": ""
                }
            }
        ],
        "indexes": [],
        "listRule": "",
        "viewRule": "",
        "createRule": null,
        "updateRule": null,
        "deleteRule": null,
        "options": {}
    },
    {
        "id": "pages01",
        "name": "pages",
        "type": "base",
        "system": false,
        "schema": [
            {
                "system": false,
                "id": "pg_slug",
                "name": "slug",
                "type": "text",
                "required": true,
                "presentable": true,
                "unique": true,
                "options": {
                    "min": 1,
                    "max": 120,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "pg_title",
                "name": "title",
                "type": "text",
                "required": true,
                "presentable": true,
                "unique": false,
                "options": {
                    "min": 1,
                    "max": 200,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "pg_content",
                "name": "content",
                "type": "text",
                "required": false,
                "presentable": true,
                "unique": false,
                "options": {
                    "min": null,
                    "max": 20000,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "pg_published",
                "name": "published",
                "type": "bool",
                "required": false,
                "presentable": true,
                "unique": false,
                "options": {}
            },
            {
                "system": false,
                "id": "1ysc0ph3",
                "name": "previewToken",
                "type": "text",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "min": null,
                    "max": null,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "8pda61kl",
                "name": "previewTokenExpiresAt",
                "type": "date",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "min": "",
                    "max": ""
                }
            }
        ],
        "indexes": [],
        "listRule": "published = true",
        "viewRule": "published = true\n|| (\n  previewToken != \"\" \n  && previewToken = @request.query.token \n  && (\n    previewTokenExpiresAt = \"\" \n    || previewTokenExpiresAt >= @now\n  )\n)",
        "createRule": null,
        "updateRule": null,
        "deleteRule": null,
        "options": {}
    },
    {
        "id": "posts01",
        "name": "posts",
        "type": "base",
        "system": false,
        "schema": [
            {
                "system": false,
                "id": "po_title",
                "name": "title",
                "type": "text",
                "required": true,
                "presentable": true,
                "unique": false,
                "options": {
                    "min": 1,
                    "max": 200,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "po_slug",
                "name": "slug",
                "type": "text",
                "required": true,
                "presentable": true,
                "unique": true,
                "options": {
                    "min": 1,
                    "max": 150,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "po_excerpt",
                "name": "excerpt",
                "type": "text",
                "required": false,
                "presentable": true,
                "unique": false,
                "options": {
                    "min": null,
                    "max": 300,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "po_body",
                "name": "body",
                "type": "text",
                "required": false,
                "presentable": true,
                "unique": false,
                "options": {
                    "min": null,
                    "max": 20000,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "po_published",
                "name": "published",
                "type": "bool",
                "required": false,
                "presentable": true,
                "unique": false,
                "options": {}
            },
            {
                "system": false,
                "id": "jdttjxpa",
                "name": "tags",
                "type": "relation",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "collectionId": "tags01",
                    "cascadeDelete": false,
                    "minSelect": null,
                    "maxSelect": null,
                    "displayFields": null
                }
            },
            {
                "system": false,
                "id": "ddzbwqmq",
                "name": "previewToken",
                "type": "text",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "min": null,
                    "max": null,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "p0wwbaws",
                "name": "previewTokenExpiresAt",
                "type": "date",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "min": "",
                    "max": ""
                }
            }
        ],
        "indexes": [],
        "listRule": "published = true",
        "viewRule": "published = true\n|| (\n  previewToken != \"\" \n  && previewToken = @request.query.token \n  && (\n    previewTokenExpiresAt = \"\" \n    || previewTokenExpiresAt >= @now\n  )\n)",
        "createRule": null,
        "updateRule": null,
        "deleteRule": null,
        "options": {}
    },
    {
        "id": "projects01",
        "name": "projects",
        "type": "base",
        "system": false,
        "schema": [
            {
                "system": false,
                "id": "pr_title",
                "name": "title",
                "type": "text",
                "required": true,
                "presentable": true,
                "unique": false,
                "options": {
                    "min": 1,
                    "max": 200,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "pr_slug",
                "name": "slug",
                "type": "text",
                "required": true,
                "presentable": true,
                "unique": true,
                "options": {
                    "min": 1,
                    "max": 150,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "pr_excerpt",
                "name": "excerpt",
                "type": "text",
                "required": false,
                "presentable": true,
                "unique": false,
                "options": {
                    "min": null,
                    "max": 300,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "pr_body",
                "name": "body",
                "type": "text",
                "required": false,
                "presentable": true,
                "unique": false,
                "options": {
                    "min": null,
                    "max": 20000,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "pr_published",
                "name": "published",
                "type": "bool",
                "required": false,
                "presentable": true,
                "unique": false,
                "options": {}
            },
            {
                "system": false,
                "id": "scfwvo5y",
                "name": "gallery",
                "type": "relation",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "collectionId": "media01",
                    "cascadeDelete": false,
                    "minSelect": null,
                    "maxSelect": null,
                    "displayFields": null
                }
            },
            {
                "system": false,
                "id": "yd2vazjm",
                "name": "skills",
                "type": "relation",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "collectionId": "skills01",
                    "cascadeDelete": false,
                    "minSelect": null,
                    "maxSelect": null,
                    "displayFields": null
                }
            },
            {
                "system": false,
                "id": "ng1ta4pl",
                "name": "tags",
                "type": "relation",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "collectionId": "tags01",
                    "cascadeDelete": false,
                    "minSelect": null,
                    "maxSelect": null,
                    "displayFields": null
                }
            },
            {
                "system": false,
                "id": "ghcsvdky",
                "name": "previewToken",
                "type": "text",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "min": null,
                    "max": null,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "qdtwht2i",
                "name": "previewTokenExpiresAt",
                "type": "date",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "min": "",
                    "max": ""
                }
            }
        ],
        "indexes": [],
        "listRule": "published = true",
        "viewRule": "published = true\n|| (\n  previewToken != \"\" \n  && previewToken = @request.query.token \n  && (\n    previewTokenExpiresAt = \"\" \n    || previewTokenExpiresAt >= @now\n  )\n)",
        "createRule": null,
        "updateRule": null,
        "deleteRule": null,
        "options": {}
    },
    {
        "id": "pw07wvildec8sxq",
        "name": "site_settings",
        "type": "base",
        "system": false,
        "schema": [
            {
                "system": false,
                "id": "xhqhnsdq",
                "name": "siteTitle",
                "type": "text",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "min": null,
                    "max": null,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "vlh1evk3",
                "name": "logo",
                "type": "file",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "mimeTypes": [],
                    "thumbs": [],
                    "maxSelect": 1,
                    "maxSize": 5242880,
                    "protected": false
                }
            },
            {
                "system": false,
                "id": "isdhp2b8",
                "name": "nav",
                "type": "json",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "maxSize": 2000000
                }
            },
            {
                "system": false,
                "id": "lre2o7pn",
                "name": "links",
                "type": "json",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "maxSize": 2000000
                }
            },
            {
                "system": false,
                "id": "tpsb7bpp",
                "name": "defaultLang",
                "type": "text",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "min": null,
                    "max": null,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "auwshkkg",
                "name": "ogImageDefault",
                "type": "file",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "mimeTypes": [],
                    "thumbs": [],
                    "maxSelect": 1,
                    "maxSize": 5242880,
                    "protected": false
                }
            },
            {
                "system": false,
                "id": "up5pwegf",
                "name": "favicon",
                "type": "file",
                "required": false,
                "presentable": false,
                "unique": false,
                "options": {
                    "mimeTypes": [],
                    "thumbs": [],
                    "maxSelect": 1,
                    "maxSize": 5242880,
                    "protected": false
                }
            }
        ],
        "indexes": [],
        "listRule": "",
        "viewRule": "",
        "createRule": null,
        "updateRule": null,
        "deleteRule": null,
        "options": {}
    },
    {
        "id": "skills01",
        "name": "skills",
        "type": "base",
        "system": false,
        "schema": [
            {
                "system": false,
                "id": "sk_name",
                "name": "name",
                "type": "text",
                "required": true,
                "presentable": true,
                "unique": false,
                "options": {
                    "min": 1,
                    "max": 80,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "sk_slug",
                "name": "slug",
                "type": "text",
                "required": true,
                "presentable": true,
                "unique": true,
                "options": {
                    "min": 1,
                    "max": 120,
                    "pattern": ""
                }
            }
        ],
        "indexes": [],
        "listRule": "",
        "viewRule": "",
        "createRule": null,
        "updateRule": null,
        "deleteRule": null,
        "options": {}
    },
    {
        "id": "tags01",
        "name": "tags",
        "type": "base",
        "system": false,
        "schema": [
            {
                "system": false,
                "id": "tg_name",
                "name": "name",
                "type": "text",
                "required": true,
                "presentable": true,
                "unique": false,
                "options": {
                    "min": 1,
                    "max": 80,
                    "pattern": ""
                }
            },
            {
                "system": false,
                "id": "tg_slug",
                "name": "slug",
                "type": "text",
                "required": true,
                "presentable": true,
                "unique": true,
                "options": {
                    "min": 1,
                    "max": 120,
                    "pattern": ""
                }
            }
        ],
        "indexes": [],
        "listRule": "",
        "viewRule": "",
        "createRule": null,
        "updateRule": null,
        "deleteRule": null,
        "options": {}
    }
]
```
