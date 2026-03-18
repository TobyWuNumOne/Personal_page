---
applyTo: "cms/**,scripts/cms_*.py,AI_NOTES.md"
---

# CMS Instructions

- PocketBase is treated as production data infrastructure, not a free-form AI target.
- CMS automation must use structured fields such as collection, record identifier, and explicit update payloads.
- Prefer preview or read-only inspection before apply.
- Avoid schema changes unless they are explicitly requested and separately reviewed.
- Document any PocketBase credential assumptions in code comments or workflow summaries.
