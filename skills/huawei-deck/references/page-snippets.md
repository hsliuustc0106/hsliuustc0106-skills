# page-snippets.md — 可直接粘贴的页面骨架与构件

所有片段与 `assets/template-deck.html` 的实页写法一致，每段都标注了「模板第 N 页有活例」（页序与 data-label 对照见 `template-pages.md`）。**配图相关构件**（类型化占位块、图卡片、自绘流程图节点 / 箭头 / 泳道、分组表格）在 `artwork.md`，此处不重复。**整页复用优先直接复制模板对应页**（保占位说明与节拍编排）；本文的骨架用于从零拼一页或往现有页里加构件。

每页在 deck 里的**外壳**固定是：

```html
<div class="slide-fit" data-idx="N"><div class="slide-canvas">
  <section data-label="页名" style="..."> …页面内容… </section>
</div></div>
```

`data-idx` 必须是**数字**（装饰性、非唯一，导航按 DOM 顺序）；`data-label` 是页标识，verify 脚本与 edit-bundle 都用它定位——**尽量别起同名页**（工具遇到同名只处理第一个）。下面的片段除注明外只给 `<section>…</section>` 部分。插入新页用 `edit-bundle.py` 的 `insert_page`（见 `editing-guide.md`），别手拼。

---

## 1. 内容页骨架（最常用；活例：第 5–10 页）

```html
<section data-label="页名" style="width:100%; height:100%; padding:56px 90px; display:flex; flex-direction:column; background:#fff; font-family:'Noto Sans SC',sans-serif; overflow:hidden; position:relative;">
  <div style="font-family:'JetBrains Mono',monospace; font-size:18px; letter-spacing:.2em; color:#b5333b; margin-bottom:10px;">1.3 · 小节名 / ENGLISH</div>
  <h3 style="margin:0 0 8px; font-weight:600; font-size:46px; letter-spacing:-.02em; color:#1a1a1c;">大标题</h3>
  <p style="margin:0 0 22px; max-width:1320px; font-size:21px; line-height:1.55; color:#585860;">一行导语，<b style="color:#1565c0;">点睛的结论用蓝色加粗</b>。</p>
  <div style="flex:1; min-height:0;">
    <!-- 主体：卡片 / 两栏 / 网格 / 图。flex:1 + min-height:0 让它吃满并能收缩 -->
  </div>
</section>
```

新写的内容页建议在 `#fff` / `#fafafa` 间交替背景，以区分相邻页（模板页型画廊本身未严格交替）；密页可把 h3 调 40–42px、上下 padding 收到 44–48px。正文散文最小 21px（见 `design-system.md` 第 3 节）。

## 2. 左图右文两栏（活例：第 6 页）

```html
<div style="display:flex; gap:34px; align-items:center; height:100%;">
  <div style="flex:0 0 auto; max-width:60%; min-width:0; height:100%; display:flex; align-items:center; justify-content:center;">
    <img src="嵌入图的uid" alt="说明" style="height:100%; width:auto; max-width:100%; object-fit:contain; display:block; border:1px solid #ececec; border-radius:10px;">
  </div>
  <div style="flex:1 1 auto; min-width:0; display:flex; flex-direction:column; gap:12px;">
    <div style="font-size:24px; font-weight:600; color:#1a1a1c;">小标题</div>
    <div style="font-size:21px; color:#585860; line-height:1.6;">正文…</div>
  </div>
</div>
```

要点：图用 `height:100%; width:auto`（不是 `max-*`，否则小图不放大、四周留白）；外层 `flex:0 0 auto` 让框紧贴图。`src` 填 `embed_image` 返回的 uid（见 `editing-guide.md` 第 3.4 节）。模板里的虚线「图 · 占位」框就是留给这类真图的坑位。

## 3. build 逐步揭示（活例：第 14 页）

```html
<div class="build" data-step="0" style="…">第 1 拍出现</div>
<div class="build" data-step="1" style="…">第 2 拍出现</div>
<div class="build" data-step="2" data-reveal="#other" style="…">第 3 拍出现，并联动点亮 #other</div>
```

