#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from typing import Any


SECTION_RE = re.compile(r"^##\s+(.+?)\n(.*?)(?=^##\s+|\Z)", re.MULTILINE | re.DOTALL)
TITLE_PREFIX_RE = re.compile(r"^\[(bug|feature)\]\s*", re.IGNORECASE)
HIGH_RISK_PATTERNS = [
    ("deployment", re.compile(r"\bdeploy(?:ment)?\b", re.IGNORECASE)),
    ("Vercel", re.compile(r"\bvercel\b", re.IGNORECASE)),
    ("Railway", re.compile(r"\brailway\b", re.IGNORECASE)),
    ("secrets", re.compile(r"\bsecret(?:s)?\b", re.IGNORECASE)),
    ("environment variables", re.compile(r"\benv(?:ironment)?\b", re.IGNORECASE)),
    ("migrations", re.compile(r"\bmigration(?:s)?\b", re.IGNORECASE)),
    ("schema changes", re.compile(r"\bschema\b", re.IGNORECASE)),
    ("collection rules", re.compile(r"\bcollection rule\b", re.IGNORECASE)),
    ("production data", re.compile(r"\bproduction data\b", re.IGNORECASE)),
    ("PocketBase schema/rules", re.compile(r"\bpocketbase\s+(?:rule|schema|migration)\b", re.IGNORECASE)),
    ("AI pipeline", re.compile(r"\bai pipeline\b", re.IGNORECASE)),
]


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def load_issue() -> dict[str, Any]:
    event_path = require_env("GITHUB_EVENT_PATH")
    with open(event_path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    issue = payload.get("issue")
    if not issue:
        raise RuntimeError("GitHub event payload does not contain an issue")
    return issue


def parse_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    for match in SECTION_RE.finditer(body):
        sections[match.group(1).strip().lower()] = match.group(2).strip()
    return sections


def strip_markdown(raw: str) -> str:
    text = raw.strip()
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text.strip()


def section_has_content(sections: dict[str, str], name: str) -> bool:
    return bool(strip_markdown(sections.get(name, "")))


def parse_checked_items(raw: str) -> list[str]:
    items: list[str] = []
    for line in raw.splitlines():
        match = re.match(r"^\s*-\s*\[(x|X)\]\s*(.+?)\s*$", line)
        if match:
            items.append(match.group(2).strip().lower())
    return items


def detect_kind(title: str) -> str | None:
    match = TITLE_PREFIX_RE.match(title.strip())
    if not match:
        return None
    return match.group(1).lower()


def find_risks(title: str, sections: dict[str, str]) -> list[str]:
    findings: list[str] = []
    haystacks = [
        title,
        sections.get("affected area", ""),
        sections.get("scope", ""),
        sections.get("technical notes", ""),
        sections.get("current behavior", ""),
        sections.get("expected behavior", ""),
        sections.get("proposed behavior", ""),
    ]
    combined = "\n".join(haystacks)
    for label, pattern in HIGH_RISK_PATTERNS:
        if pattern.search(combined):
            findings.append(label)
    return findings


def validate_issue(issue: dict[str, Any]) -> dict[str, Any]:
    title = issue.get("title", "")
    body = issue.get("body", "")
    sections = parse_sections(body)
    kind = detect_kind(title)

    result: dict[str, Any] = {
        "issue_number": issue["number"],
        "issue_title": title,
        "issue_kind": kind or "",
        "eligible": "false",
        "reason": "",
    }

    if not kind:
        result["reason"] = "Issue title must start with [Bug] or [Feature]."
        return result

    missing: list[str] = []
    for section_name in ["summary", "acceptance criteria", "additional context"]:
        if not section_has_content(sections, section_name):
            missing.append(section_name)

    if kind == "bug":
        for section_name in ["current behavior", "expected behavior", "reproduction steps"]:
            if not section_has_content(sections, section_name):
                missing.append(section_name)
    else:
        for section_name in ["goal", "proposed behavior", "technical notes"]:
            if not section_has_content(sections, section_name):
                missing.append(section_name)

    if missing:
        result["reason"] = (
            "Issue is missing required sections for automation: "
            + ", ".join(sorted(dict.fromkeys(missing)))
            + "."
        )
        return result

    checked_acceptance = parse_checked_items(sections.get("acceptance criteria", ""))
    if not checked_acceptance:
        result["reason"] = "Acceptance criteria must include at least one checked item."
        return result

    risks = find_risks(title, sections)
    if risks:
        result["reason"] = (
            "Issue was routed away from automatic code PR because it appears to touch a high-risk area: "
            + ", ".join(sorted(dict.fromkeys(risks)))
            + "."
        )
        return result

    result["eligible"] = "true"
    result["reason"] = "Issue is eligible for Copilot coding agent automation."
    return result


def write_outputs(result: dict[str, Any]) -> None:
    output_path = os.getenv("GITHUB_OUTPUT")
    if not output_path:
        return
    with open(output_path, "a", encoding="utf-8") as handle:
        for key, value in result.items():
            handle.write(f"{key}={value}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Route code issues into automation eligibility")
    parser.parse_args()

    issue = load_issue()
    result = validate_issue(issue)
    write_outputs(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
