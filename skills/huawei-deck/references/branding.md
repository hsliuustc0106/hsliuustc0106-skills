# branding.md — 品牌可替换点指南

模板 deck（`assets/template-deck.html`）里所有「华为味」的品牌元素都是可替换的。本文说明每个替换点在哪里、怎么换、换完怎么验证。需要华为官方封面 KV / logo / 图标等现成素材时，直接取 `assets/huawei-refs/`（从官方 PPT 提取，内附索引）。

**先备份再动手**。所有命令都假设你在 skill 根目录（`huawei-deck/`）下执行，且已把模板复制为自己的工作文件：

```bash
cp assets/template-deck.html my-deck.html
```

---

## 1. 品牌元素清单

| 元素 | 当前资源（manifest key 前 12 位 / 现规格） | 影响页面 | 替换方式 |
|---|---|---|---|
| 金色门面背景画 | `tplbg-057d9f…`（JPEG 1920×1080，约 670KB） | 封面、目录、章扉页、结语页（**两套变体已白底化，仅授课模板全量生效**） | `apply_bg.py --target bg` |
| 金框黑板底图 | `tplboard-cacd…`（PNG 1887×1062） | 黑板·题卡A、黑板·金框题卡 | `apply_bg.py --target board` |
| 右下人像装饰 | `tplppl-3f0d59…`（PNG 271×266，透明底） | 问题页、研讨页 | `apply_bg.py --target people` |
| HUAWEI logo 水印 | `18fc27a8-f87c…`（PNG 266×60，透明底） | 全部页面（`position:fixed` 右下角） | `apply_bg.py --target logo` |
| 口号文案 | 占位文本「在此替换口号…」×2 | 封面、结语页 | 文本替换（见第 3 节） |
| 品牌红色系 | `#b5333b` 等（见第 4 节） | 全部页面 | 色值映射替换（见第 4 节） |

> key 是当前模板的初始值，仅供识别。`apply_bg.py` 每次运行都会重新从 deck 里解析当前 key，所以**换过一次之后还能再换**，不依赖上表。

## 2. 换图片：apply_bg.py

```bash
# 先跑一遍不带 --yes：只打印替换摘要和建议的备份命令，不写盘
python3 scripts/apply_bg.py my-deck.html 你的背景画.jpg

# 确认无误后加 --yes 落盘
python3 scripts/apply_bg.py my-deck.html 你的背景画.jpg --yes

# 其他三个替换点（同样建议先去掉 --yes 预览一遍再执行）
python3 scripts/apply_bg.py my-deck.html 你的黑板底图.png --target board --yes
python3 scripts/apply_bg.py my-deck.html 你的插画.png     --target people --yes
python3 scripts/apply_bg.py my-deck.html 你的logo.png     --target logo --yes
```

脚本做的事：把新图嵌入 manifest → 把 deck 内旧图的全部引用替换为新图 → 从 manifest 删除旧图条目（不留死重量）→ 落盘后复核（旧 key 零残留、引用数一致、manifest 合法）并跑 `edit-bundle.py` 的 verify。

各 target 的建议图片规格（按现资源尺寸推断）：

| target | 建议规格 | 说明 |
|---|---|---|
| `bg` | **1920×1080 JPEG**，控制在 1MB 内 | 铺满整页（`center/cover`），顶部会叠一层淡白渐变洗，选顶部偏浅的画面文字更清晰 |
| `board` | **约 1920×1080 PNG**，边框图案完整 | 以 `100% 100%` 拉伸铺满，内容内缩在 74px/124px padding 内，边框别太宽 |
| `people` | **透明背景 PNG**，接近方形（现 271×266） | 显示区 330×324，`contain` 缩放、底对齐，非透明底会出现白块 |
| `logo` | **透明背景 PNG，横向条状**（现 266×60） | 显示宽度固定 104px、高度自适应，太方/太高会显得突兀 |

失败排查：退出码 2 = 参数/文件问题（路径不对、图不是 jpg/png）；退出码 1 = deck 里找不到目标引用（比如 `<style id="tpl-bg-950">` 被删过，或 logo `<img>` 的 `alt="HUAWEI"` 被改名——可以给该 img 加 `data-brand-logo` 属性让脚本重新识别）。

## 3. 换口号

口号是纯文本占位，占位内容完全相同。**各模板处数：授课模板 2 处（封面底部、结语页居中）；技术分享模板 1 处（仅结语页，封面已改深色 KV 版式）；汇报模板 0 处（官方化改版已移除）**——下方脚本的 `assert count == 2` 仅适用于授课模板，其他模板按实际处数改断言：

```
在此替换口号　八字四段　全角空格分隔　详见branding
```

约定：口号为「八字四段」体（如 `转型强基　铸魂精神　千军万马　奔赴战场`），段与段之间用 **U+3000 全角空格**（`　`）分隔——不要用半角空格，否则间距会明显变窄、气势全无。

替换必须经 `edit-bundle.py`（template 是 JSON 字符串，直接编辑 HTML 文件会破坏转义）：

