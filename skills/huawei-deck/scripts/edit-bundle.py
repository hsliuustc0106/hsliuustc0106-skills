# -*- coding: utf-8 -*-
"""
edit-bundle.py — 安全编辑「独立版」单文件 deck 的工具函数。

独立版结构（约 187 行）：
  - 行 184(索引)  <script type="__bundler/manifest">  ← 上一行；行 176(索引) 是 28MB JSON dict {uuid:{mime,compressed,data(base64)}}
  - 行 184(索引)  <script type="__bundler/template"> 的内容（行 185/索引184）= 整份 deck 的 HTML，存成一个 JSON 字符串
  实际索引以代码里的探测为准（找 '<script type="__bundler/template">' 的下一行）。

铁律：
  1) 编码必须 dump_template()：json.dumps(s, ensure_ascii=False).replace('</','<\\u002F')
     —— 只转义 '</'（防 </script> 提前闭合 + 子标签）；CJK 不转义；URL 里普通 '/' 不动。
  2) 回填后断言 '</' not in raw 且 json.loads(raw)==s。
  3) 改结构必须三处同步：slide DOM / nav[] / chapters[]。下面的 insert/delete/move 已做完。
  4) data-idx 必须是数字。

典型用法：
  bundle = load(PATH); s = get_template(bundle)
  s = insert_page(s, new_block, before_label='LoRA 原理')   # 或 before_idx
  set_template(bundle, s); save(PATH, bundle); verify(PATH)
"""
import json, base64, gzip, zlib, uuid, re

# ---------------- 读写 ----------------
def load(path):
    return open(path, encoding='utf-8').read().split('\n')

def save(path, lines):
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))

def _tpl_idx(lines):
    for i, ln in enumerate(lines):
        if ln.strip() == '<script type="__bundler/template">':
            return i + 1
    raise RuntimeError('template script not found')

def _man_idx(lines):
    for i, ln in enumerate(lines):
        if ln.strip() == '<script type="__bundler/manifest">':
            return i + 1
    raise RuntimeError('manifest script not found')

def get_template(lines):
    return json.loads(lines[_tpl_idx(lines)].strip())

def dump_template(s):
    raw = json.dumps(s, ensure_ascii=False).replace('</', '<\\u002F')
    assert '\n' not in raw and '</' not in raw and json.loads(raw) == s, 'template encode invariant failed'
    return raw

def set_template(lines, s):
    lines[_tpl_idx(lines)] = dump_template(s)

# ---------------- 图片 / 资源 ----------------
def embed_image(lines, file_path, mime='image/jpeg', prefix='img'):
    """把图片追加进 manifest，返回可用作 <img src="..."> 的 uuid。jpg/png 用 compressed:false。"""
    b64 = base64.b64encode(open(file_path, 'rb').read()).decode('ascii')
    uid = prefix + '-' + uuid.uuid4().hex
    entry = '"%s":{"mime":"%s","compressed":false,"data":"%s"}' % (uid, mime, b64)
    mi = _man_idx(lines); mraw = lines[mi]; ms = mraw.rstrip()
    assert ms.endswith('}')
    lead = mraw[:len(mraw) - len(mraw.lstrip())]
    lines[mi] = lead + ms[:-1] + ',' + entry + '}'
    assert uid in json.loads(lines[mi].strip())
    return uid

def get_resource(lines, uid):
    """取出某 uuid 的解码字节（自动 gzip 解压 compressed:true，如内联的 React 运行时）。"""
    e = json.loads(lines[_man_idx(lines)].strip())[uid]
    raw = base64.b64decode(e['data'])
    return gzip.decompress(raw) if e.get('compressed') else raw

# ---------------- 离线内联 React（修 unpkg CDN 依赖）----------------
def inline_react(lines, react_umd_path, reactdom_umd_path):
    """把 react/react-dom UMD 作为内联 <script> 放到运行时脚本之前，使 deck 真离线。
    两个文件需是 react@18.3.1 / react-dom@18.3.1 的 UMD production；不得含字面 '</script'。"""
    s = get_template(lines)
    rt = re.search(r'<script src="[0-9a-f-]{30,}"></script>', s)
    assert rt, 'runtime <script src=UUID> not found'
    rc = open(react_umd_path, encoding='utf-8').read()
    rd = open(reactdom_umd_path, encoding='utf-8').read()
    for nm, c in [('react', rc), ('react-dom', rd)]:
        assert re.search(r'</script', c, re.I) is None, nm
    inline = ('<script>/* React UMD inlined for offline */\n' + rc + '\n</script>\n'
              '<script>/* ReactDOM UMD inlined for offline */\n' + rd + '\n</script>\n')
    s = s[:rt.start()] + inline + s[rt.start():]
    set_template(lines, s)

# ---------------- nav / chapters ----------------
def _nav_entries(s):
    ns = s.find('const nav = ['); ne = s.find('];', ns)
    ents = re.findall(r"\{ i:\d+, code:'((?:[^'\\]|\\.)*)', label:'((?:[^'\\]|\\.)*)' \}", s[ns:ne+2])
    return ns, ne, [c for c, l in ents], [l for c, l in ents]

def _write_nav(s, codes, lbls):
    ns = s.find('const nav = ['); ne = s.find('];', ns)
    body = "\n".join("      { i:%d, code:'%s', label:'%s' }," % (k, codes[k], lbls[k]) for k in range(len(codes)))
    return s[:ns] + "const nav = [\n" + body + "\n    ];" + s[ne+2:]

