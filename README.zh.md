# Agentic Coding Skills

面向 Codex、Claude Code 和 Cursor 的可复用编码代理规则。

本仓库保留简洁的 skills 组织方式，并加入适用于 `vllm`、`vllm-omni`、`afd-plugin`、`vllm-omni-cookbook` 的项目规则。

## 主要文件

- `AGENTS.md`：共享规则源，Codex 优先读取。
- `CLAUDE.md`：Claude Code 的轻量入口，导入 `AGENTS.md`。
- `.cursor/rules/*.mdc`：Cursor 项目规则。
- `skills/*/SKILL.md`：通用和项目级技能。
- `external/vllm-omni-review.md`：外部 vLLM Omni review skill 的说明，不硬编码个人账号。

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

## 核心原则

1. 先理解，再编码。
2. 优先简单、局部、可维护的改动。
3. 只修改任务需要的内容。
4. 把任务转化为可验证目标。
5. 交付前运行相关检查，或说明为什么没有运行。

## License

MIT

