# Copilot Instructions

This repository uses GitHub Copilot coding agent for narrow, reviewable work and uses Codex manually for deeper implementation, refactors, and debugging.

## Repository shape

- `frontend/` is the main application. It is a Vue 3 + Vite + Tailwind SPA deployed on Vercel.
- `cms/` contains the PocketBase container setup deployed on Railway.
- PocketBase is the source of truth for site content. Frontend code should read from PocketBase, not duplicate content in code unless there is an explicit fallback.

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

## Validation

- For frontend changes, prefer running `npm --prefix frontend run build`.
- If a command cannot be run, say so in the PR summary rather than inventing results.
- Do not claim Railway, Vercel, or PocketBase production changes were applied unless a dedicated workflow or a human explicitly performed them.

## CMS and production safety

- General code-change PRs must not directly update production PocketBase data.
- PocketBase writes go through the dedicated CMS workflow and require structured inputs.
- Treat secrets, deployment settings, and production data as high-risk surfaces; minimize changes and explain them clearly in the PR.
