#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Any
from urllib import error, parse, request


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def normalize_base_url(raw: str) -> str:
    base = raw.rstrip("/")
    for suffix in ("/api", "/_"):
        if base.endswith(suffix):
            base = base[: -len(suffix)]
    return base


def load_updates(raw: str) -> dict[str, Any]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"updates_json is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("updates_json must decode to a JSON object")
    return payload


def clean_optional(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def make_request(
    method: str,
    url: str,
    *,
    token: str | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = None
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "cms-sync-workflow",
    }
    if token:
        headers["Authorization"] = token
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = request.Request(url, method=method, data=data, headers=headers)
    try:
        with request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"PocketBase request failed: {exc.code} {details}") from exc


def authenticate(base_url: str) -> str:
    token = os.getenv("POCKETBASE_SUPERUSER_TOKEN")
    if token:
        return token if token.lower().startswith("bearer ") else f"Bearer {token}"

    email = require_env("POCKETBASE_SUPERUSER_EMAIL")
    password = require_env("POCKETBASE_SUPERUSER_PASSWORD")
    auth_candidates = [
        (
            f"{base_url}/api/collections/_superusers/auth-with-password",
            {"identity": email, "password": password},
        ),
        (
            f"{base_url}/api/admins/auth-with-password",
            {"identity": email, "password": password},
        ),
        (
            f"{base_url}/api/admins/auth-with-password",
            {"email": email, "password": password},
        ),
    ]
    errors: list[str] = []
    for auth_url, payload in auth_candidates:
        try:
            auth = make_request("POST", auth_url, payload=payload)
            auth_token = auth.get("token")
            if not auth_token:
                raise RuntimeError("PocketBase auth response did not include a token")
            return f"Bearer {auth_token}"
        except RuntimeError as exc:
            errors.append(f"{auth_url}: {exc}")

    joined = "\n".join(errors)
    raise RuntimeError(f"PocketBase authentication failed with all known endpoints:\n{joined}")


def resolve_record(
    base_url: str,
    token: str,
    collection: str,
    record_id: str | None,
    record_filter: str | None,
) -> dict[str, Any]:
    record_id = clean_optional(record_id)
    record_filter = clean_optional(record_filter)
    collection_part = parse.quote(collection, safe="")
    if record_id:
        record_part = parse.quote(record_id, safe="")
        url = f"{base_url}/api/collections/{collection_part}/records/{record_part}"
        try:
            return make_request("GET", url, token=token)
        except RuntimeError as exc:
            if "404" not in str(exc) or not record_filter:
                raise RuntimeError(
                    f"Record `{record_id}` was not found in collection `{collection}`"
                ) from exc

    if not record_filter:
        raise RuntimeError("Either --record-id or --filter is required")

    query = parse.urlencode({"page": 1, "perPage": 1, "filter": record_filter})
    url = f"{base_url}/api/collections/{collection_part}/records?{query}"
    listing = make_request("GET", url, token=token)
    items = listing.get("items") or []
    if len(items) != 1:
        raise RuntimeError(
            f"Filter must resolve to exactly one record, got {len(items)} matches"
        )
    return items[0]


def write_summary(lines: list[str]) -> None:
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    with open(summary_path, "a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def preview_changes(record: dict[str, Any], updates: dict[str, Any]) -> list[str]:
    lines = [
        "## CMS Sync Preview",
        "",
        f"- Record ID: `{record.get('id', '(unknown)')}`",
        "",
        "| Field | Current | Proposed |",
        "| --- | --- | --- |",
    ]
    for key, value in updates.items():
        current = json.dumps(record.get(key), ensure_ascii=False)
        proposed = json.dumps(value, ensure_ascii=False)
        lines.append(f"| `{key}` | `{current}` | `{proposed}` |")
    return lines


def apply_update(
    base_url: str,
    token: str,
    collection: str,
    record_id: str,
    updates: dict[str, Any],
) -> dict[str, Any]:
    collection_part = parse.quote(collection, safe="")
    record_part = parse.quote(record_id, safe="")
    url = f"{base_url}/api/collections/{collection_part}/records/{record_part}"
    return make_request("PATCH", url, token=token, payload=updates)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preview or apply PocketBase record updates")
    parser.add_argument("--collection", required=True)
    parser.add_argument("--record-id")
    parser.add_argument("--filter")
    parser.add_argument("--updates-json", required=True)
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    updates = load_updates(args.updates_json)
    base_url = normalize_base_url(require_env("POCKETBASE_URL"))
    token = authenticate(base_url)
    record = resolve_record(
        base_url,
        token,
        args.collection.strip(),
        args.record_id,
        args.filter,
    )

    summary_lines = preview_changes(record, updates)
    write_summary(summary_lines)

    if not args.apply:
        print("\n".join(summary_lines))
        return 0

    updated = apply_update(base_url, token, args.collection, record["id"], updates)
    apply_lines = [
        "## CMS Sync Applied",
        "",
        f"- Collection: `{args.collection}`",
        f"- Record ID: `{updated['id']}`",
        f"- Updated fields: `{', '.join(sorted(updates))}`",
    ]
    write_summary(apply_lines)
    print("\n".join(apply_lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
