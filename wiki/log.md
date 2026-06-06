# Wiki Log

> Append-only。CI 用 `grep "^## \["` 解析。
> 格式：`## [YYYY-MM-DD] <op> | <name>`

---

## [2026-06-07] init | wiki skeleton
- 写入: [[Spec Driven Development]], [[Harness Engineering]], [[LLM Wiki Pattern]], [[TDD]]
- 写入: [[todo-api]], [[claude-code]], [[fastapi]]
- 写入: [[spec-001-todo-api]]
- 写入: `graphs/concepts.mmd`, `graphs/entities.mmd`, `graphs/full.mmd`, `graphs/spec-flow.mmd`
- 写入: `scripts/wiki/{ingest,lint,render_graph,mcp_server}.py`
- 写入: `.github/workflows/wiki-ci.yml`
- 摘要: 采用 [LLM-wiki实践](https://github.com/Hackercds/LLM-wiki-Practical)（极简：单 Schema + 平铺 + 4 个脚本）

## [2026-06-07] ingest | materials/01
- 源: `materials/01_spec模板.md`
- 写入: [[Spec Driven Development]]
- 更新: [[index]]

## [2026-06-07] ingest | materials/09
- 源: `materials/09_Harness工程化指南.md`
- 写入: [[Harness Engineering]]
- 更新: [[index]]

## [2026-06-07] ingest | llm-wiki.md
- 源: `nashsu/llm_wiki/llm-wiki.md`（核心理念）
- 写入: [[LLM Wiki Pattern]]
- 更新: [[index]]

## [2026-06-07] ingest | code/backend/SPEC-001
- 源: `code/backend/SPEC-001-todo-api.md`
- 写入: [[todo-api]], [[spec-001-todo-api]]
- 更新: [[index]]

## [2026-06-07] render-graph | initial
- 渲染: concepts.mmd, entities.mmd, full.mmd, spec-flow.mmd
- 状态: 4/4 OK
