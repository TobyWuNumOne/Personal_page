#!/usr/bin/env python3
import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib import error, request

from openai import OpenAI


REPO_ROOT = Path(__file__).resolve().parents[1]
MAX_CONTEXT_FILES = 40
MAX_FILE_CHARS = 12000
TEXT_EXTENSIONS = {
    ".css",
    ".env.example",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".ts",
    ".tsx",
    ".txt",
    ".vue",
    ".yaml",
    ".yml",
}
SKIP_PARTS = {
    ".git",
    ".github",
    "dist",
    "build",
    "coverage",
    "node_modules",
    "__pycache__",
}


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def load_event() -> dict[str, Any]:
    event_path = require_env("GITHUB_EVENT_PATH")
    with open(event_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    cmd = ["git", *args]
    logging.info("Running git command: %s", " ".join(cmd))
    return subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        check=check,
        capture_output=True,
        text=True,
    )


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def collect_repo_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if should_skip(path.relative_to(REPO_ROOT)):
            continue
        suffix = path.suffix.lower()
        if suffix not in TEXT_EXTENSIONS and path.name not in {"README", "README.md"}:
            continue
        files.append(path)
    files.sort()
    return files[:MAX_CONTEXT_FILES]


def read_context() -> str:
    sections: list[str] = []
    for path in collect_repo_files():
        rel = path.relative_to(REPO_ROOT)
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            logging.warning("Skipping non-utf8 file: %s", rel)
            continue
        trimmed = content[:MAX_FILE_CHARS]
        if len(content) > MAX_FILE_CHARS:
            trimmed += "\n...[truncated]..."
        sections.append(f"FILE: {rel}\n```\n{trimmed}\n```")
    return "\n\n".join(sections)


