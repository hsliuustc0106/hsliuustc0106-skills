---
name: tech-blog-post
description: Research, blueprint, write, and locally integrate evidence-backed technical blog posts. Use when the user asks to write, add, update, or organize a technical blog or article for a Next.js site, Markdown file, or Zhihu; provides source URLs, repositories, papers, issues, or PRs to turn into a post; or requests code-, architecture-, benchmark-, or contributor-grounded technical writing. Default to the repository-aware nextjs-site profile while preserving explicit markdown and backward-compatible zhihu profiles.
---

# Technical Blog Post

Create technical posts through a required narrative-blueprint approval gate.
Default to English and the `nextjs-site` profile. Keep source claims auditable,
make minimal repository changes, validate locally, and never publish implicitly.

## Non-negotiable rules

- Ask for the user's important starting references unless they already supplied
  them. Do not ask again when the references are clear.
- Prefer primary sources: official repositories, code, documentation, papers,
  issues, PRs, release notes, and reproducible benchmark records.
- Use secondary sources for framing only. Mark inference, experimental results,
  projections, and unverified claims explicitly.
- Link or cite reference figures, tables, and code rather than copying them.
  Copy an asset locally only when its reuse rights are clear.
- Require approval of the narrative blueprint before drafting or editing output
  files. After presenting it, stop and wait.
- Do not commit, push, publish, create a PR, or send content externally unless
  the user separately and explicitly requests that action.
- Keep repository edits surgical. Do not introduce a CMS, refactor shared blog
  architecture, or restyle unrelated pages without explicit authorization.

## Select the output profile

Use an explicitly requested profile when provided. Otherwise default to
`nextjs-site`.

- `nextjs-site`: Read [references/nextjs-site.md](references/nextjs-site.md)
  before repository discovery or file edits.
- `markdown`: Read [references/markdown.md](references/markdown.md) before
  writing the standalone draft.
- `zhihu`: Read [references/zhihu.md](references/zhihu.md) before composing.
  Preserve the legacy Chinese/Zhihu formatting behavior.

English is the default language. Honor an explicit language request. For an
established target site, match its language only when doing so does not conflict
with an explicit choice; surface a multilingual ambiguity in the blueprint.

## Workflow

### 1. Establish scope and references

Identify the topic, intended audience, target repository or output file, and
important starting references. Ask one concise question for missing important
references before self-discovery. State any material assumptions.

For `nextjs-site`, complete read-only repository discovery before proposing an
integration plan. If the blog structure is not confidently identifiable, stop
and ask rather than guessing paths or falling back silently.

### 2. Research only what the narrative needs

Read the supplied sources completely enough to understand their claims and
limitations. Follow their primary references, then inspect only the additional
code, PRs, issues, papers, or benchmarks needed to support the article. Do not
target an arbitrary number of PRs or citations.

For each material claim, record:

- the primary source and stable link;
- whether it is a fact, measured result, inference, projection, or opinion;
- the exact environment or topology for performance claims;
- relevant limitations, exclusions, or contradictory evidence.

Code and architecture analysis are optional. Include them when they materially
improve the thesis. Prefer concise pseudocode and links to pinned commits or
exact source locations over long copied excerpts.

### 3. Present the narrative blueprint and stop

Before drafting prose or modifying files, present:

1. Working title, target audience, and central thesis.
2. Intended reader takeaway and explicit non-goals.
3. Overall logical progression.
4. One row per proposed section with:
   - purpose;
   - main content;
   - key claims;
   - primary-source links;
   - proposed figures or code;
   - caveats;
   - transition to the next section.
5. Planned Next.js files and validation commands for `nextjs-site`; otherwise,
   the planned output file and format checks.

Place unresolved evidence or judgment under the relevant section's caveats.
Present materially different narrative interpretations when they would change
the article. Recommend one rather than choosing silently.

Ask the user to approve or revise the blueprint. Do not draft, edit, commit, or
publish until approval is explicit. If approval changes only part of the
blueprint, update the affected logic and confirm that the remaining structure
still holds.

### 4. Draft from the approved blueprint

Follow the approved section order, claims, scope, and source plan. Do not add a
new central claim or restructure the logic silently. If new evidence invalidates
the approved narrative, stop, explain the conflict, and request a blueprint
revision.

Write in an engineer's deep-dive voice: clear, evidence-led, accessible to the
approved audience, and precise about experimental boundaries. Keep copied
quotes short. Attach links near the claims or reused elements they support, and
include a references section when the target format benefits from one.

### 5. Integrate minimally

Follow the selected profile reference. For `nextjs-site`, create or update only
the approved post and the smallest required listing, metadata, or route files.
Preserve existing style, components, author conventions, and unrelated work.

### 6. Validate and hand off

Run the approved focused checks. At minimum for `nextjs-site`:

- verify route, slug, date, read time, and listing metadata agree;
- lint or format the changed files when supported;
- run the production build when available;
- check internal links and referenced local assets;
- run a diff/whitespace check.

Report unrelated pre-existing failures without fixing them. Summarize the
article, changed files, source policy, validation results, and any remaining
caveats. Stop with local changes unless the user separately requests a Git
publication workflow.
