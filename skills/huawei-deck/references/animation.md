# animation.md — 动画机制（build / layer / SMIL）

模板第 14–18 页（`动画·build逐步` / `动画·layer切换` / `动画·混合链` / `动画·SMIL运动` / `动画·多组切换`）是这套机制的**活教材**：页面正文就在讲解写法，放映着过一遍比读十遍文档都快。本文给出完整规则。

## 0. 总原则

- **所有动画都靠讲者手动推进**（点击空白 / 空格 / 方向键），**绝不自动循环播放**——动画的目的是控制讲课节奏，不是炫技。SMIL 装饰动效是唯一例外（循环但不占节拍、不抢注意力）。
- **不写任何操作提示文字**。「点击查看」「点击切换」「点击下方流程」之类一律不写——讲者知道怎么推进，听众不需要知道机制。真实功能控件的简短标签（如「复制链接」「新窗口打开」）不算操作提示，可以写；模板 03 章动画机制页正文里的「点击」是教学主题本身，同样豁免——别把它们当成可抄的文案范例。

## 1. 进入放映与键位

deck 打开时默认**滚动模式**（鼠标滚轮浏览全部页）。**右上角玻璃工具条**有两枚图标钮：**显示器图标 = 放映模式**（点击切入，同时自动尝试进入浏览器全屏）、上下箭头图标 = 滚动模式。以下键位在放映模式下生效：

| 操作 | 效果 |
|---|---|
| `→` / `PageDown` / 空格 / 点击页面空白 | 前进一拍（当前页拍完则翻下一页） |
| `←` / `PageUp` | 回退一拍（清掉已显示状态；本页回完则翻回上一页） |
| `F` | 切换浏览器全屏（任一模式可用） |
| `Esc` | 关闭已打开的缩略图侧栏 / 笔记面板（退出全屏是浏览器原生 Esc 行为） |
| 刷新页面 | 自动回到上次所在页（localStorage 记忆） |

点击推进只在放映模式生效，且点在按钮 / 链接 / iframe 等交互元素上时交给元素自己处理、不推进节拍。进页时点击计数 `level = 0`，只显示没挂动画的元素；每前进一拍 `level + 1`。

## 2. 机制一：build 逐步揭示

```html
<div class="build" data-step="0">第 1 拍出现</div>
<div class="build" data-step="1">第 2 拍出现</div>
<div class="build" data-step="1">同拍齐现（同一 data-step 的多个元素一起出）</div>
```

- 规则：放映态下 `.build` 默认隐藏（`opacity:0`），当前 `level > data-step` 时引擎给它 `data-shown` → 显示。`data-step="0"` 即第 1 次点击出现。
- **初始就该显示、不参与动画的元素不要加 `class="build"`。**
- `data-reveal="#id"` 可让某 build 元素显现时联动点亮另一个元素。
- 活例：模板第 14 页；第 9 页（密集多栏）演示「一拍点亮一组」。

## 3. 机制二：layer 层切换

一个区域多个面板互斥切换（tab / 方案 / 阶段视图）：

```html
<!-- 按钮：同 key 同组配对面板；首个 data-active 且不写 data-step（=默认层） -->
<div class="layerbtn" data-layer-btn="a" data-layer-group="G" data-active="">标签A</div>
<div class="layerbtn" data-layer-btn="b" data-layer-group="G" data-step="0">标签B</div>
<div class="layerbtn" data-layer-btn="c" data-layer-group="G" data-step="1">标签C</div>
<!-- 面板：与按钮同 key 同组；首个 data-active -->
<div class="layerpanel" data-layer-panel="a" data-layer-group="G" data-active="">面板A</div>
<div class="layerpanel" data-layer-panel="b" data-layer-group="G">面板B</div>
<div class="layerpanel" data-layer-panel="c" data-layer-group="G">面板C</div>
```

