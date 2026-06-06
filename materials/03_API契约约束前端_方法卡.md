# 方法卡：用 API 契约约束前端（企业级版）

> **题眼：API 定义不是文档，是上一层的产出变成下一层的规格。**
>
> **本版本升级**：在原方法卡基础上增加 **契约治理 / 契约 diff 进 CI / 双端 mock / 分层契约**，让它成为企业级契约治理的指南。

---

## 1. 链路（一图流）

```
后端（Spec → TDD 生成）
   └─▶ 自动产出 OpenAPI 契约（/openapi.json）
          ├─ paths        端点：前端只能调这些
          ├─ schemas      请求/响应字段与类型：前端不能编不存在的字段
          └─ min/maxLength / enum / pattern：前端校验直接继承
   └─▶ 把契约喂给 AI 生成 UI，约束自动落到代码
   └─▶ typed client（自动生成）+ mock server（自动起）
   └─▶ 契约 diff 进 CI：字段改了，前端 PR 立刻见红
```

---

## 2. 怎么做（4 步）

1. **后端跑起来**，拿到 `openapi.json`（**单一真相源**）。
2. **提示 AI**：
   > 「这是后端的 OpenAPI 契约，按它生成 UI，端点 / 字段 / 校验以契约为准，**不要自造后端没有的字段**。」
3. **自动生成 typed client + mock**：
   - TS：`openapi-typescript` / `orval` / `openapi-generator`
   - Python：`openapi-python-client` / `fastapi-code-generator`
4. **契约 diff 进 CI**：`oasdiff` / `swagger-cli` ——改了契约 PR 立刻见红。

---

## 3. 契约分层（企业级必备）

> 契约**不能一把抓**——分层才能管好。

| 层级 | 谁看 | 稳定性 | 演进规则 |
|---|---|---|---|
| **Public API** | 外部客户、第三方 | 高 | 任何破坏性变更需 major 版本 + changelog |
| **Internal API** | 内部多端 | 中 | 走 PR + 契约 diff，约定弃用周期 |
| **Private** | 单端内部 | 低 | 可随时改，但仍走契约 diff |

> **前端永远只看"它该看的那层"**——别把 internal/private 暴露给前端。

---

## 4. 契约治理（4 个治理点）

| 治理点 | 工具 / 做法 | 价值 |
|---|---|---|
| **Lint** | Spectral（OpenAPI lint） | 字段命名、描述、example 齐全 |
| **Diff** | `oasdiff` / `swagger-cli` | 改了契约 PR 见红，跨端协同 |
| **生成** | `openapi-generator` / `orval` | typed client / server stub / doc |
| **Mock** | `prism` / `mockoon` / `msw` | 后端没好前端也能跑；联调时只剩"通不通" |

> **契约也要进版本控制**——契约文件 = 代码。一改 PR，diff 必查。

---

## 5. 实际例子（待办 API）

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

## 6. 进阶：把约束落到代码级别

| 形态 | 工具 | 作用 |
|---|---|---|
| 手写 UI + 读契约校验 | 任何 AI 工具 | 起步快，约束靠人盯 |
| OpenAPI → typed client（TS / Python） | `openapi-typescript` / `orval` / `fastapi-code-generator` | 字段不存在的编译错误 |
| OpenAPI → mock server | `prism` / `mockoon` | 后端没好前端也能跑 |
| OpenAPI → 服务端 stub | `openapi-generator` | 后端并行开发，契约先行 |
| 契约 diff 进 CI | `oasdiff` / `swagger-cli` | 改 API 时下游立刻见红 |
| 契约 lint 进 CI | Spectral | 字段命名/描述/示例齐全 |
| 契约可视化 | Redoc / Stoplight | 给人看（但不是真相源） |

---

## 7. 常见坑

| 坑 | 后果 | 改成什么 |
|---|---|---|
| 契约老旧 | 前端还在用旧的 | 契约随代码进版本控制 + CI 校验 |
| 契约一把抓 | 暴露 internal 实现细节 | 契约分层 |
| 把契约当文档 | 失去"机器可读"价值 | 契约 = 机器契约，docs = 派生物 |
| 没有 changelog | 客户不知何时变 | SemVer + 自动 changelog |
| mock 与真服务不一致 | 上线才见红 | mock 与真服务同源（同 OpenAPI 生成） |
| 客户端硬编码 URL | 改域名要改 N 处 | typed client 集中管理 baseURL |

---

## 8. 一句话收束

> **确定性逐层传导**：spec 决定测试，测试决定实现，**实现导出契约，契约约束前端，前端变化驱动契约演进**。
> AI 自由发挥的空间被契约一层层夹紧——这才是"前后端协同"的企业级解法。
