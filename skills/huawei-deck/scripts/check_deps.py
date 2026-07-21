#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""依赖体检 doctor —— 检查本 skill 的运行依赖，缺失即按需自动安装。

覆盖：
  · 本 skill 运行时：Node ≥ 18、playwright-core（三级查找）、python-pptx、pymupdf、Chrome、soffice(LibreOffice)

行为（默认）：能自动装的（pip / npx / npm）先打印命令再装；装不了的（Node/Chrome/soffice）给安装提示。
  --check-only  只体检并报告，不改动环境。

退出码契约（与 verify 三件套一致）：0 全部就绪 / 1 仍有缺失（含手动依赖或自动安装失败）/ 2 工具或参数错误。

用法：
  python3 scripts/check_deps.py              # 体检 + 自动安装可装项
  python3 scripts/check_deps.py --check-only # 仅体检报告
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OPENCLAW_PW = "/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core/index.js"

# 输出小工具（TTY 上色，非 TTY 纯文本）
_C = sys.stdout.isatty()
def _c(s, code): return f"\033[{code}m{s}\033[0m" if _C else s
def ok(s):   return _c(s, "32")   # 绿
def bad(s):  return _c(s, "31")   # 红
def warn(s): return _c(s, "33")   # 黄
def dim(s):  return _c(s, "2")


def run(cmd, **kw):
    """跑命令，返回 CompletedProcess；找不到可执行文件时返回 rc=127。"""
    try:
        return subprocess.run(cmd, **kw)
    except FileNotFoundError:
        cp = subprocess.CompletedProcess(cmd, 127, "", "")
        return cp


# ---- 各依赖的探测函数：返回 (present: bool, detail: str) ----

def probe_pymod(mod):
    def _p():
        cp = run([sys.executable, "-c", f"import {mod}"],
                 capture_output=True, text=True)
        return cp.returncode == 0, f"import {mod}"
    return _p

def probe_node():
    cp = run(["node", "--version"], capture_output=True, text=True)
    if cp.returncode != 0:
        return False, "未安装 node"
    v = (cp.stdout or "").strip()
    try:
        major = int(v.lstrip("v").split(".")[0])
    except ValueError:
        return False, f"无法解析版本 {v!r}"
    return major >= 18, f"{v}（需 ≥ 18）"

def probe_playwright():
    # 三级查找，与 scripts/verify/*.mjs 口径一致
    env = os.environ.get("PLAYWRIGHT_CORE")
    if env and Path(env).is_file():
        return True, f"PLAYWRIGHT_CORE={env}"
    cp = run(["node", "-e", "require.resolve('playwright-core')"],
             cwd=str(REPO), capture_output=True, text=True)
    if cp.returncode == 0:
        return True, "require.resolve('playwright-core')"
    if Path(OPENCLAW_PW).is_file():
        return True, "openclaw 内置"
    return False, "三级查找均未命中"

def probe_chrome():
    if sys.platform == "darwin":
        for p in ("/Applications/Google Chrome.app",
                  str(Path.home() / "Applications/Google Chrome.app")):
            if Path(p).exists():
                return True, p
    for exe in ("google-chrome", "google-chrome-stable", "chromium", "chrome"):
        w = shutil.which(exe)
        if w:
            return True, w
    return False, "未找到 Google Chrome"

def probe_which(name):
    def _p():
        w = shutil.which(name)
        return (w is not None), (w or f"未找到 {name}")
    return _p


# ---- 依赖清单 ----
# install: 可自动安装时给命令（list）；否则 None
# hint:    手动安装提示
# optional: True 时缺失不计入失败退出码
def pip(*pkgs):
    return [sys.executable, "-m", "pip", "install", *pkgs]

CHECKS = [
    dict(key="node", label="Node.js", why="verify 三件套 / html2pptx",
         probe=probe_node, install=None,
         hint="安装 Node ≥ 18（nodejs.org 或 brew install node）"),
    dict(key="playwright-core", label="playwright-core", why="截图 / 溢出检测 / 逐拍",
         probe=probe_playwright, install=["npm", "i", "playwright-core"],
         install_cwd=str(REPO),
         hint="在仓库根 npm i playwright-core，或设 PLAYWRIGHT_CORE 指向其 index.js"),
    dict(key="chrome", label="Google Chrome", why="playwright channel:chrome",
         probe=probe_chrome, install=None,
         hint="安装 Google Chrome（google.com/chrome）"),
    dict(key="python-pptx", label="python-pptx", why="HTML → PPTX 导出",
         probe=probe_pymod("pptx"), install=pip("python-pptx")),
    dict(key="pymupdf", label="pymupdf", why="解析 pptx/pdf 参考素材",
         probe=probe_pymod("fitz"), install=pip("pymupdf")),
    dict(key="soffice", label="LibreOffice(soffice)", why="pptx → pdf 转换",
         probe=probe_which("soffice"), install=None,
         hint="安装 LibreOffice（libreoffice.org 或 brew install --cask libreoffice）"),
]


def do_probe(chk):
    present, detail = chk["probe"]()
    return present, detail


def main():
    ap = argparse.ArgumentParser(description="huawei-deck 依赖体检")
    ap.add_argument("--check-only", action="store_true",
                    help="只体检并报告，不安装任何东西")
    args = ap.parse_args()

    print(dim(f"依赖体检 · {REPO}"))
    missing = []       # (chk, detail) —— 首轮缺失
    for chk in CHECKS:
        present, detail = do_probe(chk)
        tag = "（可选）" if chk.get("optional") else ""
        if present:
            print(f"  {ok('✓')} {chk['label']}{tag}  {dim(detail)}")
        else:
            print(f"  {bad('✗')} {chk['label']}{tag}  {dim(chk['why'])} — {detail}")
            missing.append(chk)

    if not missing:
        print(ok("\n全部依赖就绪。"))
        return 0

    # 处理缺失项
    still = []         # 处理后仍缺失
    print()
    for chk in missing:
        auto = chk.get("install")
        if auto is None or args.check_only:
            if args.check_only and auto is not None:
                print(f"  {warn('⬇')} {chk['label']}：可自动安装 → {dim(' '.join(auto))}（--check-only 未执行）")
            else:
                print(f"  {warn('⚠')} {chk['label']}：需手动安装 → {chk.get('hint','')}")
            still.append(chk)
            continue
        # 先打印再装
        print(f"  {warn('⬇')} 安装 {chk['label']} → 执行: {dim(' '.join(auto))}")
        cp = run(auto, cwd=chk.get("install_cwd"))
        if cp.returncode == 127:
            tool = auto[0]
            print(f"    {bad('✗')} 找不到 {tool}，无法自动安装。手动：{chk.get('hint','')}")
            still.append(chk)
            continue
        # 复检
        present, detail = do_probe(chk)
        if present:
            print(f"    {ok('✓')} {chk['label']} 安装完成  {dim(detail)}")
        else:
            print(f"    {bad('✗')} {chk['label']} 安装后仍未就绪（rc={cp.returncode}）。手动：{chk.get('hint','')}")
            still.append(chk)

    # 退出码：非可选项仍缺失 → 1
    hard = [c for c in still if not c.get("optional")]
    print()
    if hard:
        print(bad(f"仍有 {len(hard)} 项依赖缺失：") + " " + "、".join(c["label"] for c in hard))
        return 1
    if still:
        print(warn("可选依赖缺失（不影响核心功能）：") + " " + "、".join(c["label"] for c in still))
    print(ok("核心依赖已就绪。"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
