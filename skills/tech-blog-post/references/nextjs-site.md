# Next.js Site Profile

Use this profile for the default repository-aware blog workflow.

## Repository discovery

Perform read-only discovery before the narrative blueprint:

1. Read every applicable `AGENTS.md` and repository instruction file.
2. Inspect `package.json`, framework configuration, and available scripts.
3. Locate blog routes, content directories, listing or metadata sources,
   templates, and blog-specific documentation using `rg` or `rg --files`.
4. Inspect several recent representative posts and the listing render path.
5. Check Git status and preserve unrelated tracked and untracked work.
6. Identify the smallest file set and focused validation commands.

Confidence requires one clear convention for the post route or content file and
one clear mechanism for blog discovery/listing. If multiple live patterns could
be authoritative, describe them and ask which to use. Do not silently choose,
create a parallel blog system, or fall back to a Markdown-only result.

## Narrative blueprint integration fields

Include:

- proposed route, slug, title, date, read time, excerpt, tags, and language;
- existing post or template used as the structural reference;
- exact files to create or update;
- whether metadata, listing data, sitemap, feeds, or generated indexes require
  changes based on the repository's existing mechanism;
- focused lint, type-check, test, build, and link/asset checks.

## Minimal integration

- Follow the existing App Router, Pages Router, MDX, Markdown, CMS, or
  data-driven pattern already used by the site.
- Reuse existing components and styling. Create a helper only when the approved
  post requires it and reuse is not possible.
- Keep cited external assets remote unless reuse rights and repository patterns
  support a local copy.
- Add accessible link text, semantic headings, and responsive tables or code
  blocks consistent with nearby posts.
- Keep metadata and the listing entry synchronized with the rendered article.
- Do not edit shared navigation, global styling, dependencies, deployment, or
  unrelated content unless required by the approved blueprint.

## Validation

Prefer repository scripts over invented commands. Run, when available and
relevant:

1. changed-file formatting or lint;
2. type-check or framework compile;
3. production build or static export;
4. route/listing consistency checks;
5. internal-link and local-asset existence checks;
6. `git diff --check`.

If a repository-wide check fails outside the edited scope, show the focused
result and report the pre-existing failure separately. Do not repair it without
authorization.