def bump_chapters(s, delta, after_start):
    """把 start > after_start 的所有 chapters[].start 加 delta（在某章内增删页时调用）。"""
    def repl(m):
        st = int(m.group(2))
        return m.group(1) + str(st + delta if st > after_start else st)
    return re.sub(r"(start:)(\d+)", repl, s)

# ---------------- 页块定位 ----------------
def _slide_bounds(s, label):
    i = s.find('<section data-label="%s"' % label)
    assert i > 0, label
    st = s.rfind('<div class="slide-fit"', 0, i)
    end = s.find('</div></div>', s.find('</section>', i)) + len('</div></div>')
    return st, end

# ---------------- 增 / 删 / 移 页（自动同步三处）----------------
SEP = '\n\n    '

def insert_page(s, new_block, before_label, nav_code, nav_label):
    """在 before_label 页之前插入 new_block。new_block 是完整 '<div class="slide-fit"...>...</div></div>'。
    自动：插 DOM、nav 在该页前插入并重编号、其后章节 start+1。
    章归属约定：插到某章首页之前 = 新页成为该章新首页（该章 start 不动）；
    插到章中/章尾页之前 = 新页属该章，下一章起各章 start+1。
    注意：必须在改动 DOM/nav 之前用 before 页的原索引定章——插入后 before 页索引 +1，
    若它原是章尾页，新索引会撞上下一章 start，导致下一章漏 +1。"""
    ns, ne, codes, lbls = _nav_entries(s)
    pos = lbls.index(before_label)
    starts = [int(m) for m in re.findall(r"start:(\d+)", s)]
    home = max([x for x in starts if x <= pos], default=0)  # before 页所属章（原索引）
    st, _ = _slide_bounds(s, before_label)
    assert s[st-len(SEP):st] == SEP
    s = s[:st-len(SEP)] + SEP + '    ' + new_block + s[st-len(SEP):]
    ns, ne, codes, lbls = _nav_entries(s)
    codes.insert(pos, nav_code); lbls.insert(pos, nav_label)
    s = _write_nav(s, codes, lbls)
    s = bump_chapters(s, +1, home)  # home 之后各章 +1
    return s

def delete_page(s, label):
    st, end = _slide_bounds(s, label)
    assert s[st-len(SEP):st] == SEP
    s = _bump_after_page(s, label, -1)
    s = s[:st-len(SEP)] + s[end:]
    ns, ne, codes, lbls = _nav_entries(s)
    pos = lbls.index(label); codes.pop(pos); lbls.pop(pos)
    s = _write_nav(s, codes, lbls)
    return s

def move_page(s, label, after_label):
    """把 label 页移到 after_label 页之后（同章内移动：章节 start 不变；只动 DOM + nav 顺序）。"""
    st, end = _slide_bounds(s, label)
    chunk = SEP + s[st:end]           # 含前置分隔符
    assert s[st-len(SEP):st] == SEP
    s = s[:st-len(SEP)] + s[end:]     # 先移除
    _, dst_end = _slide_bounds(s, after_label)
    s = s[:dst_end] + chunk + s[dst_end:]
    ns, ne, codes, lbls = _nav_entries(s)
    i = lbls.index(label); c, l = codes.pop(i), lbls.pop(i)
    j = lbls.index(after_label)
    codes.insert(j+1, c); lbls.insert(j+1, l)
    s = _write_nav(s, codes, lbls)
    return s

def _bump_after_page(s, ref_label, delta):
    """ref 页所在章之后的所有章 start ±delta（增删页时用）。靠 nav 位置定位章。"""
    # 计算 ref 页的 DOM 序号（= nav 索引），再找它落在哪个 chapter 区间，其后各章 start 调整
    _, _, codes, lbls = _nav_entries(s)
    # 重新解析当前 nav 顺序对 DOM 顺序：nav 已与 DOM 同步，ref_label 的 nav index 即 DOM index
    try:
        idx = lbls.index(ref_label)
    except ValueError:
        return s
    starts = [int(m) for m in re.findall(r"start:(\d+)", s)]
    # 该页所属章 = 最大的 start <= idx
    home = max([x for x in starts if x <= idx], default=0)
    return bump_chapters(s, delta, home)

# ---------------- 矩阵网格助手 ----------------
def grid(rows, red=None, cell=30, fs=15):
    red = red or set(); h = '<table style="border-collapse:collapse;border:1.5px solid #b0b0b6;">'
    for ri, row in enumerate(rows):
        h += '<tr>'
        for ci, v in enumerate(row):
            isr = (ri, ci) in red; col = '#d4001a' if isr else '#1a1a1c'; wt = '700' if isr else '400'
            h += ('<td style="width:%dpx;height:%dpx;border:1px solid #cfcfd4;text-align:center;'
                  'font-family:JetBrains Mono,monospace;font-size:%dpx;color:%s;font-weight:%s;padding:0;">%s</td>'
                  % (cell, cell, fs, col, wt, v))
        h += '</tr>'
    return h + '</table>'

# ---------------- 验证 ----------------
def verify(path):
    lines = load(path)
    s = get_template(lines)
    nslide = s.count('class="slide-fit"')
    nsec = s.count('<section data-label=')
    nums = [int(x) for x in re.findall(r'\{ i:(\d+),', s)]
    ok_seq = nums == list(range(len(nums)))
    print('slide-fit=%d  sections=%d  nav=%d  nav_seq_ok=%s' % (nslide, nsec, len(nums), ok_seq))
    print('chapters:', re.findall(r"name:'[^']+', start:\d+", s))
    assert ok_seq, 'nav i: not sequential — 三处同步没做全'
    return True

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        verify(sys.argv[1])
    else:
        print(__doc__)
