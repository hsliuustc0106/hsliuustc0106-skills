# Zhihu Profile

Preserve the original `tech-blog-post` behavior when the user explicitly asks
for Zhihu or selects the `zhihu` profile.

## Language and tone

- Default to Chinese unless the user requests another language.
- Write an accessible engineer's deep dive rather than a whitepaper.
- Keep code examples concise, normally 10–20 lines.

## Source and PR research

Start from the user's important references, then inspect only relevant PRs,
commits, code, contributors, and performance evidence. Do not require a fixed
PR count.

For useful PRs, gather the description, changed-file scope, illustrative code
changes, measured results, author, signed-off-by entries, and co-authors. Map a
GitHub noreply address to its embedded username; do not guess a GitHub handle
from a corporate email.

## Recommended article structure

Adapt the structure to the approved narrative. For optimization-focused posts,
prefer:

1. Overview.
2. Test environment.
3. Optimization dimensions with linked PRs.
4. Performance results and limitations.
5. PR index and contributors.
6. References.

## Zhihu-compatible formatting

- Use `<table>`, `<tr>`, `<td>`, and `<b>` for tables, not Markdown pipe tables.
- Use `<pre><code>...</code></pre>` for block code, not fenced code blocks.
- Use normal backticks for inline code.
- Use Markdown headings and bold text normally.
- Use full GitHub URLs for PRs and source references.

Write the approved article to `<model-or-topic>_blog.md` or the explicit target
path. Validate balanced HTML table/code tags, links, headings, and whitespace.
