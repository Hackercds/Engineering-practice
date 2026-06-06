---
title: spec-001-todo-api
type: summary
created: 2026-06-07
updated: 2026-06-07
sources: [code/backend/SPEC-001-todo-api.md]
---

# spec-001-todo-api（摘要）

> SPEC-001 的可读摘要。源：[code/backend/SPEC-001-todo-api.md](../code/backend/SPEC-001-todo-api.md)

## 一句话目标

对外提供 Todo 的增 / 查 / 标记完成；内存存储，3 个端点，OpenAPI 契约导出。

## 范围

**必须有**：
- POST /todos（新建）
- GET  /todos（列表）
- POST /todos/{id}/done（标记完成，幂等）

**不做**：删除 / 编辑标题 / 分页 / 持久化 / 鉴权

## 数据模型

| 字段 | 类型 | 约束 |
|---|---|---|
| `id` | int | 服务端自增，从 1 开始 |
| `title` | str | 必填，去首尾空白后非空，1–100 字 |
| `done` | bool | 默认 `false` |

## 边界（5 条 → 5 条测试）

1. 空标题 `""` → 422
2. 仅空白 `"   "` → 422
3. 超长 101 字 → 422
4. id 不存在（如 999）→ 404
5. 重复标记完成 → 幂等 200

## 相关页

- [[todo-api]] — 实现
- [[Spec Driven Development]] — 方法论
- [[TDD]] — 8 条测试的来源
