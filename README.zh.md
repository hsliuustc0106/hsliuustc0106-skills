# Agentic Coding Skills

面向 Codex、Claude Code 和 Cursor 的可复用编码代理规则。

本仓库保留简洁的 skills 组织方式，并加入适用于 `vllm`、`vllm-omni`、`afd-plugin`、`vllm-omni-cookbook` 的项目规则。

## 主要文件

- `AGENTS.md`：共享规则源，Codex 优先读取。
- `CLAUDE.md`：Claude Code 的轻量入口，导入 `AGENTS.md`。
- `.cursor/rules/*.mdc`：Cursor 项目规则。
- `skills/*/SKILL.md`：通用和项目级技能。
- [skills/repository-maintenance/](skills/repository-maintenance/SKILL.md)：适用于
  单个或多个仓库的统一维护 SOP，并遵循各项目自己的规则。
- [skills/formal-slides/](skills/formal-slides/SKILL.md)：基于十种内置版式创建
  可编辑演示文稿；现有模板不适用时，调整或新增同风格模板。
- `skills/ncu-report-skill/`：Nsight Compute CUDA 性能分析、瓶颈诊断与优化报告，
  包含 B200/sm_100 参考文档、辅助脚本和上游 MIT 许可证。
  固定版本与运行要求见 [来源说明](external/ncu-report-skill.md)。
- `skills/setup-server-project/`：在已有服务器账号中创建 `repos/`、`models/`、
  `llm_wiki/` 和 `envs/` 目录、克隆仓库、
  安装隔离的项目依赖并验证环境，不扩展为账号创建或整机管理。
- `skills/vllm-omni-deck/`：包含七种可复用示例版式、带品牌白色画布的八页
  空白 PowerPoint 模板、原始图表完整复用规则和类型化生成器的 vLLM-Omni
  演示技能。
- [项目审查覆盖内容](skills/repository-maintenance/references/project-reviews.md)：
  统一 SOP 使用的项目特有审查上下文和每日队列规则。

## 安装

```bash
git clone <this-repo-url> ~/.agentic-coding-rules
cd /path/to/project
~/.agentic-coding-rules/scripts/sync-project.sh --project generic --tools codex,claude,cursor
```

`generic` 安装通用编码和维护技能、项目审查覆盖内容、每日队列选择器及规范
审查来源加载器；项目资源不再是独立技能。若已启用插件，也可以直接调用 `$repository-maintenance`，
无需逐仓库同步。例如，请它检查指定仓库的开放 PR 和 CI，并分别报告后续行动。
一般健康检查覆盖文档体系、CI 分层、贡献及审查合并流程、issue/PR 标签体系；
针对性任务只检查相关部分，不假设各项目使用相同的 CI 等级或标签规则。

也可以将通用技能安装一次，供当前用户的所有 Codex 仓库使用：

```bash
~/.agentic-coding-rules/scripts/sync-project.sh --project generic --tools skills --target ~/.codex
```

如使用其他 Codex home，请调整目标路径。更新已安装文件时，确认需要替换后
重新运行并加上 `--force`；本地 `review-sources.local.json` 不会被复制或覆盖。

项目专用配置仍然可用：

- `vllm`
- `vllm-omni`
- `afd-plugin`
- `vllm-omni-cookbook`
- `nanodot`
- `router`
- `sciencediscovery`
- `system1-omni`

统一 SOP 会遵循项目自己的审查规则；已配置的个人每日简报使用通用技能内对应的
项目覆盖内容和选择规则。必要的规范审查来源不可用时，会报告阻塞，不会静默
替换成通用审查。

通用开发指导和显式启用的标签/新提交队列规则集中维护；项目开发和审查技能
入口已整合。项目覆盖内容和 Cursor 规则保留项目特有的来源、证据和策略差异。
新增仓库先使用通用 SOP，只有确实需要项目特有指导时才新增覆盖内容。
对已证实、可能重复的问题，优先考虑合适的代码约束、静态检查或回归测试，
并验证错误与正确情况；根据改动选择运行时证据，区分实际结果和配置中的检查。

同步脚本会安装规则引用的 skills、参考文档和辅助脚本。复制前检查全部目标
文件：内容相同则跳过，内容冲突则停止。请手动合并已有项目规则；仅在确定
要替换时使用 `--force`。符号链接和目录不会被替换。
同步不会自动删除之前安装的旧技能，请检查本地改动后再移除过期副本。
使用旧项目审查技能名或选择器路径的命令和自动化，需要改用
`$repository-maintenance` 及已安装技能中对应的
`references/projects/<alias>/scripts/select_daily.py`；本次迁移不会修改自动化。

辅助脚本回归测试无需联网，需要 Python 3.8+、Bash 和 `jq`：

```bash
python3 -m unittest discover -s tests -v
```

## 核心原则

1. 先理解，再编码。
2. 优先简单、局部、可维护的改动。
3. 只修改任务需要的内容。
4. 把任务转化为可验证目标。
5. 交付前运行相关检查，或说明为什么没有运行。

## License

MIT

## 仓库维护的审查技能

项目仓库是审查规则的唯一维护源；统一技能加载对应的项目覆盖内容与规范来源。
加载器校验本地仓库 origin，并返回实际读取的提交、内容哈希和工作树状态。
它不会联网更新源码；源码是否最新须另行核实。尚未合并的技能需显式使用其
草稿分支，缺失时明确报告，不以通用审查代替。

入口见 [repository-review-source](skills/repository-review-source/SKILL.md)。
私有项目通过未跟踪的本地 JSON 配置加载，配置与私有内容不提交到公共仓库。

没有本地 checkout 时，可通过已授权的 GitHub connector 固定源码提交，并读取规范技能及需要的引用文件；记录实际读取文件的 Git blob 标识，不需要复制或维护另一份规则。
