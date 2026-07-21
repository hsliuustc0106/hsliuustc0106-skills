#!/usr/bin/env node
// measure_overflow.mjs — 检测 deck 每页的内容溢出（section 级 + 内层 overflow:hidden 裁切）
//
// 用法:
//   node measure_overflow.mjs <deck.html> [label ...]   # 只测指定 data-label 的页
//   node measure_overflow.mjs <deck.html> --all         # 测全部含 section[data-label] 的页（不传 label 同 --all）
//
// 输出: 每页 label、section 溢出 Y/X（像素）、内层 overflow:hidden 裁切数量与 top 条目。
// --all 模式按 canvas 逐页遍历，同名 label 各测各的（第二个起后缀 #2/#3 区分）；
// 指定 label 且存在同名页时只测第一个并打印警告。内层裁切只报告、不判失败。
//
// 退出码契约: 0 = 通过；1 = 检测到问题（存在溢出 / label 不存在）；2 = 工具或参数错误。
//
// 依赖: Node >= 18、本机安装 Google Chrome、playwright-core。
// playwright-core 查找顺序: 环境变量 PLAYWRIGHT_CORE → import('playwright-core') → openclaw 内置路径。

import { existsSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

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

const [deckFile, ...rest] = process.argv.slice(2);
if (!deckFile) { console.error('用法: node measure_overflow.mjs <deck.html> [label ...|--all]'); process.exit(2); }
if (!existsSync(deckFile)) { console.error(`找不到 deck 文件: ${deckFile}`); process.exit(2); }
const wantLabels = rest.filter(a => a !== '--all');

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
    .stage .slide-canvas{content-visibility:visible!important;}` });
  // build 元素全显后再测，避免隐藏态漏测
  await page.evaluate(() => document.querySelectorAll('.build').forEach(el => {
    el.style.opacity = '1'; el.style.transform = 'none'; el.style.filter = 'none';
  }));
  await page.waitForTimeout(400); // 强显后的重排 settle

  // 全部 canvas 的 { idx, label }（label 为 null 表示该 canvas 无 section[data-label]）
  const pages = await page.evaluate(() =>
    [...document.querySelectorAll('.stage .slide-canvas')].map((c, i) =>
      ({ idx: i, label: c.querySelector('section[data-label]')?.dataset.label ?? null })));
  const allLabels = pages.filter(p => p.label !== null).map(p => p.label);

  // 待测清单：--all 按 canvas 遍历（同名各测各的）；显式 label 只取第一个匹配并警告
  const targets = [];
  if (wantLabels.length === 0) {
    const seen = new Map();
    for (const p of pages) {
      if (p.label === null) continue;
      const n = (seen.get(p.label) ?? 0) + 1; seen.set(p.label, n);
      targets.push({ idx: p.idx, disp: n > 1 ? `${p.label} #${n}` : p.label });
    }
  } else {
    for (const lbl of wantLabels) {
      const hits = pages.filter(p => p.label === lbl);
      if (hits.length === 0) {
        console.error(`找不到 data-label="${lbl}"。可用 label（${allLabels.length} 个）:`);
        for (const l of allLabels) console.error('  ' + l);
        exitCode = 1; continue;
      }
      if (hits.length > 1) console.warn(`警告: data-label="${lbl}" 有 ${hits.length} 个同名页，只测第一个（全测请用 --all）`);
      targets.push({ idx: hits[0].idx, disp: lbl });
    }
  }

  for (const t of targets) {
    const handle = await page.evaluateHandle(i => document.querySelectorAll('.stage .slide-canvas')[i], t.idx);
    const el = handle.asElement();
    await el.scrollIntoViewIfNeeded();      // 原位测量，不要 position:fixed 钉页（canvas 祖先有 transform）
    await page.waitForTimeout(250);         // 滚动/懒渲染稳定
    const r = await el.evaluate((node, trunc) => {
      const sect = node.querySelector('section');
      if (!sect) return null;
      const clips = [];
      for (const e of node.querySelectorAll('*')) {
        const cs = getComputedStyle(e);
        const txt = (e.innerText || '').replace(/\s+/g, ' ').slice(0, trunc);
        if ((cs.overflow === 'hidden' || cs.overflowY === 'hidden') && e.scrollHeight - e.clientHeight > 2)
          clips.push({ dir: 'Y', amt: Math.round(e.scrollHeight - e.clientHeight), txt });
        if ((cs.overflow === 'hidden' || cs.overflowX === 'hidden') && e.scrollWidth - e.clientWidth > 2)
          clips.push({ dir: 'X', amt: Math.round(e.scrollWidth - e.clientWidth), txt });
      }
      clips.sort((a, b) => b.amt - a.amt);
      return { y: Math.round(sect.scrollHeight - sect.clientHeight),
               x: Math.round(sect.scrollWidth - sect.clientWidth),
               nClips: clips.length, top: clips.slice(0, 6) };
    }, TRUNC);
    if (r === null) { console.log(`--- ${t.disp} ---  页内无 section，跳过测量（请检查页面结构）`); continue; }
    console.log(`--- ${t.disp} ---  section overflow Y=${r.y} X=${r.x}  nested clips=${r.nClips}`);
    for (const c of r.top) console.log(`    clip ${c.dir} +${c.amt}px  ${JSON.stringify(c.txt)}`);
    if (r.y > 0 || r.x > 0) exitCode = 1;
  }
} catch (e) {
  console.error('执行失败（浏览器/页面基础设施错误）: ' + (e?.message ?? e));
  exitCode = 2;
} finally {
  if (browser) await browser.close().catch(() => {});
}
process.exit(exitCode);
