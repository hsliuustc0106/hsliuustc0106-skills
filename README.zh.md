# Agentic Coding Skills

面向 Codex、Claude Code 和 Cursor 的可复用编码代理规则。

本仓库保留简洁的 skills 组织方式，并加入适用于 `vllm`、`vllm-omni`、`afd-plugin`、`vllm-omni-cookbook` 的项目规则。

## 主要文件

- `AGENTS.md`：共享规则源，Codex 优先读取。
- `CLAUDE.md`：Claude Code 的轻量入口，导入 `AGENTS.md`。
- `.cursor/rules/*.mdc`：Cursor 项目规则。
- `skills/*/SKILL.md`：通用和项目级技能。
- `skills/vllm-omni-deck/`：包含七种可复用示例版式、带品牌白色画布的八页
  空白 PowerPoint 模板、原始图表完整复用规则和类型化生成器的 vLLM-Omni
  演示技能。
- `skills/vllm-omni-review/`：仓库内置的 vLLM Omni review skill 和辅助脚本。

## 安装

```bash
git clone <this-repo-url> ~/.agentic-coding-rules
cd /path/to/project
~/.agentic-coding-rules/scripts/sync-project.sh --project vllm-omni --tools codex,claude,cursor
```

支持的项目：

- `vllm`
- `vllm-omni`
- `afd-plugin`
- `vllm-omni-cookbook`

同步脚本会安装规则引用的 skills、参考文档和辅助脚本。复制前检查全部目标
文件：内容相同则跳过，内容冲突则停止。请手动合并已有项目规则；仅在确定
要替换时使用 `--force`。符号链接和目录不会被替换。

辅助脚本回归测试无需联网，需要 Python 3.8+、Bash 和 `jq`：

```bash
python3 -m unittest discover -s tests -v
```

## vLLM-Omni 发布维护

使用 [update-vllm-omni-skills](skills/update-vllm-omni-skills/SKILL.md)：

```text
Use $update-vllm-omni-skills to refresh the skills for the latest stable release.
```

可以指定目标版本；需要提交 PR 时，在请求中明确说明。默认生成本地修改和
PR 文案。

每次正式发布后，按
[发布维护流程](skills/update-vllm-omni-skills/references/release-maintenance.md)
检查版本相关规则，并在
[覆盖记录](skills/update-vllm-omni-skills/references/release-status.md)
中保存上游 commit、证据、检查范围和未验证部分。初次 v0.28.0 检查仅覆盖
部分依赖、配置和测试规则，不代表完整运行时兼容性验证。

## 核心原则

1. 先理解，再编码。
2. 优先简单、局部、可维护的改动。
3. 只修改任务需要的内容。
4. 把任务转化为可验证目标。
5. 交付前运行相关检查，或说明为什么没有运行。

## License

MIT
