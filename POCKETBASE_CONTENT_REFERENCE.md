# PocketBase Content Reference

這份文件是給 GitHub Copilot、Codex 和人工維護時參照的 PocketBase 內容摘要。目的是讓 AI 在產生新內容、準備 `CMS Sync` 輸入、或修改前端資料映射時，有一致的 schema 來源。

## 使用原則

- 更新 production PocketBase 時，優先使用 `.github/workflows/cms-sync.yml`。
- `record_id` 適合已知確切 id 的情況；一般內容頁更適合用 `filter`。
- `filter` 最常用唯一欄位是 `slug`。
- `updates_json` 必須是 JSON object，不是陣列，也不是自然語言。
- relation 欄位需要傳 record id 或 id 陣列，不是 display text。

## 常用 collections

### `pages`

用途：靜態頁面內容，例如 `home`、`about`。

關鍵欄位：
- `slug` `text`，唯一
- `title` `text`
- `content` `text`
- `published` `bool`
- `previewToken` `text`
- `previewTokenExpiresAt` `date`

建議 filter：
- `slug="home"`
- `slug="about"`

範例 `updates_json`：

```json
{
  "title": "About Me",
  "content": "Updated markdown or plain text content",
  "published": true
}
```

### `posts`

用途：部落格文章。

關鍵欄位：
- `title` `text`
- `slug` `text`，唯一
- `excerpt` `text`
- `body` `text`
- `published` `bool`
- `tags` `relation[] -> tags`
- `previewToken` `text`
- `previewTokenExpiresAt` `date`

建議 filter：
- `slug="my-first-post"`

範例 `updates_json`：

```json
{
  "title": "New Post Title",
  "excerpt": "Short summary",
  "body": "Full article body",
  "published": true
}
```

### `projects`

用途：專案列表與專案詳情頁。

關鍵欄位：
- `title` `text`
- `slug` `text`，唯一
- `excerpt` `text`
- `body` `text`
- `published` `bool`
- `gallery` `relation[] -> media_assets`
- `skills` `relation[] -> skills`
- `tags` `relation[] -> tags`
- `youtube` `text`
- `previewToken` `text`
- `previewTokenExpiresAt` `date`

建議 filter：
- `slug="project-slug"`

範例 `updates_json`：

```json
{
  "title": "Project Title",
  "excerpt": "One-line project summary",
  "body": "Detailed project description",
  "published": true,
  "youtube": "<iframe ...></iframe>"
}
```

### `rolling_items`

用途：首頁輪播或動態區塊。

關鍵欄位：
- `title` `text`
- `field` `select`: `instagram`, `image`, `text`
- `content` `text`
- `order` `number`
- `published` `bool`

建議 filter：
- 若已知 id，優先用 `record_id`
- 若需要批次排序調整，先人工確認，不建議讓 AI 盲改多筆資料

範例 `updates_json`：

```json
{
  "title": "New rolling card",
  "field": "text",
  "content": "Short rolling content",
  "order": 3,
  "published": true
}
```

### `site_settings`

用途：全站設定。通常只有少量 records，常見是單筆主設定。

關鍵欄位：
- `siteTitle` `text`
- `logo` `file`
- `nav` `json`
- `links` `json`
- `defaultLang` `text`
- `ogImageDefault` `file`
- `favicon` `file`
- `skills` `relation[] -> skills`
- `habbet` `relation[] -> tags`

建議查詢方式：
- 優先用 `record_id`
- 如果只有一筆設定，也可以用 `filter=""` 的讀取思路，但 `cms_sync.py` 目前要求唯一 id 或唯一 filter，因此實務上建議填 `record_id`

範例 `updates_json`：

```json
{
  "siteTitle": "Cody Wu",
  "defaultLang": "zh-TW"
}
```

更新 `nav` 的範例：

```json
{
  "nav": [
    { "label": "首頁", "route": "/", "visible": true, "order": 1 },
    { "label": "關於我", "route": "/profile", "visible": true, "order": 2 }
  ]
}
```

更新 `links` 的範例：

```json
{
  "links": {
    "github": "https://github.com/your-name",
    "linkedin": "https://linkedin.com/in/your-name"
  }
}
```

## Reference collections

### `skills`

用途：標籤型技能資料，常被 `projects` 或 `site_settings` relation 使用。

欄位：
- `name`
- `slug`

### `tags`

用途：文章和專案標籤。

欄位：
- `name`
- `slug`

### `media_assets`

用途：圖片和媒體資產。

欄位：
- `file`
- `alt`
- `caption`

注意：
- 更新 relation 欄位時要傳 `media_assets` record id，不是檔名。

## `CMS Sync` 輸入範例

### 更新 about 頁面標題

- `collection`: `pages`
- `filter`: `slug="about"`
- `updates_json`:

```json
{"title":"About Me"}
```

### 更新首頁內容

- `collection`: `pages`
- `filter`: `slug="home"`
- `updates_json`:

```json
{"content":"Updated home page content","published":true}
```

### 更新 site settings

- `collection`: `site_settings`
- `record_id`: `<actual-record-id>`
- `updates_json`:

```json
{"siteTitle":"Cody Wu","defaultLang":"zh-TW"}
```

## AI 內容生成建議

- `pages.content`、`posts.body`、`projects.body` 生成時，優先輸出可直接渲染的 Markdown 或純文字。
- `excerpt` 應保持短，適合列表卡片。
- `title` 不要混入 slug。
- `slug` 不應自動重寫，除非需求明確要求。
- `published` 預設應保守處理；如果是 preview 階段，不要擅自改成 `false` 或 `true`。

## 自動 preview issue 格式

內容型 issue 要讓自動 preview 生效，請在 `Structured CMS Inputs` 區塊保持這種格式：

```text
- Collection: pages
- Record id or filter: slug="about"
- JSON field updates: {"title":"About Me"}
```

如果 `JSON field updates` 不可由單行 JSON 表示，可以在 `New Content` 區塊放完整 JSON object。
