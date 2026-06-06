---
name: tech-blog-post
description: Generate a Zhihu-formatted technical blog post from a source article URL (WeChat MP, etc.) by analyzing PRs in the current repo for technical depth — code blocks, tables, contributor info, and performance data. Use when the user says "write a blog post", "post to Zhihu", "write a Zhihu article", or provides a source article URL and asks to organize it into a blog post.
license: MIT
---

# Tech Blog Post Generator

Generate a Zhihu-formatted technical blog post from a source article. Extracts key topics from the article, searches the repo for related PRs, pulls technical details (code diffs, commit messages), and outputs a ready-to-publish `.md` file with HTML tables and `<pre>` code blocks for Zhihu compatibility.

## Workflow

### Step 1: Fetch Source Article

Try multiple methods in order until content is retrieved:

1. **curl with WeChat mobile UA** (for mp.weixin.qq.com):
   ```bash
   curl -sL -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38" "<URL>" | python3 -c "
   import sys, html, re
   content = sys.stdin.read()
   clean = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
   clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
   clean = re.sub(r'<[^>]+>', '\n', clean)
   clean = html.unescape(clean)
   lines = [l.strip() for l in clean.split('\n') if l.strip() and len(l.strip()) > 10]
   print('\n'.join(lines[:100]))
   "
   ```

2. **curl with standard browser UA** for other sources.
3. **WebFetch tool** for accessible URLs.

Extract from the article:
- Title / topic
- Model names mentioned
- Key technical claims (performance numbers, optimizations)
- Framework / hardware references

### Step 2: Discover Related PRs

Search the repo for PRs related to the models and topics found:

```bash
# Search by model name
git log --oneline --all --grep="<ModelName>" --since="<cutoff-date>" | head -30

# Search by optimization keywords (fused, perf, attention, parallel, quant, etc.)
git log --oneline --all --grep="<keyword>" --since="<cutoff-date>" | head -20
```

Filter PRs to those most relevant to the article's narrative. Aim for 10-15 key PRs.

### Step 3: Extract Technical Details

For each selected PR, extract:

```bash
# PR description and metadata
git log --format="%H %s%n%b" <commit> -1

# Changed files and scope
git diff <commit>^..<commit> --stat | tail -5

# Key code changes (focus on the most illustrative diffs)
git show <commit> -- <relevant_file> | head -80
```

Prioritize PRs that:
- Show a clear before/after pattern (good for code blocks)
- Have measurable performance impact
- Demonstrate architectural decisions

### Step 4: Gather Contributor Info

```bash
for pr in <pr_numbers>; do
  commit=$(git log --oneline --all --grep="#$pr" --format="%H" | head -1)
  if [ -n "$commit" ]; then
    echo "=== PR #$pr ==="
    git log --format="Author: %an <%ae>" $commit -1
    git log --format="%b" $commit -1 | grep -i "Signed-off-by:" | head -5
    git log --format="%b" $commit -1 | grep -i "Co-authored-by:" | head -5
    echo ""
  fi
done
```

Map email addresses to GitHub usernames:
- `XXXXX+USERNAME@users.noreply.github.com` → `USERNAME`
- For corporate emails, use the Signed-off-by name as the GitHub ID

### Step 5: Compose the Blog Post

Structure the post following this template:

```
# <Title>：<Subtitle>

## 1. Overview
<2-3 paragraphs: background, what this covers, key result>

## 2. Test Environment
<HTML table: component | spec>

## 3. Optimization Dimensions
### 3.1 <Dimension Name>（#PR1, #PR2）
<Explanation + code blocks + technical analysis>
### 3.2 ...
... (repeat for each optimization dimension)

## 4. Performance Results
<HTML table: configuration | metric | speedup>

## 5. PR Index & Contributors

A single combined section with one table:

<table>
<tr><td><b>PR</b></td><td><b>Category</b></td><td><b>Description</b></td><td><b>Contributors</b></td></tr>
<tr><td><a href="https://github.com/...">#1234</a></td><td>Perf</td><td>Summary of the change</td><td>@github_id</td></tr>
...
</table>

- PR numbers link directly to GitHub PR URLs
- Contributors column lists GitHub @ handles
- Rows sorted by category (Perf → Feature → Bugfix → Quant → Enhancement)

## 6. References
<Bullet list: original article, repos, models>
```

### Step 6: Format for Zhihu

**Critical formatting rules for Zhihu compatibility:**

- **Tables**: Use `<table>` HTML tags, NOT markdown pipe tables. Include `<tr>`, `<td>`, `<b>` tags.
- **Code blocks**: Use `<pre><code>...</code></pre>` tags, NOT ``` fences.
- **Inline code**: Use backticks as normal (Zhihu handles these).
- **Bold**: Use `**text**` or `<b>text</b>`.
- **Headings**: Use `##` and `###` as normal.

### Step 7: Write Output File

Write to `<model_or_topic>_blog.md` in the current working directory.

## Important Notes

- Default language: Chinese (unless the article is in English)
- Tone: Technical but accessible — like an engineer's deep-dive, not a whitepaper
- Code blocks: Keep them concise (~10-20 lines each), focus on the most illustrative parts
- PR links: Use full GitHub URLs (not just #numbers)
- Always include the original article URL in References
- If source article can't be fetched, ask the user to paste the content
