# AI Review Heuristics

這份文件用來審查 GitHub Copilot 或其他 AI 產生的 PR，目標是快速判斷「改得對不對」與「改得有沒有超出範圍」。

## Primary Review Questions

每次看 AI PR，先回答這 5 個問題：

1. 這個 PR 是否真的只處理 issue 要求的問題？
2. 變更範圍是否比必要的更大？
3. 有沒有碰到 issue 明確說不要改的區域？
4. 驗證方法是否可信，而不是口頭宣稱？
5. 這個修法是否符合 repo 既有資料流與元件邊界？

## What Good AI PRs Look Like

- 修改集中在少數相關檔案
- 變更可以直接對應到 issue 的 `Current Behavior` / `Expected Behavior` / `Acceptance Criteria`
- 沒有順手重構、重新命名或改動無關樣式
- 有實際驗證，至少是 `npm --prefix frontend run build`
- PR 說明和實際 diff 一致

## High-Signal Review Checks

### Scope Discipline

- 是否只改了和 issue 直接相關的元件、composable 或 workflow
- 是否新增了不必要的 dependency、helper、抽象層
- 是否把小 bug 修成了半個 refactor

### Frontend Safety

- 是否保留既有 route、props、composable API
- 是否改壞 PocketBase 資料映射或 fallback 邏輯
- 是否把內容、樣式、資料流混在同一次修改裡
- 如果是 UI bug，是否只修 UI bug，而不是重寫整個元件

### CMS / Production Safety

- 一般 code PR 不應直接寫 production PocketBase
- 是否誤改 collection 名稱、field 名稱、API URL
- 是否把 CMS schema 變更塞進一般 bug/feature PR

### Workflow / Infra Safety

- 是否擴大了 GitHub Actions 權限
- 是否加入 prompt-based mutation 或新的外部 AI 依賴
- 是否誤碰 Vercel、Railway、secrets、deployment 設定

## Common AI Failure Patterns

- 修一個 bug，卻順手改了命名、樣式或資料流
- 實作和 issue 不一致，只修了表面現象
- 宣稱有驗證，但沒有實際可重現的 build/check
- 把 fallback 寫成更複雜的新邏輯，增加未來維護成本
- 為了避免理解既有程式，直接新增平行邏輯或重複函式

## Review Decision Rules

### Accept quickly when

- diff 小而集中
- 驗證清楚
- 沒碰高風險區域
- acceptance criteria 能直接對上

### Request changes when

- 有無關修改
- 改動超出 issue 邊界
- 驗證不充分
- 需要更小、更直接的修法

### Route to Codex/manual when

- issue 實際上是跨多檔重構
- 涉及 deployment、schema、production data、AI pipeline
- 需要深度 repo 理解才有辦法正確修

## Repo-Specific Biases

- 優先最小修改，不優先漂亮重構
- 前端問題優先在對應元件或最小必要 composable 修正
- 除非 issue 明講，不要改 route、CMS schema、API URL、部署設定
- `content` 類需求應走 CMS workflow，不要在一般 code PR 順手改 production 內容