初始就显示的元素**不要加** `class="build"`；同一 data-step 的多个元素同拍齐现。规则与铁律见 `animation.md`。

## 4. layer 层切换（活例：第 15 页）

```html
<!-- 按钮区：首个 data-active 且不写 data-step；要方向键推进的按钮加 data-step -->
<div style="display:flex; gap:14px; margin-bottom:18px;">
  <div class="layerbtn" data-layer-btn="a" data-layer-group="G" data-active="" style="flex:1; text-align:center;">
    <div style="font-family:'JetBrains Mono',monospace; font-size:21px; font-weight:600;">标签A</div>
    <div style="font-size:18px; margin-top:4px; opacity:.8;">副题</div>
  </div>
  <div class="layerbtn" data-layer-btn="b" data-layer-group="G" data-step="0" style="flex:1; text-align:center;">
    <div style="font-family:'JetBrains Mono',monospace; font-size:21px; font-weight:600;">标签B</div>
    <div style="font-size:18px; margin-top:4px; opacity:.8;">副题</div>
  </div>
</div>
<!-- 面板区：与按钮同 key 同组，首个 data-active -->
<div style="flex:1; min-height:0;">
  <div class="layerpanel" data-layer-panel="a" data-layer-group="G" data-active="" style="height:100%;">…面板A…</div>
  <div class="layerpanel" data-layer-panel="b" data-layer-group="G" style="height:100%;">…面板B…</div>
</div>
```

`.layerbtn` / `.layerpanel` / `[data-active]`（红底白字高亮）的 CSS 模板已内置，无需自己写。面板内再嵌 build（data-step 接在按钮之后）即成混合链——活例第 16 页。

## 5. SMIL 连续运动（活例：第 17 页；装饰用法见第 2 页议程）

```html
<svg viewBox="0 0 760 380" style="height:100%; width:auto;">
  <path d="M90,82 C220,120 322,300 400,318 C478,300 580,120 700,82" fill="none" stroke="#b8b8c0" stroke-width="3.5"></path>
  <circle r="11" fill="#b5333b" stroke="#fff" stroke-width="3" cx="110" cy="92">
    <animate attributeName="cx" dur="3.4s" repeatCount="indefinite" calcMode="discrete" values="110;245;360;400;110"></animate>
    <animate attributeName="cy" dur="3.4s" repeatCount="indefinite" calcMode="discrete" values="92;225;308;318;92"></animate>
  </circle>
</svg>
```

随页激活自动播放、离页冻结、不占节拍。⚠ SVG 元素若同时是 `.build` 且带 `transform="rotate()"`，把 rotate 移到外层非 build 的 `<g>` 上（`animation.md` 铁律 3）。

## 6. 矩阵网格（讲矩阵 / 权重变换；活例：第 16 页）

用 `edit-bundle.py` 自带的 Python 助手生成，红色高亮标改动格：

```python
# eb 为已加载的 edit-bundle 模块（加载方式见 editing-guide.md 第 3.1 节）
html = eb.grid(rows=[['1','2','..'], ['..','0','4']], red={(0, 1)}, cell=30, fs=15)
```

`rows` 是二维列表，空串 = 空格子，`'..'` = 省略号；矩阵尽量用非方阵（d×k）更真实。格内数字是图元，15px 不受散文地板约束。

## 7. 嵌入网页 iframe + 复制链接（活例：第 13 页）

```html
<iframe src="https://example.com/" title="说明" loading="lazy"
  style="flex:1; min-height:0; width:100%; border:1px solid #e7e7e7; border-radius:14px; background:#fff;" allow="fullscreen"></iframe>
<button class="copylink" type="button" style="cursor:pointer; border:none; background:#b5333b; color:#fff; font-family:'Noto Sans SC',sans-serif; font-size:14px; font-weight:600; border-radius:8px; padding:9px 18px;">复制链接</button>
```

- 保留 `loading="lazy"`；外站可能拒绝被 iframe（X-Frame-Options 页面留白），复制链接按钮是兜底。
- `class="copylink"` 的复制逻辑模板运行时已用事件委托内置，**直接复用即可**；千万别写内联 `onclick`（会触发 React #231，见 `editing-guide.md` 踩坑表）。
- 视频不用 iframe：页面上放 `<a href="https://www.bilibili.com/video/BV…">` 普通链接，运行时委托会自动弹内嵌播放器（活例：第 5 页视频卡换成 bilibili 链接即可）。

