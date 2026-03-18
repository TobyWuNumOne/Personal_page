#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from typing import Any


SECTION_RE = re.compile(r"^##\s+(.+?)\n(.*?)(?=^##\s+|\Z)", re.MULTILINE | re.DOTALL)
INLINE_FIELD_RE = re.compile(
    r"(?im)^(?:[-*]\s*)?(collection|record id or filter|json field updates|pocketbase collection|record identifier)\s*:\s*(.+)$"
)


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
        title = match.group(1).strip().lower()
        content = match.group(2).strip()
        sections[title] = content
    return sections


def normalize_inline_code(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        return value[1:-1].strip()
    return value


def parse_structured_lines(content: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line.startswith("-"):
            continue
        line = line[1:].strip()
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip().lower()] = normalize_inline_code(value.strip())
    return values


def parse_inline_fields(body: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for key, value in INLINE_FIELD_RE.findall(body):
        values[key.strip().lower()] = normalize_inline_code(value.strip())
    return values


def parse_identifier(raw: str | None) -> tuple[str | None, str | None]:
    value = normalize_inline_code(raw or "")
    if not value:
        return None, None
    if "=" in value or "\"" in value or "'" in value:
        return None, value
    return value, None


def maybe_parse_json(raw: str | None) -> dict[str, Any] | None:
    if not raw:
        return None
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def parse_fields_list(raw: str | None) -> list[str]:
    if not raw:
        return []
    fields: list[str] = []
    for line in raw.splitlines():
        item = line.strip().lstrip("-").strip()
        if not item:
            continue
        parts = [part.strip() for part in item.split(",")]
        fields.extend(part for part in parts if part)
    return fields


def derive_updates(sections: dict[str, str], structured: dict[str, str]) -> dict[str, Any]:
    raw_json = structured.get("json field updates") or sections.get("new content")
    parsed = maybe_parse_json(raw_json)
    if parsed is not None:
        return parsed

    fields = parse_fields_list(sections.get("fields to update"))
    new_content = sections.get("new content", "").strip()
    if len(fields) == 1 and new_content:
        return {fields[0]: new_content}

    raise RuntimeError(
        "Unable to derive JSON field updates from the issue body. "
        "Populate `Structured CMS Inputs -> JSON field updates` with a JSON object."
    )


def build_result(issue: dict[str, Any]) -> dict[str, Any]:
    body = issue.get("body") or ""
    sections = parse_sections(body)
    structured = parse_structured_lines(sections.get("structured cms inputs", ""))
    inline_fields = parse_inline_fields(body)

    collection = normalize_inline_code(
        structured.get("collection")
        or inline_fields.get("collection")
        or inline_fields.get("pocketbase collection")
        or sections.get("pocketbase collection", "")
    )
    if not collection:
        raise RuntimeError("Missing PocketBase collection in issue body")

    raw_identifier = (
        structured.get("record id or filter")
        or inline_fields.get("record id or filter")
        or inline_fields.get("record identifier")
        or sections.get("record identifier")
    )
    record_id, record_filter = parse_identifier(raw_identifier)
    updates = derive_updates(
        sections,
        {
            **inline_fields,
            **structured,
        },
    )

    return {
        "issue_number": issue["number"],
        "issue_title": issue["title"],
        "collection": collection,
        "record_id": record_id,
        "filter": record_filter,
        "updates_json": json.dumps(updates, ensure_ascii=False),
    }


def write_outputs(result: dict[str, Any]) -> None:
    output_path = os.getenv("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as handle:
            for key, value in result.items():
                if value is None:
                    value = ""
                handle.write(f"{key}={value}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse a content issue into CMS workflow inputs")
    parser.parse_args()

    issue = load_issue()
    result = build_result(issue)
    write_outputs(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