- `.layerbtn` / `.layerpanel` / `[data-active]` 的样式模板 CSS 已内置（红底白字高亮、面板 `display:none` ↔ `block`）。
- 点按钮直接跳到该层；**给按钮加 `data-step` 才能被方向键推进**。
- **引擎规则**：组内当前 active = `data-step < level` 的按钮中 **data-step 最大者**；没有满足者就回到**组内第一个按钮**（默认层）。所以首个按钮不写 data-step，其余按 0,1,2… 递增。
- 同组按钮 / 面板靠 `data-layer-group` 隔离，跨组互不干扰。**一页可以放多个组**：按钮挂 data-step 的组并入 build 点击线，全部不挂的组则完全靠手点（第 18 页更进一步演示了「build 走完后由某组接管点击」——那是该页运行时按 data-label 定制的逻辑，复制需同步改运行时判断，见 `template-pages.md` 第 18 页条目）。
- 活例：模板第 15 页（4 标签一组）、第 18 页（一页两组）。

## 4. 机制三：SMIL 连续运动

```html
<circle r="11" fill="#b5333b" cx="110" cy="92">
  <animate attributeName="cx" dur="3.4s" repeatCount="indefinite" values="110;400;110"></animate>
</circle>
```

- 写在 SVG 元素内部的 `<animate>` / `<animateTransform>` / `<animateMotion>`，`repeatCount="indefinite"`。
- 随当前页激活自动播放，离页被 `pauseAnimations()` 冻结——**不占节拍、不参与点击计数**，适合数据流、光带扫过这类持续示意。
- 在脚本里读动画中的值要用 `el.cx.animVal.value`；`getAttribute` 拿到的是基值。
- 活例：模板第 17 页（21 个 animate）、第 2 页议程页的靶心装饰。

## 5. 三条铁律

1. **版块的「外层背景框」也要挂 build**，不能只给框内内容挂——否则进页时空灰框先露出来，节拍就穿帮了（对照模板第 8 页：整行连框一起出现）。
2. **切勿用 `:has()` 控制 opacity**。本运行时里 opacity 级联有怪异表现（已踩坑）；要隐藏 / 显示容器就用 build 机制或 `visibility`。
3. **SVG 元素既是 `.build` 又带 `transform="rotate(…)"` 时，把 transform 移到非 build 的外层 `<g>` 上**。放映态 CSS `.build[data-shown]{transform:none}` 会清掉元素自身的 transform，导致放映模式错位而滚动模式正常。

## 6. 共享 level 与混合链

同一页的 build 和 layer **共享同一个 level 计数**，可以串成一条点击线：layer 按钮吃掉前几拍（整版切换），某个面板内部的 build 用更大的 data-step 接着逐条出现。总拍数 = 页内最大 `data-step` + 2（进页空场 1 拍 + 讲完翻页 1 拍）。活例：模板第 16 页（5 标签 + 面板内 3 个 build = 8 拍）。

## 7. 「先排拍后编号」方法

给一页设计动画时，别边写 HTML 边编号：

1. 先把这页的**讲稿节拍**列成一张表：第 1 拍讲什么、出现哪些元素；第 2 拍……直到讲完。一个「知识节拍」里相关的 bullet、连接箭头、caption 应归入**同一拍**（同一 data-step），别把一句话拆成三次点击。
2. 再把表翻译成编号：每拍一个 data-step 值，从 0 开始连续递增；layer 按钮先占位，面板内 build 接在其后。
3. 检查：进页空场（level=0）该显示什么？没挂 build 的元素就是空场内容，确认它们确实该提前可见。

## 8. 用 steps.mjs 验证节拍

改完动画不要凭感觉，在 skill 根目录跑逐拍截图（模拟放映引擎，规则与运行时一致）：

```bash
node scripts/verify/steps.mjs my-deck.html 动画·混合链 /tmp/steps-out
```

- 输出 `step-00.jpg`、`step-01.jpg`……每拍一张，并在终端**逐拍打印新出现的元素摘要**——对着讲稿核对每拍内容是否如设计。
- 页面无动画时打印提示后正常退出（exit 0）；label 不存在时列出全部可用 label（exit 1）。
- 拍数对不上时，通常是 data-step 编号跳号 / 重复，或该挂 build 的元素漏挂。

逐页动画拍数清单见 `template-pages.md` 开头的总表。
