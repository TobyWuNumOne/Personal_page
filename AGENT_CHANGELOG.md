# Agent Changelog

記錄個人 AI agent 的開發歷程、架構演進、踩坑、問題與解法，避免重複走回頭路。

## 2026-03-18

### 今日變更

- 移除自製 OpenAI issue-to-PR pipeline：
  - 刪除 [.github/workflows/ai-dev.yml](/Users/codyloveyou/code/personal_page/.github/workflows/ai-dev.yml)
  - 刪除 [scripts/ai_dev.py](/Users/codyloveyou/code/personal_page/scripts/ai_dev.py)
  - 刪除 `scripts/ai_pipeline/` 模組
- 新增 GitHub Copilot 指引：
  - [.github/copilot-instructions.md](/Users/codyloveyou/code/personal_page/.github/copilot-instructions.md)
  - [.github/instructions/frontend.instructions.md](/Users/codyloveyou/code/personal_page/.github/instructions/frontend.instructions.md)
  - [.github/instructions/workflows.instructions.md](/Users/codyloveyou/code/personal_page/.github/instructions/workflows.instructions.md)
  - [.github/instructions/cms.instructions.md](/Users/codyloveyou/code/personal_page/.github/instructions/cms.instructions.md)
  - [AGENTS.md](/Users/codyloveyou/code/personal_page/AGENTS.md)
- 新增受控 CMS 更新流程：
  - [.github/workflows/cms-sync.yml](/Users/codyloveyou/code/personal_page/.github/workflows/cms-sync.yml)
  - [scripts/cms_sync.py](/Users/codyloveyou/code/personal_page/scripts/cms_sync.py)
- 更新 README、AI_NOTES、issue templates、PR template，讓整個 repo 明確採用「Copilot 主流程，Codex 補位」。

### 重要決策

- 不再把 GitHub Actions 當成自由 prompt 的自動 coding agent 宿主。
- PocketBase production 寫入與一般 code PR 分離。
- 內容更新改成結構化 workflow 輸入，而不是讓模型自己推斷寫入 payload。
- Codex 保留為人工主導的高能力工程工具，而不是 repo 內建自動化的一部分。

## 2026-03-17

### 今日變更

- 新增 GitHub Actions workflow：[.github/workflows/ai-dev.yml](/Users/codyloveyou/code/personal_page/.github/workflows/ai-dev.yml)
- 新增 AI pipeline 入口：[scripts/ai_dev.py](/Users/codyloveyou/code/personal_page/scripts/ai_dev.py)
- 將 AI pipeline 重構為模組化架構：
  - [scripts/ai_pipeline/pipeline.py](/Users/codyloveyou/code/personal_page/scripts/ai_pipeline/pipeline.py)
  - [scripts/ai_pipeline/router.py](/Users/codyloveyou/code/personal_page/scripts/ai_pipeline/router.py)
  - [scripts/ai_pipeline/context.py](/Users/codyloveyou/code/personal_page/scripts/ai_pipeline/context.py)
  - [scripts/ai_pipeline/openai_client.py](/Users/codyloveyou/code/personal_page/scripts/ai_pipeline/openai_client.py)
  - [scripts/ai_pipeline/git_ops.py](/Users/codyloveyou/code/personal_page/scripts/ai_pipeline/git_ops.py)
  - [scripts/ai_pipeline/pocketbase.py](/Users/codyloveyou/code/personal_page/scripts/ai_pipeline/pocketbase.py)
  - [scripts/ai_pipeline/executor.py](/Users/codyloveyou/code/personal_page/scripts/ai_pipeline/executor.py)
  - [scripts/ai_pipeline/config.py](/Users/codyloveyou/code/personal_page/scripts/ai_pipeline/config.py)
- 新增 GitHub Issue templates：
  - [bug_report.md](/Users/codyloveyou/code/personal_page/.github/ISSUE_TEMPLATE/bug_report.md)
  - [feature_request.md](/Users/codyloveyou/code/personal_page/.github/ISSUE_TEMPLATE/feature_request.md)
  - [content_update.md](/Users/codyloveyou/code/personal_page/.github/ISSUE_TEMPLATE/content_update.md)
  - [config.yml](/Users/codyloveyou/code/personal_page/.github/ISSUE_TEMPLATE/config.yml)
- 新增 PR template：[.github/pull_request_template.md](/Users/codyloveyou/code/personal_page/.github/pull_request_template.md)
- 新增 `.gitignore`，排除 Python 與前端建置暫存
- 更新 [README.md](/Users/codyloveyou/code/personal_page/README.md)，補上 AI pipeline 與架構說明

### 遇到的問題

#### 1. OpenAI `insufficient_quota`

現象：

- GitHub Actions 成功啟動
- `OPENAI_API_KEY` 已成功讀到
- 呼叫 OpenAI API 時回傳 `429`
- 錯誤碼為 `insufficient_quota`

原因：

- 使用的 OpenAI Platform project 沒有可用 API 額度，或 billing / project / key 對應錯誤。

解法：

- 確認 OpenAI Platform 已啟用 billing
- 確認 API key 建立在正確 project
- 必要時重新建立 API key 並更新 GitHub secret

#### 2. OpenAI `rate_limit_exceeded` / TPM 不足

現象：

- `gpt-4.1` 回傳 `Request too large`
- Log 顯示 `Limit 10000, Requested 31755`

原因：

- 第一版 `scripts/ai_dev.py` 每次會讀取過多 repository 檔案
- `MAX_CONTEXT_FILES = 40`
- `MAX_FILE_CHARS = 12000`
- 請求體過大，超過帳號當前 tokens-per-minute 限制

解法：

- 改成 selective context loading
- 新版本只根據 issue 類型挑選相關檔案
- 將 context 上限縮小為：
  - `MAX_CONTEXT_FILES = 8`
  - `MAX_FILE_CHARS = 3000`
- 新增 `MAX_OUTPUT_TOKENS = 3000`
- 預設模型改成 `gpt-5-mini`

#### 3. 單檔 `ai_dev.py` 容易過度膨脹

現象：

- workflow、routing、context、OpenAI、git、PR、PocketBase 全寫在一個檔案
- 很快會變得難維護，後續加 skill 更容易失控

原因：

- 第一版以快速打通流程為主，沒有先模組化

解法：

- 保留 `scripts/ai_dev.py` 作為 entrypoint
- 將邏輯拆到 `scripts/ai_pipeline/`
- 讓主流程只做 orchestration

### 今天的重要決策

- 不讓 AI 每次都讀整個 repository
- issue routing 採用「先規則，再模型」的方向
- skill 將來應該拆分，而不是只靠一個通用 prompt
- `scripts/ai_dev.py` 應該是入口，而不是所有邏輯的承載點
- PocketBase 更新先保留 webhook 介面，不直接在 GitHub Action 裡硬寫 PocketBase 管理邏輯

### 目前 agent 架構方向

1. `ai_dev.py` 作為入口
2. `router.py` 判斷 issue 類型與 skill
3. `context.py` 挑選相關檔案與上下文
4. `openai_client.py` 管理 prompt 與模型呼叫
5. `executor.py` 套用模型產生的檔案內容
6. `git_ops.py` 管理 branch / commit / push / PR
7. `pocketbase.py` 處理內容型 issue 的 webhook

### 後續待辦

- 讓 `router.py` 支援更準確的 issue 分類
- 增加真正的 `skills/` 目錄，而不是只用 skill 名稱字串
- 將 prompt 從「完整檔案回傳」進一步改成更省 token 的 patch 策略
- 新增 PocketBase webhook service 範例
- 增加 dry-run 模式，方便本地測試
