# Copilot Instructions

This repository uses GitHub Copilot coding agent for narrow, reviewable work and uses Codex manually for deeper implementation, refactors, and debugging.

## Repository shape

- `frontend/` is the main application. It is a Vue 3 + Vite + Tailwind SPA deployed on Vercel.
- `cms/` contains the PocketBase container setup deployed on Railway.
- PocketBase is the source of truth for site content. Frontend code should read from PocketBase, not duplicate content in code unless there is an explicit fallback.
- PocketBase content schema summary lives in `POCKETBASE_CONTENT_REFERENCE.md`. Use it when preparing CMS updates or content generation.

## Default working style

- Prefer the smallest change that satisfies the issue.
- Keep edits local to the affected subsystem. Do not refactor unrelated files.
- Do not introduce new frameworks, major dependencies, or architectural patterns unless the issue explicitly asks for them.
- Preserve the existing Vue/Vite structure and naming.
- When a task looks ambiguous, risky, or cross-cutting, stop at a draft PR or hand off to a human/Codex instead of guessing.

## AI routing rules

- Copilot is appropriate for docs, copy changes, small UI fixes, focused workflow updates, and contained bugs.
- Codex should be used manually for multi-file refactors, data-flow redesign, complex debugging, or AI/deployment pipeline work.
- Do not make destructive changes, schema rewrites, or production data mutations from a general coding PR.
- `[Bug]` and `[Feature]` issues are the intended entry points for automatic code-to-PR routing.
- `[Content]` issues are reserved for CMS preview/apply and should not trigger normal coding PR work.

## Validation

- For frontend changes, prefer running `npm --prefix frontend run build`.
- If a command cannot be run, say so in the PR summary rather than inventing results.
- Do not claim Railway, Vercel, or PocketBase production changes were applied unless a dedicated workflow or a human explicitly performed them.
- Review AI-generated PRs against `.github/AI_REVIEW_HEURISTICS.md`.

## CMS and production safety

- General code-change PRs must not directly update production PocketBase data.
- PocketBase writes go through the dedicated CMS workflow and require structured inputs.
- Content issues with titles starting with `[Content]` can auto-generate a CMS preview from the issue body. Keep the issue fields structured and machine-readable.
- This is a transitional flow: today the issue still provides structured CMS inputs, while the target direction is natural-language content requests that AI converts into a structured proposal before preview/apply.
- Treat secrets, deployment settings, and production data as high-risk surfaces; minimize changes and explain them clearly in the PR.