```bash
python3 - <<'EOF'
import importlib.util
spec = importlib.util.spec_from_file_location('eb', 'scripts/edit-bundle.py')
eb = importlib.util.module_from_spec(spec); spec.loader.exec_module(eb)

OLD = '在此替换口号　八字四段　全角空格分隔　详见branding'
NEW = '转型强基　铸魂精神　千军万马　奔赴战场'   # ← 换成你的口号

lines = eb.load('my-deck.html')
s = eb.get_template(lines)
assert s.count(OLD) == 2, '占位口号应恰有 2 处，实际 %d' % s.count(OLD)
eb.set_template(lines, s.replace(OLD, NEW))
eb.save('my-deck.html', lines)
eb.verify('my-deck.html')
EOF
```

再次更换口号时，把脚本里的 `OLD` 换成 deck 当前的口号文本（`assert` 的 2 处计数同样适用）。

## 4. 整体换品牌色

模板的品牌色是一套红色系，直接对 template 字符串做全局映射替换即可：

| 现色值 | 角色 | 出现次数（初始模板） | 换成 |
|---|---|---|---|
| `#b5333b` | 主红（标题强调、色块、eyebrow、导航高亮） | ~346 | 你的主品牌色 |
| `rgba(181,51,59,.xx)` | 主红的半透明变体（边框、底纹、阴影，α 各异） | ~34 | 你的主色 RGB + 保留各自 α |
| `#cf6b72` | 辅红（深色页上的浅红强调） | ~26 | 你的主色提亮 1 档 |
| `#e0a3a7` | 淡红（深色页次要文字） | ~4 | 你的主色提亮 2 档 |

方法（同样必须经 edit-bundle）：

```bash
python3 - <<'EOF'
import importlib.util
spec = importlib.util.spec_from_file_location('eb', 'scripts/edit-bundle.py')
eb = importlib.util.module_from_spec(spec); spec.loader.exec_module(eb)

MAP = {                       # 旧 → 新（示例：换成深蓝系）
    '#b5333b': '#1f4e8c',
    'rgba(181,51,59': 'rgba(31,78,140',   # 前缀替换，保留每处各自的透明度
    '#cf6b72': '#5b82b8',
    '#e0a3a7': '#a9bdd8',
}
lines = eb.load('my-deck.html')
s = eb.get_template(lines)
for old, new in MAP.items():
    n = s.count(old); s = s.replace(old, new)
    print('%s -> %s : %d 处' % (old, new, n))
eb.set_template(lines, s)
eb.save('my-deck.html', lines)
eb.verify('my-deck.html')
EOF
```

注意：

- 脚本会逐行打印每个色值的替换处数：**若某行打印 0 处，说明该色值不对（可能已换过色或写错），停下检查**，不要带着 0 继续。
- **警示红与品牌红同值**：模板里表示「错误 / 危险 / 反例」的红也用 `#b5333b`，全局映射会把它一起换掉。如果你的新主色不是暖色（如换成蓝），换完后请翻看含对错对比、告警标注的页面，确认语义仍读得通；必要时把个别警示处手工改回一个独立的红（如 `#d4001a`）。
- 色值都是小写；替换用精确字符串匹配即可，模板内没有大写变体。
- 改完必须验证：

```bash
node scripts/verify/measure_overflow.mjs my-deck.html --all      # 应 0 溢出
node scripts/verify/shot.mjs my-deck.html 封面 /tmp/cover.jpg    # 抽几页截图目检
node scripts/verify/shot.mjs my-deck.html 深色·金句 /tmp/dark.jpg # 深色页重点看对比度
```

## 5. 注意事项（铁律）

1. **改 template 必须经 `edit-bundle.py` 的 `get_template` / `set_template` / `save`**。deck 的 HTML 存在 `<script type="__bundler/template">` 下一行的 JSON 字符串里，`set_template` 负责唯一正确的转义（把 `</` 转成 `<\u002F`，防止字符串里的 `</script>` 提前闭合）；直接用编辑器 / sed 改这一行几乎必然把文件改坏。
2. **manifest（`<script type="__bundler/manifest">` 下一行）是一整行 JSON dict**，手改容易截断；嵌图用 `eb.embed_image`，换图用 `apply_bg.py`。
3. 改前备份（`cp my-deck.html my-deck.bak.html`），`apply_bg.py` 不带 `--yes` 的预览输出里也会给出建议命令。
4. 改后验证清单：
   - `python3 scripts/edit-bundle.py my-deck.html` —— 结构验证（页数 / nav / chapters 一致）；
   - `node scripts/verify/measure_overflow.mjs my-deck.html --all` —— 无内容溢出；
   - `node scripts/verify/shot.mjs my-deck.html <label> out.jpg` —— 抽改动涉及的页截图目检（门面页换 bg 后至少看封面 + 一张章扉页；换 logo 看任意页右下角）。
5. 浏览器打开 `file://` 时控制台可能有 2 条 CORS 报错，属良性，可忽略。
