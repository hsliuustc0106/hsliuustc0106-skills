---
name: Prepare X release post
description: >-
  Use when preparing an X (Twitter) post announcing a GitHub release: gather
  highlights, include the release link, and optionally attach GIFs/videos from
  recently merged PRs.
---
# Prepare X release post

Generic recipe for drafting (and optionally publishing) an X post about a new GitHub release. Keep repo-specific names, handles, and standing team rules out of this skill; pass them in the ask.

## Goal

A short X-ready draft that includes:
1. Version + product name
2. A few release highlights (not the full changelog)
3. The release URL
4. Optional media (GIF/video) from recent merged PRs or repo demo assets

## Steps

1. **Resolve the release**
   - Confirm `owner/repo`, tag (e.g. `v0.2.0`), and whether the GitHub release already exists.
   - If creating the release is in scope: read `CHANGELOG` Unreleased (or commits since the previous tag), draft notes, create the release/tag on the agreed target (usually `main`), then use that URL.
   - Release URL shape: `https://github.com/<owner>/<repo>/releases/tag/<tag>`.

2. **Cut highlights**
   - Prefer user-facing wins (new models/agents, demos, benchmarks, UX) over CI/docs churn.
   - Aim for 3–5 bullets in the release notes; compress to 1–3 punchy clauses for X.
   - Stay under ~260 characters for the post body so a link still fits cleanly (or use a thread if the user wants more).

3. **Find media (when asked or useful)**
   - Search PRs merged since the previous tag for demo/gif/video/mp4/webm/showcase mentions.
   - Also check common asset paths (`docs/assets/demos/`, `docs/results/`, recipe folders).
   - Rank short showcase GIFs first; note path/URL, PR number, and what it shows.
   - Present 2–4 candidates and let the user pick before attaching.

4. **Draft the post**
   - Lead with the version ship line, then highlights, then the release link on its own line.
   - Do not invent stats or claims; only use changelog/PR/release facts.
   - Show the full draft in chat for approval.

5. **Publish**
   - The X connector does **not** post tweets. After approval: either hand the draft to the user to paste, or post via the signed-in browser if they asked for that.
   - Never post without an explicit yes on the final text (and media choice if any).

## Done when

- Release URL is real and in the draft
- Highlights match the release notes
- User has an approved draft (and media pick if requested)
- Post is either published as asked or clearly left for the user to paste
