# SPEC-001 · 待办事项 API（成品 Spec 范例）

> **这份 Spec 是企业级 vibe coding 的"成品范例"**——展示 spec 怎么从"模板"长成"可执行契约"。

---

## 0. 元信息

| 字段 | 值 |
|---|---|
| 编号 | SPEC-20260607-001 |
| 名称 | 待办事项 API（v1） |
| 版本 | v1.0（已确认） |
| 负责人 | @team-platform |
| 关联 issue | #001 |
| 关联 ADR | docs/adr/0007-todo-stack.md |
| 状态 | 已确认 → 实施中 |

---

## 1. 一句话目标

对外提供 Todo 的增 / 查 / 标记完成；内存存储，3 个端点，OpenAPI 契约导出。

---

## 2. 范围

### 2.1 必须有
- POST /todos（新建）
- GET  /todos（列表）
- POST /todos/{id}/done（标记完成，幂等）
- OpenAPI 契约自动导出 → typed client

### 2.2 明确不做
- 不做删除、不做编辑标题、不做分页、不做持久化、不做鉴权、不做限流、不做审计

---

## 3. 数据模型

| 字段 | 类型 | 约束 | 示例 |
|---|---|---|---|
| `id`   | int  | 服务端自增，从 1 开始，只读 | 1 |
| `title`| str  | 必填，去除首尾空白后非空，长度 1–100 | "买菜" |
| `done` | bool | 默认 `false` | false |

---

## 4. 端点

| 动作 | 输入 | 成功返回 | 失败（状态码 + 触发条件） |
|---|---|---|---|
| `POST /todos` | `{title: str}` | `201` + 完整 Todo | `422` 空/仅空白/超长 |
| `GET /todos` | — | `200` + `Todo[]`（按 `id` 升序） | — |
| `POST /todos/{id}/done` | — | `200` + 更新后 Todo（`done=true`） | `404` id 不存在 |

---

## 5. 边界（每条对应 1 条测试）

- 空标题 `""` → 422
- 仅空白标题 `"   "` → 422（去空白后为空）
- 超长标题（101 字）→ 422
- 标记不存在的 id（如 999）→ 404
- 重复标记完成：幂等，200，仍 `done=true`

---

## 6. 验收标准（DoD）

- [ ] 8 条测试全绿（边界 5 + happy path 3）
- [ ] 故意改坏自检通过（至少 1 条测试变红）
- [ ] `openapi.yaml` 已生成，spectral lint 过
- [ ] typed client 已生成（给前端）
- [ ] 覆盖率 ≥ 80%
- [ ] SAST / SCA / secrets / lint / typecheck 全过
- [ ] README / ADR / Changelog 更新

---

## 7. 实现计划

| 顺序 | 任务 | 依赖 | 验收 |
|---|---|---|---|
| 1 | 脚手架（uv + FastAPI + pytest + ruff） | — | `uvicorn` 起得来 |
| 2 | 数据模型 + 校验（Pydantic） | 1 | 模型单测过 |
| 3 | POST /todos | 2 | happy + 3 边界 |
| 4 | GET /todos | 2 | happy |
| 5 | POST /todos/{id}/done | 2 | happy + 1 边界 |
| 6 | OpenAPI 导出 + spectral lint | 3-5 | 契约无错 |
| 7 | typed client 生成 | 6 | 前端能 import |
| 8 | 审查 + 合并 | 1-7 | 12 门全过 |

---

## 8. 任务清单

- [ ] T1: 脚手架
- [ ] T2: 数据模型
- [ ] T3: POST /todos
- [ ] T4: GET  /todos
- [ ] T5: POST /todos/{id}/done
- [ ] T6: openapi.yaml
- [ ] T7: typed client
- [ ] T8: 审查 + 合并

---

## 9. 非功能性需求

| 维度 | 指标 |
|---|---|
| 性能 | 列表 P95 < 50ms（内存） |
| 错误 | 5xx 率 < 0.1% |
| 日志 | JSON，含 `request_id` |
| 指标 | `todo_create_total` / `todo_done_total` / `request_duration_seconds` |
