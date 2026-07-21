# editing-guide.md — 独立版结构、edit-bundle.py 用法与验证工作流

deck 是一个「独立版」单文件 HTML：React 运行时、字体、全部图片都内联在文件里，真离线可用。代价是**不能用编辑器直接改内容**——本文讲清结构、安全编辑方法、踩坑与验证。所有命令均在 skill 根目录（`huawei-deck/`）执行，示例均假设你已 `cp assets/template-deck.html my-deck.html`（**改前先备份**）。

## 1. 独立版结构：两行超长 JSON

文件里有两个关键 `<script>`，各自的**下一行**是一整行 JSON：

| 标记行 | 下一行内容 |
|---|---|
| `<script type="__bundler/manifest">` | 一行 JSON dict：`{uid: {mime, compressed, data(base64)}}`——全部图片 / 资源 |
| `<script type="__bundler/template">` | 一行 JSON **字符串**：整份 deck 的 HTML（含每页 `<section>`、导航数组、运行时脚本） |

改内容 = 解码 template 字符串 → 字符串手术 → 重编码回填。`scripts/edit-bundle.py` 封装了这一切。

## 2. 安全编码铁律

1. **改 template 必须经 `get_template` / `set_template` / `save`，绝不手拼、绝不用编辑器 / sed 直改那两行。** `set_template` 负责唯一正确的编码：`json.dumps(s, ensure_ascii=False).replace('</', '<\\u002F')`——只转义 `</`（防字符串里的 `</script>` 提前闭合文档），中文不转义、URL 里的普通 `/` 不动，并内置断言（回填串不含 `</`、不含换行、`json.loads` 后与原字符串相等）。直改几乎必然把整个文件弄坏。
2. **manifest 是一整行 JSON dict，手改容易截断**——嵌图用 `eb.embed_image`，换品牌图用 `scripts/apply_bg.py`（见 `branding.md`）。
3. 改结构（加 / 删 / 移页）必须**三处同步**：slide DOM、`nav[]` 数组、`chapters[].start`——`insert_page` / `delete_page` / `move_page` 已自动做完，别手动改其中一处。

## 3. edit-bundle.py 典型用法

### 3.1 加载（所有片段的公共开头）

```python
import importlib.util
spec = importlib.util.spec_from_file_location('eb', 'scripts/edit-bundle.py')
eb = importlib.util.module_from_spec(spec); spec.loader.exec_module(eb)

lines = eb.load('my-deck.html')     # 整个文件按行读入
s = eb.get_template(lines)          # 解码出 deck HTML 字符串
```

### 3.2 改文字 = section 切片手术

**改前先看目标文本**——先把该页 section 片段打出来（去掉标签更好读），确认要替换的占位文案原文一字不差，再做替换：

```python
import re
i = s.find('<section data-label="版式·流程条"'); j = s.find('</section>', i)
print(re.sub(r'<[^>]+>', ' ', s[i:j])[:1500])   # 去标签打印该页文本，核对占位原文
```

然后把手术范围收窄到目标页的 `<section>`，在片内替换，避免误伤其他页的同词：

```python
i = s.find('<section data-label="版式·流程条"')
j = s.find('</section>', i) + len('</section>')
blk = s[i:j]

OLD, NEW = '页面标题 = 一句话概括流程', '数据准备四步走'
assert blk.count(OLD) == 1, '目标文本应恰有 1 处，实际 %d' % blk.count(OLD)
s = s[:i] + blk.replace(OLD, NEW) + s[j:]

eb.set_template(lines, s)
eb.save('my-deck.html', lines)
eb.verify('my-deck.html')
```

替换前 `assert count == 1`（或预期处数）是习惯动作——0 处说明找错了，多处说明会误伤。

### 3.3 加 / 删 / 移页（自动三处同步）

```python
# 复制章扉页为第二章扉页，插到「问题页」之前
i = s.find('<section data-label="章扉页"')
st = s.rfind('<div class="slide-fit"', 0, i)
end = s.find('</div></div>', s.find('</section>', i)) + len('</div></div>')
new_block = s[st:end].replace('data-label="章扉页"', 'data-label="章扉页2"')
s = eb.insert_page(s, new_block, before_label='问题页', nav_code='章2', nav_label='章扉页2')

# 门面页型的背景由 <style id="tpl-bg-950"> 按 data-label 精确匹配，新 label 要补选择器：
OLD_SEL = 'section[data-label="章扉页"],'
assert s.count(OLD_SEL) == 1
s = s.replace(OLD_SEL, 'section[data-label="章扉页"], section[data-label="章扉页2"],')

# 删页 / 同章内移页
s = eb.delete_page(s, '版式·动手实验')                        # 按 data-label 删
s = eb.move_page(s, '版式·流程条', after_label='版式·对比两栏')  # 同章内移到某页之后

eb.set_template(lines, s); eb.save('my-deck.html', lines); eb.verify('my-deck.html')
```

