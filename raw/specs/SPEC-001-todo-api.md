# SPEC-001 · 待办事项 API

> 原始规格文档（copy from code/backend/SPEC-001-todo-api.md）。
> 本文件作为 Wiki 的 raw 源——只读，AI 不直接修改。

---

## 0. 元信息

| 字段 | 值 |
|---|---|
| 编号 | SPEC-20260607-001 |
| 名称 | 待办事项 API（v1） |
| 版本 | v1.0 |
| 状态 | 已确认 → 实施中 |

## 1. 一句话目标

对外提供 Todo 的增 / 查 / 标记完成；内存存储，3 个端点，OpenAPI 契约导出。

## 2. 范围

**必须有**：POST /todos、GET /todos、POST /todos/{id}/done
**不做**：删除 / 编辑 / 分页 / 持久化 / 鉴权

## 3. 数据模型

| 字段 | 类型 | 约束 |
|---|---|---|
| id | int | 服务端自增 |
| title | str | 必填，去首尾空白后非空，1–100 字 |
| done | bool | 默认 false |

## 4. 端点

| 动作 | 成功 | 失败 |
|---|---|---|
| POST /todos | 201 + Todo | 422 |
| GET /todos | 200 + Todo[] | — |
| POST /todos/{id}/done | 200 + Todo | 404 |

## 5. 边界（5 条 → 5 条测试）

- 空 / 仅空白 / 超长 → 422
- id 不存在 → 404
- 重复标记完成 → 幂等 200

## 6. 实现位置

- Spec: `code/backend/SPEC-001-todo-api.md`
- 实现: `code/backend/app/__init__.py`
- 测试: `code/backend/tests/test_todo_api.py`（8 条）
- 契约: `code/backend/openapi.yaml`
