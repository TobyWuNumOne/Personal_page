# Agent Guide

Use GitHub Copilot coding agent for scoped repository work and use Codex manually for larger engineering tasks.

## Priorities

1. Keep changes narrow and reviewable.
2. Preserve the current frontend/CMS split.
3. Avoid production side effects from normal coding PRs.

## When to stop and defer

- The task requires a cross-cutting refactor.
- The task needs deep repo understanding beyond a few files.
- The task touches deployment, production data safety, or multiple systems at once.

In those cases, leave a clear draft or route the task to Codex/manual review.

## Repo conventions

- Frontend work lives under `frontend/`.
- PocketBase deployment/configuration lives under `cms/`.
- Structured CMS updates go through the dedicated GitHub workflow, not through ad hoc scripts in PRs.
- `[Bug]` and `[Feature]` issues are for code automation.
- `[Content]` issues are for CMS preview/apply, not code PR generation.

## Validation

- Frontend validation command: `npm --prefix frontend run build`
- If validation was not run, state that explicitly.