## 8. 深色页构件：强调框 / 思考框（活例：第 18 页）

```html
<!-- 深色页整页：background:#15171c；文字 #fff；红 / 金强调 -->
<!-- 行内强调框（米色，用于浅色页）： -->
<div style="background:#fbf4ee; border-left:5px solid #b5333b; border-radius:10px; padding:16px 22px; font-size:21px; color:#1a1a1c;">敲黑板：要点…</div>
<!-- 思考问题框（深底，浅深两种页都可用）： -->
<div style="background:#15171c; border-radius:12px; padding:16px 26px; display:flex; align-items:center; gap:16px;">
  <span style="font-family:'JetBrains Mono',monospace; font-size:15px; letter-spacing:.18em; color:#ffe08a;">思考一下</span>
  <span style="font-size:21px; font-weight:600; color:#fff;">提出一个问题，不给答案。</span>
</div>
```

## 9. 对比条（讲资源节省 / 差距；可拼进任意内容页）

```html
<div style="display:flex; align-items:center; gap:14px; margin-bottom:9px;">
  <div style="flex:none; width:120px; font-size:15px; color:#585860;">方案A</div>
  <div style="flex:1; height:20px; background:#eeeef0; border-radius:10px; overflow:hidden;"><div style="width:100%; height:100%; background:#b5333b; border-radius:10px;"></div></div>
  <div style="flex:none; width:430px; font-size:15px; color:#585860;">右侧说明…</div>
</div>
<!-- 第二行把内条 width 改成 2% 并换 #566472，形成「满 vs 极短」的强烈对比 -->
```

## 10. 章扉页骨架（活例：第 3 页）

```html
<section data-label="章扉页2" style="width:100%; height:100%; padding:108px 130px; display:flex; flex-direction:column; justify-content:center; background:#f5f5f6; font-family:'Noto Sans SC',sans-serif; overflow:hidden; position:relative;">
  <div style="position:absolute; left:130px; top:108px; font-family:'JetBrains Mono',monospace; font-size:180px; font-weight:700; line-height:1; color:#b5333b; opacity:.09;">02</div>
  <div style="font-family:'JetBrains Mono',monospace; font-size:21px; letter-spacing:.24em; color:#b5333b; position:relative;">SECTION 02 · XX MIN</div>
  <h2 style="margin:30px 0 0; font-weight:600; font-size:100px; line-height:.98; letter-spacing:-.03em; color:#1a1a1c; position:relative;">章名：一行点题</h2>
  <p style="margin:36px 0 0; max-width:1040px; font-size:27px; line-height:1.7; color:#585860; position:relative;">章副题：两三句写清本章叙事线。</p>
  <div style="margin:48px 0 0; display:flex; gap:12px; flex-wrap:wrap; position:relative;">
    <span style="padding:10px 20px; border:1px solid #d9d9dd; border-radius:999px; background:#fff; font-size:18px; color:#585860;">关键词一</span>
  </div>
</section>
```

⚠ **背景画不是写在 section 里的**：金色背景由 `<style id="tpl-bg-950">` 中 `section[data-label="章扉页"]` 的规则挂上（`#f5f5f6` 只是兜底色）。用新 label（如「章扉页2」）时要在该样式块的对应选择器后追加 `, section[data-label="章扉页2"]`——封面 / 目录 / 结语页同理。

## 11. 问题页骨架（活例：第 4 页）

```html
<section data-label="问题页2" style="width:100%; height:100%; padding:108px 130px; display:flex; flex-direction:column; justify-content:center; background:#f5f5f6; font-family:'Noto Sans SC',sans-serif; overflow:hidden; position:relative;">
  <div style="position:absolute; right:70px; top:30px; font-family:'JetBrains Mono',monospace; font-size:300px; font-weight:700; line-height:1; color:#b5333b; opacity:.06;">Q2</div>
  <div style="font-family:'JetBrains Mono',monospace; font-size:21px; letter-spacing:.24em; color:#b5333b; position:relative;">问题 二 · QUESTION 2</div>
  <h2 style="margin:34px 0 0; font-weight:600; font-size:72px; line-height:1.15; letter-spacing:-.02em; color:#1a1a1c; max-width:1400px; position:relative;">一个<span style="color:#b5333b;">具体可讨论</span>的真问题？</h2>
</section>
```