def sanitize_branch_fragment(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")
    return cleaned or "change"


def strip_code_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def build_prompt(event: dict[str, Any]) -> str:
    issue = event["issue"]
    labels = [label["name"] for label in issue.get("labels", [])]
    repo_name = event["repository"]["full_name"]
    return f"""
You are an autonomous software engineer working inside the Git repository "{repo_name}".

Task:
- Read the GitHub issue below.
- Propose safe repository changes that can be applied automatically.
- Prefer small, surgical edits over broad rewrites.
- If the issue is ambiguous or unsafe to automate, return no file edits and explain why.
- If the issue appears to be content-related, set pocketbase.should_update to true and provide a small JSON payload describing the CMS update.

Issue number: {issue["number"]}
Issue title: {issue["title"]}
Issue labels: {json.dumps(labels, ensure_ascii=False)}
Issue body:
{issue.get("body") or "(empty)"}

Repository context:
{read_context()}

Return valid JSON only with this shape:
{{
  "summary": "short explanation",
  "branch_suffix": "kebab-case-short-name",
  "commit_message": "short git commit message",
  "pr_title": "PR title",
  "pr_body": "markdown body",
  "files": [
    {{
      "path": "relative/path/to/file",
      "action": "create_or_update",
      "content": "full file contents"
    }}
  ],
  "pocketbase": {{
    "should_update": true,
    "reason": "why",
    "payload": {{}}
  }}
}}

Rules:
- Only use action=create_or_update.
- Only write text files.
- Return full file contents for each file.
- Do not include binaries.
- Do not include explanations outside JSON.
- Keep files unchanged if you are not confident.
""".strip()


def request_plan(event: dict[str, Any]) -> dict[str, Any]:
    client = OpenAI(api_key=require_env("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL") or "gpt-4.1"
    prompt = build_prompt(event)
    logging.info("Requesting implementation plan from OpenAI model %s", model)
    response = client.responses.create(
        model=model,
        input=prompt,
        temperature=0.2,
    )
    payload = strip_code_fences(response.output_text)
    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Model response was not valid JSON: {exc}") from exc


def assert_safe_path(rel_path: str) -> Path:
    target = (REPO_ROOT / rel_path).resolve()
    if not str(target).startswith(str(REPO_ROOT.resolve())):
        raise RuntimeError(f"Refusing to write outside repository: {rel_path}")
    return target


def apply_file_changes(file_ops: list[dict[str, Any]]) -> list[str]:
    written: list[str] = []
    for item in file_ops:
        if item.get("action") != "create_or_update":
            raise RuntimeError(f"Unsupported file action: {item.get('action')}")
        rel_path = item["path"]
        content = item["content"]
        if not isinstance(rel_path, str) or not isinstance(content, str):
            raise RuntimeError("Each file operation must include string path and content")
        target = assert_safe_path(rel_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written.append(rel_path)
        logging.info("Wrote file: %s", rel_path)
    return written


def git_status_porcelain() -> str:
    result = run_git("status", "--short", check=True)
    return result.stdout.strip()


def ensure_clean_start() -> None:
    status = git_status_porcelain()
    if status:
        raise RuntimeError(
            "Repository is not clean. Refusing to run automated branch changes.\n"
            f"Current status:\n{status}"
        )


def create_branch(branch_name: str) -> None:
    run_git("checkout", "-b", branch_name)


def commit_and_push(branch_name: str, message: str) -> None:
    run_git("add", ".")
    run_git("config", "user.name", "github-actions[bot]")
    run_git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    run_git("commit", "-m", message)
    run_git("push", "--set-upstream", "origin", branch_name)


def github_api(
    method: str,
    url: str,
    token: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        method=method,
        data=data,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "ai-dev-pipeline",
        },
    )
    try:
        with request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API request failed: {exc.code} {details}") from exc


def create_pull_request(
    event: dict[str, Any],
    branch_name: str,
    plan: dict[str, Any],
) -> str:
    repo = event["repository"]["full_name"]
    default_branch = event["repository"]["default_branch"]
    issue_number = event["issue"]["number"]
    token = require_env("GITHUB_TOKEN")
    api_url = f"https://api.github.com/repos/{repo}/pulls"
    pr_body = plan.get("pr_body") or ""
    if f"Closes #{issue_number}" not in pr_body:
        pr_body = f"{pr_body}\n\nCloses #{issue_number}".strip()
    payload = {
        "title": plan.get("pr_title") or f"AI: Resolve issue #{issue_number}",
        "head": branch_name,
        "base": default_branch,
        "body": pr_body,
    }
    response = github_api("POST", api_url, token, payload)
    return response["html_url"]


def maybe_update_pocketbase(event: dict[str, Any], plan: dict[str, Any]) -> None:
    pocketbase = plan.get("pocketbase") or {}
    if not pocketbase.get("should_update"):
        logging.info("PocketBase update not requested by model plan")
        return

    endpoint = os.getenv("POCKETBASE_API")
    if not endpoint:
        logging.info("Skipping PocketBase update because POCKETBASE_API is not configured")
        return

    payload = {
        "issue": {
            "number": event["issue"]["number"],
            "title": event["issue"]["title"],
            "labels": [label["name"] for label in event["issue"].get("labels", [])],
        },
        "reason": pocketbase.get("reason") or "content-related issue",
        "payload": pocketbase.get("payload") or {},
    }
    req = request.Request(
        endpoint,
        method="POST",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "ai-dev-pipeline",
        },
    )
    try:
        with request.urlopen(req) as resp:
            logging.info("PocketBase API update completed with status %s", resp.status)
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"PocketBase API request failed: {exc.code} {details}") from exc


def main() -> int:
    configure_logging()
    try:
        event = load_event()
        issue = event.get("issue")
        if not issue:
            raise RuntimeError("GitHub event does not include an issue payload")

        logging.info("Processing issue #%s: %s", issue["number"], issue["title"])
        ensure_clean_start()

        plan = request_plan(event)
        logging.info("OpenAI summary: %s", plan.get("summary", "(none)"))

        file_ops = plan.get("files") or []
        if not file_ops:
            maybe_update_pocketbase(event, plan)
            logging.info("No file changes proposed. Exiting without branch creation.")
            return 0

        branch_suffix = sanitize_branch_fragment(
            str(plan.get("branch_suffix") or issue["title"])
        )
        branch_name = f"ai/issue-{issue['number']}-{branch_suffix}"
        create_branch(branch_name)

        written_files = apply_file_changes(file_ops)
        logging.info("Applied %s file changes", len(written_files))

        status = git_status_porcelain()
        if not status:
            maybe_update_pocketbase(event, plan)
            logging.info("No git diff produced after writing files. Exiting cleanly.")
            return 0

        commit_message = plan.get("commit_message") or f"AI update for issue #{issue['number']}"
        commit_and_push(branch_name, commit_message)
        pr_url = create_pull_request(event, branch_name, plan)
        logging.info("Created pull request: %s", pr_url)

        try:
            maybe_update_pocketbase(event, plan)
        except Exception:
            logging.exception("PocketBase update failed but git/PR workflow already completed")

        return 0
    except Exception as exc:
        logging.exception("AI pipeline failed: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
