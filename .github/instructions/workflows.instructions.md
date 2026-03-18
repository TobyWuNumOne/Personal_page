---
applyTo: ".github/**"
---

# Workflow Instructions

- Keep GitHub Actions permissions minimal.
- Prefer explicit, structured workflow inputs over natural-language prompts.
- Never add a workflow that writes to production systems without a separate, auditable apply step.
- Do not add OpenAI API dependencies or prompt-based code mutation back into the repository workflows.
- If a workflow touches PocketBase, require preview-first behavior and clear failure messages.
