#!/usr/bin/env node
// steps.mjs — 模拟放映态，把某一页的动画逐拍截图（step-00.jpg, step-01.jpg, ...）
//
// 用法:
//   node steps.mjs <deck.html> <label> <outdir>
//
// 引擎规则（与 deck 运行时一致）:
//   - build:  class="build" data-step="N"，点击计数 level > N 时显示（无 data-step 视作 0）
//   - layer:  [data-layer-btn]/[data-layer-panel] 同 key 同 group 联动 data-active；
//             组内 active = data-step < level 的按钮中 data-step 最大者，否则组内第一个按钮
//   - 总拍数 = 页内最大 data-step + 2（level 从 0 到 max+1，每拍一张图）
// 每拍打印新出现的元素摘要，便于核对讲课节奏。页面无动画时打印提示后 exit 0。
// label 找不到时列出全部可用 label；存在同名页时只处理第一个并打印警告。
//
// 退出码契约: 0 = 成功（含无动画页）；1 = 检测到问题（label 不存在）；2 = 工具或参数错误。
//
// 依赖: Node >= 18、本机安装 Google Chrome、playwright-core。
// playwright-core 查找顺序: 环境变量 PLAYWRIGHT_CORE → import('playwright-core') → openclaw 内置路径。

import { existsSync, mkdirSync, readdirSync, unlinkSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { join } from 'node:path';

const TRUNC = 36; // 元素文本摘要统一截断长度

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

const [deckFile, label, outDir] = process.argv.slice(2);
if (!deckFile || !label || !outDir) { console.error('用法: node steps.mjs <deck.html> <label> <outdir>'); process.exit(2); }
if (!existsSync(deckFile)) { console.error(`找不到 deck 文件: ${deckFile}`); process.exit(2); }

const chromium = await loadChromium();
let browser, exitCode = 0;
try {
  browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(deckFile).href, { waitUntil: 'load', timeout: 180000 }); // 单文件 deck 很大，放宽超时
  await page.waitForFunction(() => document.querySelectorAll('.stage .slide-canvas').length > 0, { timeout: 60000 });
  await page.waitForTimeout(5000); // React mount + 字体/图片 settle
  await page.addStyleTag({ content: `
    .glassbar.railtoggle,.glassbar.navbar,.glassbar.modebar,.railpanel,.railfoot,.hint,.noteschip,#__deck_loading_overlay{display:none!important;}
    .stage .slide-canvas{content-visibility:visible!important;}
    img[alt="HUAWEI"], img[data-brand-logo] { right: 30px !important; } /* fixed logo 超出 canvas 元素框右缘会被 element.screenshot 裁掉 → 左移 8px */
    [data-steps-target] .build{opacity:0!important; transition:none!important;}
    [data-steps-target] .build[data-shown]{opacity:1!important; transform:none!important; filter:none!important;}` });

  // 定位目标页（CSS.escape 防 label 含引号/特殊字符；同名页只取第一个）
  const idxs = await page.evaluate(lbl => {
    const out = [];
    document.querySelectorAll('.stage .slide-canvas').forEach((c, i) => {
      if (c.querySelector(`section[data-label="${CSS.escape(lbl)}"]`)) out.push(i);
    });
    return out;
  }, label);
  if (idxs.length === 0) {
    const all = await page.evaluate(() =>
      [...document.querySelectorAll('.stage .slide-canvas section[data-label]')].map(s => s.dataset.label));
    console.error(`找不到 data-label="${label}"。可用 label（${all.length} 个）:`);
    for (const l of all) console.error('  ' + l);
    exitCode = 1;
  } else {
    if (idxs.length > 1) console.warn(`警告: data-label="${label}" 有 ${idxs.length} 个同名页，只处理第一个`);
    const handle = await page.evaluateHandle(i => document.querySelectorAll('.stage .slide-canvas')[i], idxs[0]);
    const el = handle.asElement();

    const info = await el.evaluate(node => {
      node.setAttribute('data-steps-target', ''); // 模拟放映的 CSS 只作用于本页
      const steps = [...node.querySelectorAll('[data-step]')]
        .map(e => parseInt(e.getAttribute('data-step'), 10)).filter(Number.isFinite);
      return { max: steps.length ? Math.max(...steps) : 0,
               nBuild: node.querySelectorAll('.build').length,
               nLayerBtn: node.querySelectorAll('[data-layer-btn]').length };
    });
    if (info.nBuild === 0 && info.nLayerBtn === 0) {
      console.log(`此页无动画（无 .build / layer 元素）: ${label}`);
    } else {
      mkdirSync(outDir, { recursive: true });
      for (const f of readdirSync(outDir))            // 清掉旧的逐拍图，避免上次残留混淆
        if (/^step-\d+\.jpg$/.test(f)) unlinkSync(join(outDir, f));
      await el.scrollIntoViewIfNeeded();              // 原位截图，不要 position:fixed 钉页（canvas 祖先有 transform）
      await page.waitForTimeout(600);                 // 滚动/懒渲染稳定

      console.log(`"${label}"  builds=${info.nBuild} layerBtns=${info.nLayerBtn} maxStep=${info.max} → ${info.max + 2} 拍`);
      for (let L = 0; L <= info.max + 1; L++) {
        const appeared = await el.evaluate((node, arg) => {
          const brief = e => `<${e.tagName.toLowerCase()}> ${(e.innerText || '').replace(/\s+/g, ' ').trim().slice(0, arg.trunc)}`;
          const out = [];
          for (const b of node.querySelectorAll('.build')) {
            const step = b.hasAttribute('data-step') ? parseInt(b.getAttribute('data-step'), 10) : 0;
            const show = step < arg.lvl;
            if (show && !b.hasAttribute('data-shown')) out.push('build ' + brief(b));
            b.toggleAttribute('data-shown', show);
          }
          const groups = new Map();
          for (const b of node.querySelectorAll('[data-layer-btn]')) {
            const g = b.getAttribute('data-layer-group') || '';
            if (!groups.has(g)) groups.set(g, []);
            groups.get(g).push(b);
          }
          for (const [g, btns] of groups) {
            let act = null, best = -1;
            for (const b of btns) {
              if (!b.hasAttribute('data-step')) continue;
              const s = parseInt(b.getAttribute('data-step'), 10);
              if (s < arg.lvl && s > best) { best = s; act = b; }
            }
            if (!act) act = btns[0]; // 无满足者取组内第一个按钮（默认层）
            if (!act.hasAttribute('data-active')) out.push(`layer[${g}]→${act.getAttribute('data-layer-btn')} ` + brief(act));
            const key = act.getAttribute('data-layer-btn');
            for (const b of btns) b.toggleAttribute('data-active', b === act);
            for (const p of node.querySelectorAll(`[data-layer-panel][data-layer-group="${CSS.escape(g)}"]`))
              p.toggleAttribute('data-active', p.getAttribute('data-layer-panel') === key);
          }
          return out;
        }, { lvl: L, trunc: TRUNC });
        await page.waitForTimeout(200); // 状态切换后的重绘 settle
        const out = join(outDir, `step-${String(L).padStart(2, '0')}.jpg`);
        await el.screenshot({ path: out, type: 'jpeg', quality: 90 }); // 90 = 清晰度/体积平衡
        console.log(`step ${String(L).padStart(2, '0')} -> ${out}` + (appeared.length ? '' : '  （无新增）'));
        for (const a of appeared) console.log('    + ' + a);
      }
    }
  }
} catch (e) {
  console.error('执行失败（浏览器/页面基础设施错误）: ' + (e?.message ?? e));
  exitCode = 2;
} finally {
  if (browser) await browser.close().catch(() => {});
}
process.exit(exitCode);
