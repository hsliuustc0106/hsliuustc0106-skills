# Formal slide library

The user approved this visual family and its reusable layouts on 2026-10-08.
The source is `../assets/templates.pptx`; the visual catalog is
`../assets/templates-preview.png`. This is a template library, not a required
deck order. Choose by name; the positions below identify the current exemplars.
Append new types rather than renumbering existing ones.

## Layout selection

| Position | Name / user aliases | Use and composition |
| --- | --- | --- |
| 1 | Cover / 封面 / section divider | Topic, framing promise, presenter/date, brief navigation. A section divider can omit the agenda. |
| 2 | Overview / 总览 / 要点 | Three parallel cards and a shared implication; adapt to two or four cards when appropriate. |
| 3 | Figure with explanation / 图文 / 证据 | Principal screenshot, chart, or case on the left; observations, value, and implication on the right. |
| 4 | Comparison / 对比 / 矩阵 | Native editable table with shared comparison dimensions. Also supports responsibility and requirement mappings. |
| 5 | Workflow / 流程 / 步骤 | Four stages with labeled order and input/output context; adapt stage count to the task. |
| 6 | Architecture / 架构 / 分层 | Entry point, application groups, and shared support capabilities; label relationships and abstraction level. |
| 7 | Roadmap / 路线图 / 计划 | Three stages, time windows, work, deliverables, owner, and decision checkpoint. |
| 8 | Summary and actions / 总结 / 行动 | Main conclusions, value, and unresolved questions above concrete actions, owners, and timing. |
| 9 | Product insight / 产品洞察 | Product screenshot or key workflow on the left; four analytical dimensions on the right; product implication below. |
| 10 | Thank You / 致谢 | Closing message, openJiuwen GitHub, community repository, and Bilibili links. |

Examples: “use 产品洞察 for this product,” “use architecture and roadmap,” or
“choose layouts for a three-page update.” Layout selection does not determine
which facts to assert or authorize additional research or publication.

## Product-insight page

This is the user's preferred product-analysis structure, informed by the earlier
Claude Science and Muse pages. Keep the four dimensions unless the user changes
the brief:

- **目标人群 / Target users:** actual users, their roles, and the paying party.
- **用户场景 / User scenario:** triggering situation, inputs, task, and useful outcome.
- **核心痛点 / Core pain:** the current workflow's friction and its time, cost,
  or quality consequences. Connect product capabilities to those pains.
- **商业模式 / Business model:** who pays, how charging works, and why a user
  would purchase or renew. A pricing list alone is insufficient analysis.

Put the **open-source status** in the small badge below the title on the right:
`开源状态：开源 / 部分开源 / 未开源`. Replace the options with the actual finding;
use `待核验` when unresolved. Check the relevant official repository and license:
publicly viewable code alone does not establish open-source licensing. Specify
what is partial when code, service, model weights, or other components differ.

The left region contains a product screenshot, documented key workflow, or
attributable case—not invented UI. Use a caption to identify its provenance and
scope. If no meaningful image is available, use an explicitly labeled workflow
or an appropriately adapted text-first composition. The bottom takeaway should
explain what the product teaches us about user value, sustained use, or payment.

Record product version, pricing scope and date, and sources. Distinguish a vendor
demo or customer anecdote from independent measurement. Do not carry old product
claims from the historical examples into new research without verification.

## Shared style

| Element | Saved default |
| --- | --- |
| Canvas | 16:9, approximately 13.333 × 7.5 inches |
| Background | White `#FFFFFF`; covers retain the saved decorative illustration |
| Primary | Blue `#245BFF` for titles, emphasis, and table headers |
| Main / secondary text | Navy `#182B4D` / gray `#64748B` |
| Neutral cards / dividers | `#F3F6FD` / `#DCE5F1` |
| Secondary groups | Teal `#008598` with `#EAF7F5`; purple `#7044B8` with `#F2EDFA` |
| Font family | Arial for Latin; Microsoft YaHei is the declared CJK companion; verify actual fallback in the renderer |
| Sizes | Title 28 pt; card heading 20 pt; body 18 pt; compact diagram/table labels about 16 pt; captions/footer 9–13 pt |
| Header | Title left; compact chapter badge right; context and optional status underneath |
| Main region | Roughly 1.9–6.25 inches vertically, with about 0.6-inch outer margins |
| Conclusion | Pale full-width takeaway around y=6.37 inches, unless the visual already carries the implication |
| Footer | Fine divider, project/date/status as relevant, openJiuwen branding, actual slide number |

These are defaults, not reasons to distort evidence or crowd content. Keep the
typographic hierarchy and consistent spacing while allowing the layout to adapt.
Shorten or restructure narrative before reducing its font size; captions are not
a body-text style. New figures use matching colors, labels, borders, and line
treatments. A chart's color mapping stays stable across related slides.

Preserve the saved branding for this presentation family. When the user specifies
another organization or theme, replace the associated marks and closing links.
Do not leave openJiuwen promotional links on an unrelated organization's deck.

## Closing links

The user confirmed the Bilibili account on 2026-10-08. The closing exemplar has
real hyperlinks, not only printed URLs:

- Organization: https://github.com/openJiuwen-ai
- Community: https://github.com/openJiuwen-ai/community
- Bilibili: https://space.bilibili.com/3690984464451987

Retain these destinations when adapting an openJiuwen closing page. Change the
footer's page number to the actual presentation order. A content-only brief does
not require a closing page.

## Library maintenance

The selection helper takes one-based positions from this catalog and preserves
the selected slides' native objects and relationships. It accepts unique
positions; duplicate pages through the chosen authoring engine when repeated
layouts are required. Renumber actual presentation footers and replace the
template-number badge with the intended chapter label.

For a new reusable type, add one clean exemplar to the end of the library and
append its position, name, purpose, and important semantic slots to the table.
Regenerate the preview from the updated library. Keep the original layouts and
their positions intact; omit one-off variations that existing layouts can handle.

Stage the expanded `.pptx` and verify native tables, images, notes, and links
before installing it. Do not save customer data or task-specific source media
into the skill. A supplied design for an unrelated brand is not automatically a
new member of this visual family.

## Provenance

The bundled deck is the generic ten-layout pack approved by the user on
2026-10-08, including the product-insight status badge and GitHub/Bilibili
closing links. It draws on these user-supplied presentations:

- Agent application incubation (user-provided presentation)
- Business insights and planning (user-provided presentation)
- Mission and innovation opportunities (user-provided presentation)

These presentations are evidence of the preferred writing and visual patterns,
not independent evidence of their historical product claims.
