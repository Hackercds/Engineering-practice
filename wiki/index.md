# Wiki Index · 唯一目录

> **AI 必读导航。** 接入项目：先读 `CLAUDE.md` → 再读本文件 → 按需读相关页。
> 最后更新：2026-06-07 · 总页数：6

---

## 概念（Concepts · 方法论 / 规范 / 模式）

- [[Spec Driven Development]] — 把 spec 升级为可执行契约，AI 据此生成实现与测试
- [[Harness Engineering]] — 给 AI Coding Agent 装"缰绳"：约束 + 反馈 + 验证
- [[LLM Wiki Pattern]] — 让知识以复利方式积累（nashsu 范式）
- [[TDD]] — 测试先行的红→绿→重构循环

## 实体（Entities · 项目 / 服务 / 组件 / 工具）

- [[todo-api]] — SPEC-001 的 FastAPI 实现
- [[claude-code]] — Anthropic 的 agentic 编码工具
- [[fastapi]] — 本项目后端框架

## 摘要（Summaries · raw 资料的可读摘要）

- [[spec-001-todo-api]] — 待办 API 的 SDD 产物摘要

## 图（自动生成 · CI 渲染）

- `graphs/concepts.mmd` — 概念关系图
- `graphs/entities.mmd` — 实体关系图
- `graphs/full.mmd` — 全局图谱
- `graphs/spec-flow.mmd` — spec → 生产的端到端流程

---

## 跳读指引

| 我是 | 我想 | 看 |
|---|---|---|
| 新 AI agent | 30 秒接入 | [[LLM Wiki Pattern]] → [[Harness Engineering]] |
| 架构师 | 找设计依据 | [[Spec Driven Development]] + 原始 specs/ |
| 工程师 | 跑通后端 | [[todo-api]] → `code/backend/` |
| Claude 用户 | 知道怎么用 | 根 [[../CLAUDE.md]] |
| 团队 lead | 看 CI 怎么守 | [[../materials/07_CI门与发版策略]] |
