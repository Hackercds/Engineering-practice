# AGENTS.md · 工程宪法（通用 · 跨工具）

> **让任何 AI 编码工具（Claude Code / Codex / Cursor / Aider / Junie / Devin / Continue ……）都遵守同一份"工程口味"。**
> 纯文本、和框架无关，沉淀一次、处处生效。
>
> ## 为什么存在 / 与 CLAUDE.md 的关系
>
> - **`AGENTS.md`**（本文件）= **通用工程规则**（命名/目录/安全/测试/审査/AgentOps……），跨工具生效。
> - **[`CLAUDE.md`](CLAUDE.md)** = Claude Code 专属使用习惯（plan mode / MCP / 子代理 / 上下文管理……），只 Claude 读。
> - **通用规则改本文件**；**Claude 偏好改 CLAUDE.md**。**不要重复**。
> - 不冲突：AGENTS.md 是"工程宪法"（与工具无关），CLAUDE.md 是"Claude 使用手册"（与工具绑定）。
> - 改一处 AGENTS.md → 任何工具都生效，**这是可移植性的最小成本**。

---

## 0. 元信息

| 字段 | 值 |
|---|---|
| 技术栈 | <Python 3.10 + FastAPI 0.110 + Pydantic v2 / TypeScript 5.x + Next.js 14 / Go 1.22 / ……> |
| 包管理器 | <uv / pnpm / go mod / ……> |
| 部署目标 | <Docker / K8s / Serverless / VM> |
| 维护者 | <@team-platform> |
| 最后更新 | YYYY-MM-DD |

---

## 1. 命名

- 文件 / 目录：<snake_case / kebab-case>
- 函数：动词开头；布尔量用 `is_/has_/can_` 前缀
- 常量：大写下划线；类名 PascalCase
- 提交信息：Conventional Commits（feat/fix/docs/...）

## 2. 目录

- 业务逻辑：<app/ / src/>
- 测试：<tests/ / __tests__/>，镜像业务结构
- Spec：<docs/spec/>，**不进源码树**
- 生成的代码（typed client / mock）：<gen/>，加 `.gitignore` 行级注解

## 3. 写代码的口味

- 先 spec、再测试、再实现；一个改动一个小提交
- 公共函数要有类型签名；副作用写在名字里（`save_*` / `send_*` / `delete_*`）
- 错误抛明确异常，不静默吞掉；日志带上下文（who/when/id/request_id）
- 不可变优先；可变状态集中管理（避免散落全局变量）

## 4. 安全 / 合规

- **不引入未在 requirements 里的新依赖**（先问）
- **不进 secrets / API key** 到代码或日志——用 secret manager
- SQL 参数化；用户输入校验；输出转义
- **不可逆操作**（删数据 / 动钱 / 对外发布 / 改线上配置）**必须留给人确认**
- PII / GDPR：按 [materials/07](materials/07_CI门与发版策略.md) 走

## 5. 禁止

- 不为通过类型检查加无意义抽象
- 不把失败测试注释掉"通过"
- 不在 commit / PR 信息里编造未发生的事
- 不绕过 CI 硬关（force push to main / 关闭 required check）
- 不用 `any`（TS）/ 不 catch 所有异常后只 print

## 6. 测试

- 改了行为就更新 / 补测试
- 一个端点一个 TDD 循环
- 故意改坏一处实现 → 对应测试必须立刻变红
- 覆盖率门槛 80%（降覆盖需 PR 显式说明）

## 7. 契约

- 后端实现必须导出 OpenAPI；前端 typed client 必须从 OpenAPI 生成
- 改契约 = 改 spec = 改测试 + 改 changelog（SemVer）
- 契约 diff 进 CI（[03](materials/03_API契约约束前端_方法卡.md)）

## 8. 可观测 + AgentOps

- 关键路径必须有 metric + 结构化 log + trace
- agent 改代码必须在 PR body 标 `agent-assisted` + run_id
- 不可逆操作必须有人确认（见 §4）
- 详见 [08](materials/08_AgentOps_可观测与回滚.md)

## 9. 审查

- 第一关：AI 自审 prompt（[06](materials/06_审查双关_prompt与checklist.md)）
- 第二关：人按 checklist 批
- CI 硬关：测试 / 契约 / SAST / SCA / secrets（[07](materials/07_CI门与发版策略.md)）

## 10. 演进

- 规则被违反 3 次以上 → 写进 AGENTS.md
- 规则 > 20 条 → 拆 `<lang>/AGENTS.md` / `<module>/AGENTS.md`
- 跑偏一次补一条，半年后长成团队真正的口味

---

## 附：多文件拆分（企业级项目）

```
project/
├── AGENTS.md                  ← 总纲（本文件，5-8 条）
├── backend/AGENTS.md          ← 后端专属（语言/框架/部署）
├── frontend/AGENTS.md         ← 前端专属（组件/状态/样式）
├── infra/AGENTS.md            ← IaC 专属（Terraform/Helm/K8s）
└── docs/
    ├── adr/                   ← 架构决策记录
    └── runbooks/              ← 操作手册
```

> **进入子目录时，工具会优先读最近的 AGENTS.md，再读父级**——这是天然的"作用域继承"。
