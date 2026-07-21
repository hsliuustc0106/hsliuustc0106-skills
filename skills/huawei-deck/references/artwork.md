# artwork.md — 配图工作流：初版占位标注 → 终版抽图 / 自绘图 / 制表落地

**总原则：字不如表，表不如图。** 凡是讲方法论、解决方案、原理逻辑的页面，必须有图或表承担主表达，文字只做补充。分工：**素材原图给证据**（实验曲线、结果柱状图、官方方法图），**自绘图讲机制**（流程、架构、分支决策，中文标注、品牌配色），**表格管对比与枚举**（多方案对照、速查清单）。

配图分两段做，**不要在初版抠图**：

| 阶段 | 动作 |
|---|---|
| 初版 | 每个配图位放一个**类型化占位块**（见第 1 节），写清类型 + 来源 + 内容规格；逐页规划表的「配图」列同步登记 |
| 终版 | `grep data-todo` 找出全部占位，逐个落地（抽原图 / 自绘 / 制表），清零后跑 verify |

## 1. 初版：类型化占位块

占位块统一带 `data-todo="fig"` 标记（终版用它检索清零），类型四选一：**【原图】【自绘·流程】【自绘·架构】【表格】**。

```html
<div data-todo="fig" style="flex:1; min-height:0; border:2px dashed #d9a0a4; border-radius:12px; background:#fdf7f7; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px; padding:18px;">
  <span style="font-family:'JetBrains Mono',monospace; font-size:14px; color:#b5333b;">【原图】Let&#39;s Verify · Fig 3</span>
  <span style="font-size:15px; color:#8a8a92;">best-of-N 曲线：PRM / ORM / 投票三线对比 · 约 4:3 横图</span>
</div>
```

第一行写「类型 + 来源」（原图注明 PDF 与 Fig 编号；自绘注明要画什么机制；表格注明数据来源），第二行写「内容一句 + 长宽比」。**占位不写清规格，终版落地时就要重读全部素材**——规格是给未来的自己（或另一个会话）看的。

逐页规划表加一列「配图」：

> 页序 | data-label | 页型 | 核心观点 | 排版逻辑 | **配图（类型 + 一句规格）** | 拍数

## 2. 终版落地 A：从素材 PDF 抽原图（PyMuPDF）

依赖 `pymupdf`（`python3 -m pip install pymupdf`）。若素材是 pptx，先 `soffice --headless --convert-to pdf` 转成 PDF 再走本节流程（内嵌媒体也可直接用 `zipfile` 解包 `ppt/media/` 拿原图）；PDF 的合并 / 拆分 / 文本表格提取 / 表单等进阶操作，按需参考单独安装的 PDF skill。三步循环，每张图都要**目检**：

```python
import fitz
doc = fitz.open('论文.pdf')
# ① 整页渲染找图：像素坐标 ÷ zoom = PDF pt 坐标
doc[1].get_pixmap(matrix=fitz.Matrix(2, 2)).save('/tmp/page2.png')   # 用 Read 看图，估算 bbox
# ② 高清裁切（zoom 3）
doc[1].get_pixmap(matrix=fitz.Matrix(3, 3), clip=fitz.Rect(40, 120, 560, 430)).save('fig.png')
# ③ 再用 Read 目检裁切结果，不满意调 bbox 重裁
```

- 裁切范围：含图形与图内标签，**不含论文自带的「Figure N: …」图注**——中文图注自己写，并标明「论文 Fig N」出处。
- 素材多于 3 篇时**并行分派 agent**（一篇/一组一个 agent），每个 agent 给足：PDF 绝对路径、目标图描述（Fig 编号 + 内容特征）、输出文件名、上述三步方法，要求最终回复一行 JSON（file / figure / 内容一句 / 宽x高）。
- 抽出的 PNG 一般每张几十至几百 KB，无需压缩；超过 1MB 再考虑降采样。

嵌入 deck（经 edit-bundle，见 `editing-guide.md` 第 3.4 节）：

```python
uid = eb.embed_image(lines, 'fig.png', mime='image/png', prefix='fig')
```

图卡片统一样式（图 + 中文图注）：

```html
<div style="flex:1; min-width:0; min-height:0; background:#fff; border:1px solid #e7e7e7; border-radius:14px; padding:12px 16px; display:flex; flex-direction:column; gap:7px; align-items:center; justify-content:center;">
  <img src="嵌入返回的uid" style="width:100%; object-fit:contain; flex:1; min-height:0;">
  <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#9a9aa2; text-align:center;">论文 Fig 3 · 一句话说明图里是什么、该看哪条线</div>
</div>
```

## 3. 终版落地 B：自绘流程图 / 架构图（div 构件，不用画图工具）

