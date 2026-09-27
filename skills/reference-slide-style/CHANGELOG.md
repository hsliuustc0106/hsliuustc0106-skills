## Repository source distribution

- Publish the English and Simplified Chinese v2 skill under `skills/reference-slide-style/`.
- Rebuild the optional v1 geometry blueprint from tracked JSON when its PPTX is absent.
- Keep generated Office files and raster previews out of Git; publish the six Office
  templates through the dedicated build workflow artifact.
- Add clean-checkout regression tests. Preserve the original visual system, layouts,
  blank-content rules, localization, and historical validation notes.

# v2 changes / v2 更新

- Added blank editable decks in English and Simplified Chinese; pages 01–13 have no visible content text.
- Added true POTX files and fourteen named custom layouts in each language.
- Added single-content and two-column layouts; exposed the closing-decision variant separately.
- Added final “Thank you / Questions & discussion” and “谢谢聆听／欢迎交流与提问” pages.
- Added full Chinese skill and quick-start guide, plus localized layout names, prompts and notes.
- Added labelled layout guides and rendered previews without example business claims.
- Preserved formatting in empty paragraphs and placed background geometry on layouts.
- Restricted the insertable cover image to the right side so it cannot hide the title panel.
- Removed inherited selective status fills from the blank table.
- Retained v1 geometry assets and builder separately for compatibility.

新增中英文空白模板与真正的 POTX 文件；每份有 14 种命名版式。
新增单栏、双栏、独立总结决策与最终致谢；中文覆盖技能、入门说明、提示及备注。
背景结构放在版式中，空段落保留格式；封面图片区不会遮盖左侧标题。
空白表不保留示例数据的状态强调。v1 蓝本和构建器继续保留供兼容使用。