右下角人像由 `tpl-bg-950` 中 `section[data-label="问题页"]::after` 挂上——新 label 需在该规则追加选择器。提问不给答案。

## 12. 议程行（活例：第 2 页）

议程页整页建议直接复制模板第 2 页改文案；往里加一行目标用这个行块：

```html
<div style="display:flex; gap:24px; align-items:center; padding:16px 0; border-top:1px solid #ededed;">
  <svg width="34" height="34" viewBox="0 0 34 34" style="flex:none;"><circle cx="17" cy="17" r="17" fill="#fbeaec"></circle><path d="M10 17.5 L15 22.5 L24 11.5" fill="none" stroke="#b5333b" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"></path></svg>
  <div style="flex:1; font-size:21px; line-height:1.5; color:#2a2a30;">目标句：可检验的动词开头，一句话。</div>
  <div style="flex:none; text-align:right; min-width:140px;"><div style="font-size:21px; color:#6a6a72; line-height:1.3;">章名</div><div style="font-family:'JetBrains Mono',monospace; font-size:21px; color:#b5333b;">CH.0X · XX min</div></div>
</div>
```

## 13. 研讨议题条（活例：第 21 页）

研讨页整页建议复制模板第 21 页；往议题卡里加一条：

```html
<div style="display:flex; gap:13px; align-items:flex-start; padding:12px 0; border-bottom:1px solid #ececec;">
  <span style="flex:none; font-family:'JetBrains Mono',monospace; font-size:19px; font-weight:700; color:#fff; background:#566472; border-radius:6px; padding:3px 10px; margin-top:2px;">⑤</span>
  <div style="font-size:21px; line-height:1.55; color:#3a3a40;"><b style="color:#1a1a1c;">议题五</b>　开放式问题，正文加粗<b>关键词锚点</b>？</div>
</div>
```

末条去掉 `border-bottom`。右下角人像同问题页，靠 `tpl-bg-950` 的 `::after` 规则。

## 14. 金框黑板题卡（活例：第 19、20 页）

黑板底图由 `tpl-bg-950` 中 `section[data-label="黑板·题卡A"], section[data-label="黑板·金框题卡"]` 的规则挂上（`url(底图) center/100% 100%` 拉满 + 强制 `padding:74px 124px`）——新增黑板页同样要给新 label 追加选择器。单张题卡（金字风格，两拍：题干一拍、答案一拍）：

```html
<div class="build" data-step="0" style="background:rgba(255,255,255,.05); border:1px solid rgba(244,200,74,.18); border-radius:12px; padding:11px 18px; display:flex; flex-direction:column; gap:5px;">
  <div style="display:flex; align-items:center; gap:9px;"><span style="font-family:'JetBrains Mono',monospace; font-size:21px; font-weight:700; color:#f4c84a;">01</span><span style="font-family:'JetBrains Mono',monospace; font-size:21px; color:#f4c84a; border:1px solid rgba(244,200,74,.5); border-radius:5px; padding:1px 7px;">选择</span></div>
  <div style="font-size:21px; color:#fff; font-weight:500; margin-bottom:4px;">题干：问法明确、只有一个正确项？</div>
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px 14px; font-size:21px; color:#e8e8ec;"><span>A. 选项一</span><span>B. 选项二</span><span>C. 选项三</span><span>D. 选项四</span></div>
  <div class="build" data-step="1" style="font-size:21px; color:#f4c84a; font-weight:600;">✅ 答案：B · 一句话解析</div>
</div>
```

填空题干里的挖空写法：`<span style="border-bottom:1.5px solid rgba(255,255,255,.5); padding:0 16px;">　</span>`。后续题卡的 data-step 按 2,3 / 4,5 / … 顺延。换黑板底图用 `apply_bg.py --target board`。
