// shoot.mjs — 把 DC 独立版 HTML 课件逐页截图为 JPEG
// 用法: node shoot.mjs <input.html> <outDir> [scale] [quality]
// 输出: outDir/slide-001.jpg ... 以及 outDir/manifest.json
//
// 多状态页（页内多标签）处理：对每页检测 [data-layer-btn]/[data-layer-panel]
// 标签组，逐个激活每个标签并各截一张图 → PPTX 里每个标签内容都保留。
// 顺序写入 manifest（扁平有序），build_pptx 按序一页一图。
import { writeFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

// playwright-core 查找顺序: 环境变量 PLAYWRIGHT_CORE → import('playwright-core') → openclaw 内置路径。
async function loadChromium() {
  const candidates = [process.env.PLAYWRIGHT_CORE, 'playwright-core',
    '/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core/index.js'].filter(Boolean);
  for (const c of candidates) {
    try { const m = await import(c); return (m.default ?? m).chromium; } catch { /* 尝试下一个 */ }
  }
  console.error(`无法加载 playwright-core（已尝试: ${candidates.join(' → ')}）`);
  console.error('请在本目录 npm i playwright-core，或设环境变量 PLAYWRIGHT_CORE 指向其 index.js');
  process.exit(2);
}
const chromium = await loadChromium();

const [, , inFile, outDir, scaleArg, qualArg] = process.argv;
if (!inFile || !outDir) {
  console.error('用法: node shoot.mjs <input.html> <outDir> [scale=2] [quality=92]');
  process.exit(1);
}
const scale = Number(scaleArg) || 2;
const quality = Number(qualArg) || 92;
const W = 1920, H = 1080;               // 课件原生分辨率（每页 .slide-canvas）
mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch({ channel: 'chrome', headless: true });
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: scale });
console.error('载入 HTML（大文件，请稍候）…');
await page.goto('file://' + encodeURI(resolve(inFile)), { waitUntil: 'load', timeout: 180000 });
await page.waitForTimeout(3000);

// 隐藏所有 UI 外壳（导航条 / 预览栏 / 提示条 / 记笔记 / 模式钮），保留华为 LOGO 水印
await page.addStyleTag({ content: `
  .glassbar.railtoggle, .glassbar.navbar, .glassbar.modebar,
  .railpanel, .railfoot, .hint, .noteschip { display: none !important; }
  /* logo 是 position:fixed right:22px，比 1864 宽的 canvas 元素框更靠右，element.screenshot 会裁掉右缘 → 左移 8px 收进框内 */
  img[alt="HUAWEI"], img[data-brand-logo] { right: 30px !important; }
` });

// 确保滚动模式 + 所有 .build 渐显内容可见，避免漏截
await page.evaluate(() => {
  document.querySelectorAll('.build').forEach(el => {
    el.style.opacity = '1';
    el.style.transform = 'none';
    el.style.filter = 'none';
    el.classList.add('in', 'show', 'visible');
  });
});
await page.waitForTimeout(500);

// 探测每页的标签组：{ idx, groups: { groupName: [keys...] } }
const slideTabs = await page.evaluate(() => {
  const slides = [...document.querySelectorAll('.stage .slide-canvas')];
  return slides.map((sl, idx) => {
    const groups = {};
    sl.querySelectorAll('[data-layer-btn]').forEach(b => {
      const g = b.getAttribute('data-layer-group') || '(none)';
      (groups[g] = groups[g] || []).push(b.getAttribute('data-layer-btn'));
    });
    // 只保留真正有对应 panel 的组（避免误判）
    const real = {};
    Object.keys(groups).forEach(g => {
      const panels = sl.querySelectorAll(`[data-layer-panel][data-layer-group="${g}"]`);
      if (panels.length > 0) real[g] = groups[g];
    });
    return { idx, groups: real };
  });
});

const slideHandles = await page.$$('.stage .slide-canvas');
console.error(`共 ${slideHandles.length} 页，开始截图 (scale=${scale}, q=${quality})…`);

// 激活某页某组的某个标签：同步 btn + panel 的 data-active
async function setActive(idx, group, key) {
  await page.evaluate(({ idx, group, key }) => {
    const sl = document.querySelectorAll('.stage .slide-canvas')[idx];
    sl.querySelectorAll(`[data-layer-btn][data-layer-group="${group}"]`).forEach(b =>
      b.toggleAttribute('data-active', b.getAttribute('data-layer-btn') === key));
    sl.querySelectorAll(`[data-layer-panel][data-layer-group="${group}"]`).forEach(pn =>
      pn.toggleAttribute('data-active', pn.getAttribute('data-layer-panel') === key));
  }, { idx, group, key });
}

let shotIdx = 0;
const manifest = [];
async function shoot(idx) {
  const el = slideHandles[idx];
  await el.scrollIntoViewIfNeeded();
  await page.waitForTimeout(250); // 等懒加载图片/字体/面板过渡绘制
  const name = `slide-${String(++shotIdx).padStart(3, '0')}.jpg`;
  await el.screenshot({ path: `${outDir}/${name}`, type: 'jpeg', quality });
  manifest.push(name);
}

for (let i = 0; i < slideHandles.length; i++) {
  const tabs = slideTabs[i];
  const groupNames = Object.keys(tabs.groups);
  if (groupNames.length === 0) {
    await shoot(i);
  } else {
    // 先把所有组重置到第一个标签（确定性起点）
    for (const g of groupNames) await setActive(i, g, tabs.groups[g][0]);
    await page.waitForTimeout(150);
    // 逐组、逐标签截图：每个标签面板都在其他组的默认态（首标签）下截取
    for (let gi = 0; gi < groupNames.length; gi++) {
      if (gi > 0) {
        for (const og of groupNames) await setActive(i, og, tabs.groups[og][0]);
        await page.waitForTimeout(100);
      }
      const keys = tabs.groups[groupNames[gi]];
      for (let ki = 0; ki < keys.length; ki++) {
        // 全默认态已随第一组的首标签截过一张，其余组跳过首标签避免重复页
        if (gi > 0 && ki === 0) continue;
        await setActive(i, groupNames[gi], keys[ki]);
        await shoot(i);
      }
    }
  }
  if ((i + 1) % 10 === 0 || i === slideHandles.length - 1) console.error(`  已处理 ${i + 1}/${slideHandles.length} 页（截图 ${manifest.length} 张）`);
}

writeFileSync(`${outDir}/manifest.json`, JSON.stringify({ width: W, height: H, scale, slides: manifest }, null, 2));
console.error(`截图完成。共 ${manifest.length} 张（${slideHandles.length} 页，含标签展开）。`);
await browser.close();
