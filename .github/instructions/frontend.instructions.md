---
applyTo: "frontend/**"
---

# Frontend Instructions

- Keep to the existing Vue 3 + Vite + Tailwind stack.
- Favor targeted component edits over broad rewrites.
- Do not change routes, CMS field names, or API URLs unless the issue explicitly requires it.
- Preserve existing page behavior and data-loading patterns.
- For content rendering changes, prefer fixing the smallest component or composable that owns the behavior.
- Validate frontend changes with `npm --prefix frontend run build` when possible.
- Prefer targeted bug fixes over opportunistic refactors.
- If the issue is about one UI behavior, avoid changing unrelated copy, spacing, or component structure.
