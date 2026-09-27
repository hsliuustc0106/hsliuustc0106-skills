# v2 validation / v2 验证记录

## Repository note

This is the historical validation report for the original v2 downloadable kit.
It is retained as provenance, not as a claim that every regenerated output has
been rendered. In this repository, run `scripts/check_templates.py` for each new
build. Automated checks do not render slides; visual review remains necessary.
The original raster previews and validation-results JSON are not checked in.

## Scope

The current delivery contains six primary Office files: two blank PPTX decks, two
POTX templates and two labelled PPTX guides. Each has 14 slides, 14 named custom
layouts, 233 slide-level placeholders (including picture/table placeholders),
133 non-placeholder layout shapes, and one prepared native table.

本次六份主要 Office 文件包括中英文空白 PPTX、POTX 模板和版式标注 PPTX。
每份含 14 页、14 种自定义版式、233 个页面级占位符、133 个固定版式图形，
以及一个预制原生表格。

## Checks performed

| Check | Result |
|---|---|
| ZIP integrity | All six files passed |
| PPTX / POTX content type | Correct presentation / template declarations |
| True 16:9 canvas | 13.333333 × 7.5 inches |
| Named custom layouts | 14 in every primary file |
| Duplicate shape IDs / placeholder indices | None detected within each slide/layout part |
| Shape geometry outside the canvas | None detected |
| Explicit object shadows | None detected |
| Native table | Five columns; one header plus ten body rows; frame and grid agree |
| Empty-table status emphasis | No selective highlights inherited from example data |
| Blank slide content | No visible slide text on pages 01–13 in either language |
| Blank closing page | Only the matching thank-you title and invitation are filled |
| Full rendering | All 14 pages of all six files rendered with LibreOffice |
| PPTX versus POTX | All 14 rendered pages match in each language |
| English versus Chinese blank geometry | First 13 rendered pages match pixel-for-pixel |
| Guide text page bounds | All extracted text spans remain within the rendered canvas |
| Chinese glyphs | No replacement-character text detected; inspected renders show Chinese glyphs |
| Reuse smoke test | Seven newly created layout-based slides rendered, including inserted picture and native table |
| Font binaries | None embedded or distributed |

Contact sheets of all English and Chinese guides and the blank layout library were
reviewed. Dense architecture and Chinese closing pages were also inspected at a
larger size. The visible previews reflect the final output, including the removal
of arbitrary table highlights and an explicit picture-zone label in guide mode.

已检查全部版式的预览，并放大查看复杂架构与中文致谢页。
预览对应最终文件：空白表无任意行强调，标注版封面另显示图片区提示。

## Compatibility limitations

Rendering used the available LibreOffice installation. Microsoft PowerPoint on the
recipient's machine was not separately tested; this is not a guarantee against all
cross-application differences. The Latin font declaration is Arial; Chinese text
explicitly uses Noto Sans CJK SC. Missing fonts may be substituted by the recipient's
software. Replace fonts consistently and inspect the completed deck after filling it.

python-pptx does not directly load the POTX main content type. The checker validates
that type, then creates a temporary in-memory PPTX view to inspect geometry. The
actual POTX files remain unchanged and were opened and rendered directly by LibreOffice.
The checker is not a full OOXML schema validator.

The layout reuse smoke test created seven new slides from the named layouts and
inserted a test picture and native table. It confirms behavior in the available
library/renderer, not every function of PowerPoint's interface. Duplicate prepared
slide 08 for exact table-cell styling and slide 14 for prefilled thank-you text.
Brand, source and page-number placeholders are intentionally empty, not automatic.

This is a style/template task; reference research was not fact-checked. Blank content
and labelled fields are not business evidence. Passing checks on empty templates
does not establish that future paragraphs, translations or charts will fit. Render
and inspect each future presentation after content is added.

本次使用 LibreOffice 渲染，未在收件人的 Microsoft PowerPoint 环境单独测试。
缺少字体可能触发替换，后续新增正文也可能改变换行。结构检查不是完整的 OOXML
模式验证，也不能验证事实或保证未来长文适配。表格和致谢建议分别复制第 08、14 张预制页。
字体、内容、页码及来源在正式使用时仍须逐项核对。

## Reproduce structural checks

```bash
python scripts/check_templates.py templates/blank-layouts-en.pptx templates/blank-layouts-zh-CN.pptx templates/reference-style-en.potx templates/reference-style-zh-CN.potx
python scripts/check_templates.py templates/layout-guide-en.pptx templates/layout-guide-zh-CN.pptx --guide
```

The original download recorded machine-readable checks in `validation-results.json`.
The previous starter's historical validation is retained separately as
`validation-v1.md`; it is not the validation report for this v2 template set.