`new_block` 必须是完整的 `<div class="slide-fit"...>…</div></div>` 块；`nav_code` 是导航条上显示的短码（模板里多为两字，如「章扉」「对比」），`nav_label` 必须与页面 data-label 完全一致（增删移页都靠它对上号）。

- **插入的章归属约定**：插到某章**首页之前** = 新页成为该章新首页（该章 start 不动）；插到章中 / 章尾页之前 = 新页归入该章，下一章起 start 全部 +1。
- **删除的对应规则**：删页后，被删页所在章**之后**各章 start 自动 −1（本章 start 不变）。
- ⚠ **`move_page` 只在同章内移动是安全的**（chapters 不需要变，它也不会去调整）；跨章移动后 `chapters.start` 不会自动修正，需按 3.5 节手工修。
- 插删页后都跑一下 `verify`，看打印出的 `chapters` start 是否符合预期。

### 3.4 嵌入图片

```python
uid = eb.embed_image(lines, '你的图.png', mime='image/png', prefix='img')  # 写入 manifest，返回 uid
s = s.replace('src="旧图uid或占位"', 'src="%s"' % uid)                     # template 里用 uid 引用
eb.set_template(lines, s); eb.save('my-deck.html', lines)
```

jpg 用 `mime='image/jpeg'`。大图先压缩（1MB 内为宜），deck 体积直接跟着涨。替换四类品牌图（背景画 / 黑板 / 人像 / logo）不用手写这些——`apply_bg.py` 全自动（含旧条目清理），见 `branding.md`。

### 3.5 结构验证与 chapters 手工修正

```bash
python3 scripts/edit-bundle.py my-deck.html
```

打印 slide-fit / section / nav 三者数量与章节起点，`nav` 编号不连续会直接 assert 失败——每次保存后都跑一下。

若 `chapters` 的 start 与预期不符（例如做了跨章 `move_page`），用 `bump_chapters` 助手手工修正后再验：

```python
s = eb.bump_chapters(s, +1, 13)   # 把 start > 13 的所有章起点 +1（delta 可为负）
eb.set_template(lines, s); eb.save('my-deck.html', lines); eb.verify('my-deck.html')
```

## 4. 同名 data-label 警告

`data-label` 是所有工具定位页面的唯一手段。deck 里出现同名 label 时：**verify 三件套会打印警告并只处理第一个**；而 **edit-bundle 的定位函数（insert/delete/move、切片手术的 `find`）同样只取第一个、且不打印任何警告**——插删改之前先确认目标 label 唯一（`s.count('<section data-label="某页"') == 1`）。复制页面务必改成新名字；万一已有同名页，`measure_overflow.mjs --all` 是唯一能把同名页各测各的模式（显示为 `label #2`）。

## 5. 踩坑表

| 症状 | 根因 / 修法 |
|---|---|
| 整页灰屏 / 加载死循环 | `data-idx` 必须是**数字**（如 `"45b"` 直接灰屏）。它是装饰性的，可重复，但必须是数字。 |
| 中文显示成细体、看不清 | 该元素只挂了 `JetBrains Mono`（无中文字形，回退细体）。中文一律 `'Noto Sans SC'`，要粗用 `font-weight:700`。 |
| 点按钮 / 链接报 React #231（onClick 是字符串） | 写了内联 `onclick="fn()"`——运行时会把它当 React 的 `onClick` 字符串。**别用内联 on\***，用事件委托：`document.addEventListener('click', e => { const t = e.target.closest('.你的class'); if (!t) return; /* 处理 */ }, true)`（capture + `stopPropagation`）。模板的复制链接、bilibili 播放器都是这么实现的，可直接复用。 |
| 改完后整个文件打不开 / JSON 报错 | 没走 `set_template` 的编码铁律（第 2 节），`</script>` 提前闭合或转义损坏。从备份恢复，重做并只经 edit-bundle。 |
| 加页后导航乱 / 某页掉出章节 | 三处同步没做全。用 `insert_page` / `delete_page` / `move_page`，并用 `verify` 检查 `nav` 连续、`chapters.start` 正确。手插 HTML 块时还要注意 `</div>` 配平。 |
| 改了章数后，目录页选中某章左侧空白 / 动画内容跑题 | 目录页左侧动画按章节索引取自 `const builders = [...]` 数组，且各动画文案是模板课程主题。增删章后同步 builders 数组并替换动画内文字，见 `template-pages.md` 目录页一节。 |

