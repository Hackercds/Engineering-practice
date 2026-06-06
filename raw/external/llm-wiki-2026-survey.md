# 外部资料：LLM Wiki 范式

> 收藏的外部资料摘要。AI 可读，可派生 wiki 页。

---

## 1. Karpathy 原始 Gist

> LLM Wiki = 让 LLM 持续把零散资料**编译**为带双向链接的结构化知识。
> 关键："the wiki is a persistent, compounding artifact"。

- 3 层：raw / wiki / schema
- 5 操作：ingest / query / lint / render-graph / audit
- 2 关键文件：`index.md`（目录）+ `log.md`（时间线，可解析前缀）

## 2. nashsu 实践仓库（[github.com/nashsu/llm_wiki](https://github.com/nashsu/llm_wiki)）

核心理念文档 `llm-wiki.md` 强调：
- **不要建子目录**——平铺所有 wiki 页，frontmatter `type` 字段区分
- **不要复杂 skill 系统**——4 个 Python 脚本足够
- **不要前端**——Obsidian 是 UI
- **log 用可解析前缀** `## [YYYY-MM-DD] op | name`——`grep` 友好

本仓库采用其极简范式。

## 3. 网易有道"LLM Wiki 技能套件"（2026-04）

> "5 分钟让知识活起来"——主打零基础上手，呼应 Karpathy 理念。
> 印证：从静态存档到 AI 动态交互是 2026 知识管理趋势。

## 4. 谷歌 Code Wiki（2026-01）

> Tree-sitter 对代码做 AST 分析 → 自动生成结构化文档。
> 与本仓库方向互补：LLM Wiki 管"项目知识层"，Code Wiki 管"代码结构层"。

## 5. MCP（Model Context Protocol）

Anthropic 2025 推出，2026 成 AI 工具集成事实标准。
- MCP server 把 wiki 暴露为 Resources → Claude Desktop / Cursor / 任何 agent 都能消费
- 本仓库 `scripts/wiki/mcp_server.py` 是最简实现（< 80 行）

## 派生 wiki 页

- [[LLM Wiki Pattern]] — 综合以上
- [[Harness Engineering]] — MCP + Wiki 在 Harness 中的位置
