# 参考演示风格 — v2 中文使用说明

本套文件基于用户提供的 `ai-application-innovation-20-pages.pptx`，
把原先的示例页扩展为**可直接填写的空白模板、自定义版式和中英文技能说明**。

## 先构建仓库版模板

本仓库采用 v2 源码分发，不将聊天下载包中的六份 PPTX/POTX 与位图预览作为
二进制文件提交。请先执行：

```bash
cd skills/reference-slide-style
python -m pip install -r requirements.txt
python scripts/build_templates.py
```

脚本可在全新检出目录运行，无需原始演示或预制的 `assets/starter-layouts.pptx`。
仓库版使用生成的版式标注 PPTX 选择版式，不依赖位图预览。专用 GitHub Actions
工作流会验证输出，并以 `reference-slide-style-templates` 构建产物发布六份
Office 文件。保留的 v2 验证记录针对最初下载包；后续构建仍须重新检查。

## 从哪里开始

日常制作，打开 **`templates/blank-layouts-zh-CN.pptx`**，另存工作副本，
复制需要的页面后填入真实内容。前 13 页没有可见文字；第 14 页仅预置
“谢谢聆听”“欢迎交流与提问”。占位符即使没有正文，也保留位置、字号、颜色和段落格式。

需要可重复使用的 PowerPoint 模板文件时，使用 **`templates/reference-style-zh-CN.potx`**。
它是正确声明模板类型的 OOXML 文件，不是只改了扩展名的 PPTX。
中文 PPTX 和 POTX 都包含 14 个命名的自定义版式。英文对应文件以 `-en` 结尾。

需要让 AI 按此风格制作时，同时提供 **`SKILL.zh-CN.md`、中文空白 PPTX 和新内容**。
英文技能为 `SKILL.md`，描述同一套设计系统。文件包不会自动安装技能，
也不会自动修改账户级偏好。

## 本次新增

新增真正留空的版式模板，不再要求先删除示例正文；新增单栏与双栏内容页；
把原参考稿的总结决策结构单列为一种版式；新增独立的中英文致谢页。
单栏、双栏和致谢是基于参考风格的新扩展，不是原文件已有的页面。

中文版本覆盖版式名称、占位提示、页面备注、致谢文案、技能与入门说明，
并显式设置中文字体。不会只翻译封面大标题。

## 文件入口

| 文件 | 用途 |
|---|---|
| `SKILL.zh-CN.md` | 中文技能说明，供未来生成或重排使用 |
| `templates/blank-layouts-zh-CN.pptx` | 14 页空白中文演示，可直接编辑 |
| `templates/reference-style-zh-CN.potx` | 中文 PowerPoint 模板，含 14 种自定义版式 |
| `templates/layout-guide-zh-CN.pptx` | 显示字段名称的版式标注版，不是空白成稿模板 |
| `templates/layout-index.json` | 中英文版式对照索引 |
| `references/validation.md` | 验证范围与兼容性限制 |
| `scripts/build_templates.py` | 重建新版 PPTX/POTX |
| `scripts/check_templates.py` | 检查新版空白／标注模板的结构 |

英文同类文件以 `-en` 结尾。旧版内容构建脚本和 JSON 蓝本保留；可选的
`assets/starter-layouts.pptx` 可重新生成，不能误当成本次新增的空白模板。

## 14 种版式

01 封面、02 目录、03 单栏内容、04 双栏内容、05 六卡总览、06 三栏比较、
07 流程与架构、08 证据表格、09 共享平台、10 三阶段流程、11 反馈闭环、
12 路线图与门槛、13 总结与决策、14 致谢。

这些是供选择的版式，不是必须照用的顺序或页数。

## 编辑时注意

卡片、强调色条和连接线放在自定义版式中，正常编辑时不会误移动；
文字在页面占位符中填写。确实需要改变结构时，修改对应版式。
品牌、来源与页码先留空，在正式演示中按实际信息填写。页码不是自动计数器。

**表格：**优先复制第 08 张预制页，保留五列表格的行色与边框。
从自定义版式直接新建时，只得到表格占位符，新插入表格可能需要重新设置格式。

**封面：**图片占位符位于右侧，防止遮盖左侧白色标题面板；
背后的整幅浅色带属于固定版式。未带入原参考稿的插图和标志。

**致谢：**优先复制第 14 张预制页，已包含两句正式致谢文字。
仅从版式新建时，显示的是填写提示；汇报人和联系方式仍需根据实际情况填写。

**中文字体：**已测试的中文字体为 Noto Sans CJK SC；没有安装时，
可统一替换为微软雅黑或苹方简体，并逐页检查换行。包内不分发字体文件。
参考文件中声明 Arial 不代表已经确认它原先实际使用的中文字体。

## 以后可直接使用的提示词

> 请使用附件中的 reference-slide-style v2 中文技能和空白 PowerPoint 模板，
> 为【受众】制作关于【主题】的【页数】页中文演示。只以我提供的材料作为事实依据。
> 根据内容选择预设版式，保留 16:9 白色画布、蓝色标题、浅色圆角卡片、紫色与青色强调，
> 以及统一页脚。文字、表格与图示保持可编辑。在正文末尾加入“谢谢聆听／欢迎交流与提问”致谢页。
> 不编造事实或来源。交付前渲染并逐页检查。

只需要空白模板时，可改为：

> 使用空白模板模式。保留确定的版式结构和可编辑占位符，正文、品牌、日期、来源和页码全部留空；
> 仅保留最终致谢页的通用文字。输出结构一致的中英文 PPTX 与 POTX 文件。

只重排已有文件时，明确要求保留原意、事实、限定条件、术语与页面顺序，不擅自增加或改写内容。

## 重建与验证

```bash
python -m pip install -r requirements.txt
python scripts/build_templates.py
python scripts/check_templates.py templates/blank-layouts-zh-CN.pptx templates/reference-style-zh-CN.potx
```

检查标注版时增加 `--guide`。脚本不负责渲染和事实核查；填入新内容后仍须逐页检查。
交付文件已经使用 LibreOffice 渲染，但没有单独在收件人电脑的 Microsoft PowerPoint 中测试。
