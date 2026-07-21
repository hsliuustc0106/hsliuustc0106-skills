#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apply_bg.py — 替换模板 deck 的品牌图片资源（门面背景画 / 黑板底图 / 人像装饰 / logo 水印）。

用法:
    python3 apply_bg.py <deck.html> <new-image> [--target bg|board|people|logo] [--yes]

target（默认 bg）:
    bg      金色门面背景画 —— 封面 / 目录 / 章扉页 / 结语页（建议 1920x1080 JPEG）
    board   金框黑板底图 —— 两个黑板题卡页（建议 1920x1080 左右、带完整边框的 PNG）
    people  右下角人像 / 插画装饰 —— 问题页 / 研讨页（建议透明背景 PNG）
    logo    右下角全局 logo 水印（建议透明背景 PNG，宽约 260px）

行为: 不加 --yes 时只打印替换摘要（含建议的备份命令）后退出，不写盘；加 --yes 才落盘。
旧图的 key 在运行时从 deck 里解析（bg/board/people 取自 <style id="tpl-bg-950"> 对应规则的
url()，logo 取自 alt="HUAWEI" 或 data-brand-logo 的 <img> 的 src），换过一次后仍可再换。
退出码: 0 成功 / 1 业务失败（deck 里找不到目标引用等）/ 2 参数或环境错误。
依赖: 同目录的 edit-bundle.py。
"""
import argparse, importlib.util, json, os, re, sys

TARGETS = {  # target -> (新 key 前缀, 描述, tpl-bg-950 规则选择器标记; logo 特判)
    'bg':     ('tplbg',     '金色门面背景画（封面/目录/章扉页/结语页）', 'data-label="封面"'),
    'board':  ('tplboard',  '金框黑板底图（黑板题卡页）',               'data-label="黑板'),
    'people': ('tplppl',    '右下角人像装饰（问题页/研讨页）',           '::after'),
    'logo':   ('brandlogo', '右下角全局 logo 水印',                     None),
}

def die(code, msg):
    print('错误: ' + msg, file=sys.stderr); sys.exit(code)

def load_eb():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'edit-bundle.py')
    if not os.path.isfile(p):
        die(2, '缺少依赖 %s（应与本脚本同目录分发）' % p)
    spec = importlib.util.spec_from_file_location('eb', p)
    eb = importlib.util.module_from_spec(spec); spec.loader.exec_module(eb)
    return eb

def sniff_mime(path):
    with open(path, 'rb') as f:
        head = f.read(8)
    if head[:2] == b'\xff\xd8':
        return 'image/jpeg'
    if head[:8] == b'\x89PNG\r\n\x1a\n':
        return 'image/png'
    return None

def find_old_key(s, target):
    """运行时从 deck template 字符串解析当前 target 引用的资源 key；找不到返回 None。"""
    if target == 'logo':
        for m in re.finditer(r'<img\b[^>]*>', s):
            tag = m.group(0)
            if 'alt="HUAWEI"' in tag or 'data-brand-logo' in tag:
                sm = re.search(r'src="([^"]+)"', tag)
                if sm:
                    return sm.group(1)
        return None
    i = s.find('<style id="tpl-bg-950">')
    j = s.find('</style>', i)
    if i < 0 or j < 0:
        return None
    block = s[i:j]
    marker = TARGETS[target][2]
    for rule in re.finditer(r'([^{}]+)\{([^{}]*)\}', block):
        if marker in rule.group(1):
            um = re.search(r'url\("([^"]+)"\)', rule.group(2))
            if um:
                return um.group(1)
    return None

def main():
    ap = argparse.ArgumentParser(description='替换独立版 deck 的品牌图片资源', add_help=True)
    ap.add_argument('deck', help='独立版 deck HTML 文件路径')
    ap.add_argument('image', help='新图片（jpg/png）')
    ap.add_argument('--target', choices=sorted(TARGETS), default='bg')
    ap.add_argument('--yes', action='store_true', help='确认执行（缺省只打印摘要不写盘）')
    args = ap.parse_args()
    if not os.path.isfile(args.deck):
        die(2, '找不到 deck 文件: %s' % args.deck)
    if not os.path.isfile(args.image):
        die(2, '找不到图片文件: %s' % args.image)
    mime = sniff_mime(args.image)
    if not mime:
        die(2, '%s 不是 JPEG/PNG（按文件头识别）。仅支持 jpg/png。' % args.image)

    eb = load_eb()
    try:
        lines = eb.load(args.deck); s = eb.get_template(lines)
        man = json.loads(lines[eb._man_idx(lines)].strip())
    except Exception as e:
        die(1, '%s 不是合法的独立版 deck（缺 __bundler/template 或 manifest，或无法读取）: %s' % (args.deck, e))
    old = find_old_key(s, args.target)
    if not old:
        die(1, 'deck 里找不到 target=%s 的当前引用（%s）。'
               'bg/board/people 需存在 <style id="tpl-bg-950"> 对应规则的 url()，'
               'logo 需存在 alt="HUAWEI" 或 data-brand-logo 的 <img>。'
               % (args.target, TARGETS[args.target][1]))
    refs = s.count(old)
    if old not in man:
        die(1, 'template 引用了 key %s，但 manifest 中没有这个条目（deck 可能已损坏）。' % old)

    prefix, desc, _ = TARGETS[args.target]
    print('目标      : %s — %s' % (args.target, desc))
    print('旧资源    : %s (%s, %d 字节, deck 内 %d 处引用)'
          % (old, man[old].get('mime'), len(man[old].get('data', '')) * 3 // 4, refs))
    print('新图片    : %s (%s, %d 字节)' % (args.image, mime, os.path.getsize(args.image)))
    if not args.yes:
        print('\n[预览模式] 未写盘。建议先备份，再加 --yes 执行:')
        print('  cp "%s" "%s"' % (args.deck, re.sub(r'\.html?$', '', args.deck) + '.bak.html'))
        print('  python3 "%s" "%s" "%s" --target %s --yes'
              % (os.path.abspath(__file__), args.deck, args.image, args.target))
        return 0

    uid = eb.embed_image(lines, args.image, mime=mime, prefix=prefix)   # 1) 新图入 manifest
    s2 = s.replace(old, uid)                                            # 2) 替换全部引用
    if old in s2 or s2.count(uid) != refs:
        die(1, '引用替换数不符（旧 %d 处 / 新 %d 处），未写盘。' % (refs, s2.count(uid)))
    eb.set_template(lines, s2)                                          # 3) 铁律: 经 set_template 回填
    mi = eb._man_idx(lines); mraw = lines[mi]                           # 4) 删旧 manifest 条目
    lead = mraw[:len(mraw) - len(mraw.lstrip())]
    man = json.loads(mraw.strip()); del man[old]
    lines[mi] = lead + json.dumps(man, ensure_ascii=False, separators=(',', ':'))
    tmp = args.deck + '.tmp-applybg'                                    # 5) 原子写盘: 临时文件 + rename
    eb.save(tmp, lines)
    os.replace(tmp, args.deck)

    lines2 = eb.load(args.deck)                                         # 6) 从盘上复核
    s3 = eb.get_template(lines2)
    man2 = json.loads(lines2[eb._man_idx(lines2)].strip())
    if old in '\n'.join(lines2):
        die(1, '落盘复核失败: 旧 key %s 仍有残留。' % old)
    if s3.count(uid) != refs or uid not in man2:
        die(1, '落盘复核失败: 新 key %s 的引用数或 manifest 条目不符。' % uid)
    eb.verify(args.deck)
    print('完成: %s 的 %d 处引用已替换为 %s，旧条目已从 manifest 删除。' % (old, refs, uid))
    return 0

if __name__ == '__main__':
    sys.exit(main())