自绘图用 div + flex 拼装即可，品牌三色（红 `#b5333b` 只给关键节点 / 瓶颈，其余中性灰边框），中文标注。基础构件：

```html
<!-- 节点（hot=true 时红边红字米底，标关键/瓶颈节点） -->
<div style="flex:none; min-width:0; background:#fff; border:1.5px solid #d9d9dd; border-radius:10px; padding:9px 14px; text-align:center;">
  <div style="font-size:17px; font-weight:600; color:#1a1a1c;">节点名</div>
  <div style="font-size:14px; color:#585860; margin-top:2px;">补充说明一行（可省）</div>
</div>
<!-- 横箭头 / 竖箭头（放在 flex 行/列中间） -->
<div style="flex:none; align-self:center; font-family:'JetBrains Mono',monospace; font-size:22px; color:#c9c9cf;">→</div>
<div style="flex:none; text-align:center; font-family:'JetBrains Mono',monospace; font-size:20px; color:#c9c9cf; line-height:1;">↓</div>
```

三种常用拓扑（外层都套一张白卡 + mono 小标题）：

- **直线流程**：flex 行/列里「节点 → 节点 → 节点」，瓶颈节点标红——适合管线、漏斗（「红利在哪一步漏掉」）。
- **分支流程**：行1「输入 → 判定节点」，↓，行2 两个并排分支节点，↓，行3 汇合节点——适合「按条件走不同路」的决策逻辑。
- **多路对照（泳道）**：头部共享节点行，↓，每路一行「↳ + 方法节点 → 结果大数字」，胜者行标红——适合同源多方案对比（评测流程）。

**选型判别**：机制/流程/决策 → 自绘（读者要按中文标注顺着走）；实验证据/复杂官方架构 → 抽原图（重画会失真且费时）；两者可同页共存——自绘图讲「怎么转」，原图证明「真的行」。

## 4. 终版落地 C：表格

对比、枚举、速查用表格。分组表格式（分组徽标列 rowspan + mono 数字列）：

```html
<table style="width:100%; border-collapse:collapse;">
  <thead><tr><th style="text-align:left; padding:8px 12px; font-family:'JetBrains Mono',monospace; font-size:13px; letter-spacing:.12em; color:#8a8a92; border-bottom:2px solid #e0e0e4;">列名</th></tr></thead>
  <tbody><tr>
    <td rowspan="3" style="padding:8px 12px; border-bottom:1.5px solid #e0e0e4; vertical-align:middle;"><span style="font-family:'JetBrains Mono',monospace; font-size:14px; font-weight:700; color:#fff; background:#b5333b; border-radius:6px; padding:3px 10px; white-space:nowrap;">分组</span></td>
    <td style="padding:8px 12px; border-bottom:1px solid #f0f0f2; font-size:16px; color:#585860;">内容列</td>
    <td style="padding:8px 12px; border-bottom:1px solid #f0f0f2; font-family:'JetBrains Mono',monospace; font-size:15px; color:#b5333b; white-space:nowrap;">关键数字</td>
  </tr></tbody>
</table>
```

表格单元格文字是**图元**，15–17px 即可、不受 21px 散文地板约束（判别法见 `design-system.md` 第 3 节）。行数多的总表先估高度：行高约 44px，超过 ~18 行考虑拆列或拆页。

## 5. 落地后的验证与踩坑

- 每落地一批：`grep -c 'data-todo' `（对 `eb.get_template` 的字符串数）应递减到 **0**，然后跑 `measure_overflow --all` + 改动页 `shot` 截图目检（图不糊、不裁、图注完整）。
- **缺字形坑**：Noto Sans SC 没有下标字符（₁₂₅ 等，会渲成方框）——公式下标用 `<sub>`/`<sup>` 标签写。
- 图注必须写出处（「论文 Fig N」）；数字型结论优先进 stat 卡或表格，不要埋在图注里。
- 自绘图**去花花绿绿**：只用 红 + 灰蓝 + 中性灰，红只标关键节点（同 `design-system.md` 三色铁律）。

## 常见错误

| 错误 | 后果 / 纠正 |
|---|---|
| 初版直接抠图、画图 | 结构没定，精修全是沉没成本；初版只放类型化占位块 |
| 占位块只写「图 · 占位」不写规格 | 终版要重读全部素材才知道放什么；第一行类型+来源、第二行内容+比例 |
| 方法论页面全是文字卡 | 字不如表，表不如图——机制类内容自绘流程/架构图做主表达 |
| 裁图带上论文原图注 | 图注语言不统一且冗余；裁掉，自己写中文图注并标「论文 Fig N」 |
| 自绘图沿用素材原配色 | 花花绿绿破坏三色体系；节点重画为 红/灰蓝/中性灰 |
| 落地后不清点占位 | 漏图无声出货；`data-todo` 计数必须归零再交付 |
