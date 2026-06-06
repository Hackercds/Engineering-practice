# 前端（从契约生成 · 企业级范例）

> **页面不预写——从前端的契约（typed client + OpenAPI）现场生成。** 这里只说企业级做法。

---

## 怎么做

```
后端跑起来 → /openapi.json
  ↓
CI 自动：typed client 生成 → PR → 合并
  ↓
前端用 typed client 调 API：
  - 端点 / 字段不存在 → 编译期报错
  - 校验（min/maxLength）→ 表单约束
  ↓
mock server 同源启动（prism）→ 后端没好前端也能跑
```

---

## 实际例子（待办 API）

| UI 里的东西 | 来自契约的哪一项 |
|---|---|
| 只调 `/todos`、`/todos/{id}/done` | 契约的 `paths` |
| 新建只发 `{ title }` | `TodoCreate` 只有 `title` |
| 标题输入 `maxlength=100` | `title` 的 `maxLength: 100` |
| 标题非空才允许提交 | `title` 的 `minLength: 1` |
| 标记完成按钮存在 | `paths` 里有 `/todos/{id}/done` |
| 404 提示"待办不存在" | `404` 的 `description` |
| 422 提示"标题不合法" | `422` 的 schema + `description` |

> AI 生成的 UI——**全是从契约继承的**，它没法瞎编一个后端不存在的字段。

---

## 进阶：把约束落到代码级别

| 形态 | 工具 | 作用 |
|---|---|---|
| OpenAPI → typed client（TS） | `openapi-typescript` / `orval` | 字段不存在 → 编译错误 |
| OpenAPI → mock server | `prism` / `mockoon` / `msw` | 后端没好前端也能跑 |
| OpenAPI → 服务端 stub | `openapi-generator` | 后端并行开发 |
| 契约 diff 进 CI | `oasdiff` / `swagger-cli` | 改 API 时前端 PR 立刻见红 |
| 契约 lint 进 CI | `spectral` | 字段命名/描述/example 齐全 |

---

## 题眼

> **API 定义不是文档，是上一层的产出变成下一层的规格。**
> **确定性逐层传导**：spec 决定测试，测试决定实现，实现导出契约，契约约束前端，前端变化驱动契约演进。

进阶方法卡见 [../../materials/03_API契约约束前端_方法卡.md](../../materials/03_API契约约束前端_方法卡.md)。