放映态动画的坑（`:has()`、SVG transform、外层框漏挂 build）见 `animation.md` 第 5 节。

## 6. 验证工作流（改完一批必做）

```bash
node scripts/verify/measure_overflow.mjs my-deck.html --all          # 1) 全页溢出检测
node scripts/verify/shot.mjs my-deck.html 版式·流程条 /tmp/p.jpg      # 2) 改过的页截图目检
node scripts/verify/steps.mjs my-deck.html 版式·流程条 /tmp/steps     # 3) 动过动画的页逐拍核对
```

- **退出码契约（三个脚本一致）**：`0` = 通过 / 成功；`1` = 检出问题（存在溢出 / label 不存在）；`2` = 工具或参数错误（浏览器起不来、参数缺失）。可以直接接进 CI / 脚本判断。
- `measure_overflow` 不传 label 等价 `--all`；报告分两层——section 级溢出（Y/X 像素，>0 即失败）和内层 `overflow:hidden` 裁切（只报告不判失败，逐条截图目检）。
- 已知基线：模板出厂时「版式·左图右文」页自带 3 处 nested clip（图占位框裁切自身的提示文字，+38px）——属预期表现，不是问题，换成真图后自然消失。
- 依赖：Node ≥ 18、本机安装 Google Chrome、playwright-core。**playwright-core 按三级顺序查找**：环境变量 `PLAYWRIGHT_CORE`（指向其 index.js）→ 裸 `import('playwright-core')`（在 skill 根目录 `npm i playwright-core` 即可满足）→ openclaw 全局安装的内置路径。都找不到时脚本会以退出码 2 报错并给出提示。
- 首次加载等待较长是正常的（脚本内置了等待 React mount 的 settle 时间）。

## 7. 导出 PPTX（html2pptx）

```bash
bash scripts/html2pptx/convert.sh my-deck.html            # 输出同名 my-deck.pptx
bash scripts/html2pptx/convert.sh my-deck.html 出货版.pptx  # 指定输出名
SCALE=2 QUALITY=92 bash scripts/html2pptx/convert.sh my-deck.html   # 清晰度 / 压缩（即默认值）
EMBED_HTML=1 bash scripts/html2pptx/convert.sh my-deck.html         # 第一页嵌原始 HTML（OLE，Windows PowerPoint 可双击打开；体积会明显增大）
```

- 原理：headless Chrome 逐页截图（自动隐藏导航条等 UI 外壳、`.build` 全显），python-pptx 组装成 16:9、每页一张满屏图。工具不解析打包结构——渲染什么截什么，改完课件**直接重跑**即可。
- **layer 页自动展开**：带 `[data-layer-btn]` 的页会逐标签各截一张、按顺序全部进 PPTX（一页 N 个标签 → N 张）；一页有多个 layer 组时逐组展开、其余组停在首标签，全默认态只截一张不重复（共 ΣN − (组数 − 1) 张）。所以模板 34 页导出为 **55 张**（`动画·layer切换` 4 张、`动画·混合链` 5 张、`动画·多组切换` 2 组共 5 张、`SFT vs LoRA` 6 张、`找问题·六层级` 6 张）。实测约 47 秒、22MB。
- 已知限制：靠 React 内部 state 切换的自制交互页无法程序化展开，只能截到默认状态（模板自带页没有这种页；自己加页时若做了这类交互，导出前心里有数）。
- 依赖：Node + Chrome + playwright-core（同第 6 节三级查找）、`python3 -m pip install python-pptx`。

## 8. 性能守则

- **别删内联的 React / 字体**。运行时默认从 CDN 拉 React——正因模板把 react / react-dom UMD 内联在运行时脚本之前才真离线；删了它，断网 / 代理环境整页起不来。`scripts/react.umd.js` / `react-dom.umd.js` 是备件，误删后可用 `eb.inline_react(lines, 'scripts/react.umd.js', 'scripts/react-dom.umd.js')` 修复。
- iframe 一律 `loading="lazy"`；能重画成矢量 / HTML 的图别贴低清大截图。
- **大改用 Python 切片，别开编辑器**——那两行 JSON 每行数 MB，多数编辑器会卡死或悄悄截断。
- 参考基线：模板 12MB，headless Chrome 首开约 2.6 秒；桌面浏览器首次打开多等几秒属正常，不是卡死。用 `file://` 直开时控制台可能有 2 条 CORS 报错，良性，忽略即可。
