# Template workflow — v2 / 模板工作流程

## Fixed structure, empty content / 固定结构，正文留空

The blank PPTX and POTX versions share the same 14 layouts. Each layout contains
native background cards, rules and connectors plus positioned placeholders. On the
prepared slides, text placeholders are empty but keep explicit default run properties.
The only visible text in the blank decks is the final thank-you title and invitation.

空白 PPTX 和 POTX 共享 14 种版式。背景卡片、分隔线及连接线位于版式中，
内容通过定位好的占位符填写。预制页中的空段落仍保留明确的字体设置。
空白版里仅最终致谢标题与交流邀请是实际可见文字。

## Recommended manual workflow / 手动编辑

Open the blank PPTX and save a copy. Use the labelled guide or its preview to choose
a layout. Duplicate the relevant prepared slide, fill placeholders and remove unused
slides. The custom layouts are also available from the layout gallery. For structural
changes, edit the matching custom layout rather than repeatedly realigning individual
cards. A “fixed layout” is not a password lock: the structure remains intentionally editable.

打开空白 PPTX 并另存副本。参照标注版或预览选版式，复制相应预制页，
填写占位符并删掉不用的页面。自定义版式也可从版式库选取。
需要改结构时，修改对应版式；“固定”不是密码锁定，而是避免日常填写时误移动。

Use PPTX for a working presentation and POTX for reusable template storage. Both
contain the same native geometry. Do not assume simply renaming a PPTX makes a POTX;
the supplied POTX packages declare the proper template content type.

PPTX 用于工作演示，POTX 用于存储可重复使用的模板。
随附 POTX 已声明正确的模板内容类型，并非只改扩展名。

## Exceptions worth knowing / 两个重要例外

**Evidence table:** slide 08 contains a native, five-column, ten-body-row styled table.
Duplicate that slide to preserve row fills, borders and cell defaults. A new slide
created from the table layout has a table placeholder; it does not automatically
inherit all formatting from the prepared table. Delete extra rows when unnecessary.
No selective evidence/status highlights are pre-applied to a blank table.

**表格：**第 08 页有五列、十行正文的原生样式表格。复制页面能保留行色、边框和单元格默认格式。
仅从版式新建时，得到的是表格占位符；它不会自动继承预制表格的所有单元格样式。
多余行应删除；空白表不提前指定某些行的证据或状态强调。

**Thank you:** slide 14 includes two real editable strings. Duplicate it for a ready-made
ending. Creating a fresh slide from that layout gives the prompts, which must be filled.
Optional presenter, team, contact, brand and date fields stay empty until supplied.

**致谢：**第 14 页已经包含两句可编辑的正式文案，复制后即可作为结尾。
从版式中新建则只有提示，仍需填写。汇报人、团队、联系方式、品牌和日期不自动虚构。

## Cover image / 封面图片

The template narrows the insertable picture zone to the exposed right side of the
original full-width band. This is a v2 usability adaptation: a slide-level picture
would otherwise sit above and obscure the layout's white title panel. The full-width
pale band and left white panel remain fixed. No cover image is supplied.

v2 把图片插入区限制在原整幅图片带的右侧可见区，避免页面级图片盖住版式中的白色标题面板。
浅色整幅横带和左侧白色面板仍保留；模板不附带示例图片。

## Branding and numbering / 品牌与页码

Blank content means the footer and page-number fields are empty too. Fill these in
for the final deck and check after reordering. They are not automatic slide-number
fields. A user-supplied logo can be added as a genuine master graphic when it should
repeat; changing a placeholder's prompt is not the same as filling it on every slide.

空白模式同样清空页脚与页码；成稿时填写，调整顺序后再核对。
页码字段不是自动计数器。需要每页重复标志时，可把用户提供的标志设为真正的母版图形；
修改占位提示不等于已经填写每页的实际内容。

## Chinese / 中文

Use the Chinese templates so prompts, layout names, notes and closing copy are localized.
CJK text is explicitly assigned Noto Sans CJK SC. No fonts are embedded or distributed.
Use Microsoft YaHei or PingFang SC as consistent alternatives when necessary, then render.
For two-language deliverables, create separate files with matched layout numbers; keep
facts and identifiers identical. Do not force full translations into one text box.

中文文件已本地化提示、版式名、备注与致谢。字体明确设为 Noto Sans CJK SC，
但不嵌入或分发字体。必要时统一替换为微软雅黑或苹方简体，再重新渲染。
双语交付时建议分别制作两份文件，版式编号对应，事实和标识符一致，不挤在同一文本框。

## AI generation / AI 制作

Attach the main skill in the working language, the relevant blank PPTX, and the new
content. Specify whether to populate a presentation, restyle an existing one, or
produce more blank templates. The blank file is the geometry reference; the labelled
guide is a field map, not a source of business claims. Use only supplied or authorized
research. Render after populating, because empty-template checks do not prove future text fit.

提供对应语言技能、空白 PPTX 和新内容，并明确是生成成稿、重排现有稿，还是继续做空白模板。
空白文件负责几何结构，标注版负责解释字段，二者都不是业务事实来源。
填写后必须重新渲染；空白模板通过检查，不代表后续长文也一定放得下。
