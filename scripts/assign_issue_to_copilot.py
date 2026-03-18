#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Any
from urllib import request


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def graphql(query: str, variables: dict[str, Any]) -> dict[str, Any]:
    token = require_env("COPILOT_ASSIGNMENT_PAT")
    url = os.getenv("GITHUB_GRAPHQL_URL", "https://api.github.com/graphql")
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "GraphQL-Features": "issues_copilot_assignment_api_support,coding_agent_model_selection",
            "User-Agent": "personal-page-copilot-router",
        },
        method="POST",
    )
    with request.urlopen(req) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    if body.get("errors"):
        raise RuntimeError(f"GitHub GraphQL request failed: {body['errors']}")
    return body["data"]


def get_assignable_bot(owner: str, repo: str) -> tuple[str, str]:
    query = """
    query($owner: String!, $repo: String!) {
      repository(owner: $owner, name: $repo) {
        suggestedActors(capabilities: [CAN_BE_ASSIGNED], first: 20) {
          nodes {
            __typename
            ... on User {
              id
              login
            }
            ... on Bot {
              id
              login
            }
          }
        }
      }
    }
    """
    data = graphql(query, {"owner": owner, "repo": repo})
    nodes = data["repository"]["suggestedActors"]["nodes"]
    for node in nodes:
        if node.get("login") == "copilot-swe-agent":
            return node["id"], node["login"]
    raise RuntimeError("Could not find copilot-swe-agent in assignable users for this repository.")


def get_issue_id(owner: str, repo: str, issue_number: int) -> str:
    query = """
    query($owner: String!, $repo: String!, $issueNumber: Int!) {
      repository(owner: $owner, name: $repo) {
        issue(number: $issueNumber) {
          id
        }
      }
    }
    """
    data = graphql(query, {"owner": owner, "repo": repo, "issueNumber": issue_number})
    issue = data["repository"]["issue"]
    if not issue:
        raise RuntimeError(f"Issue #{issue_number} was not found.")
    return issue["id"]


def assign_issue(issue_id: str, actor_id: str) -> None:
    query = """
    mutation($assignableId: ID!, $actorIds: [ID!]!) {
      replaceActorsForAssignable(input: {assignableId: $assignableId, actorIds: $actorIds}) {
        assignable {
          ... on Issue {
            id
          }
        }
      }
    }
    """
    graphql(query, {"assignableId": issue_id, "actorIds": [actor_id]})


def write_outputs(bot_login: str) -> None:
    output_path = os.getenv("GITHUB_OUTPUT")
    if not output_path:
        return
    with open(output_path, "a", encoding="utf-8") as handle:
        handle.write(f"assignee_login={bot_login}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Assign an issue to the GitHub Copilot coding agent")
    parser.add_argument("--issue-number", type=int, required=True)
    args = parser.parse_args()

    repository = require_env("GITHUB_REPOSITORY")
    owner, repo = repository.split("/", 1)
    actor_id, bot_login = get_assignable_bot(owner, repo)
    issue_id = get_issue_id(owner, repo, args.issue_number)
    assign_issue(issue_id, actor_id)
    write_outputs(bot_login)
    print(json.dumps({"issue_number": args.issue_number, "assignee_login": bot_login}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
