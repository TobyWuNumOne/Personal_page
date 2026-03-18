---
name: Content update
about: Request a PocketBase or site content update
title: "[Content] "
assignees: []
---

## Summary

Describe the content change request.

## Content Type

- PocketBase only
- PocketBase and frontend
- Frontend text/content only

## PocketBase Collection

Example: `pages`, `posts`, `projects`, `site_settings`

## Record Identifier

Provide a record id, slug, or another unique identifier if known.

## Fields To Update

List the fields that need to be changed.

## New Content

Describe the desired content or provide the exact new content when possible.

## CMS Update Mode

- [ ] Yes
- [ ] No, CMS update only
- [ ] Preview only first, then apply in the CMS workflow

## Acceptance Criteria

- [ ] The requested content is updated correctly
- [ ] No unrelated content is changed
- [ ] If applicable, the frontend reflects the new content

## Structured CMS Inputs

For the current v1 preview flow, these fields are still required so the workflow can prepare a CMS preview automatically.

- Collection: `pages`
- Record id or filter: `slug="about"`
- JSON field updates: `{"title":"About Me"}`

## Additional Context

Add links, screenshots, source text, or notes if needed.
The long-term goal is for AI to infer these structured fields from natural language, but the current workflow still expects them explicitly.
