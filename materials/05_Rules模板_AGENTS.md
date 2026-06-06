# Rules 模板（`AGENTS.md` / `CLAUDE.md` · 企业级版）

> **让 AI 不必每次从零理解你的项目。** Rules 管"约束"——让任何工具的产出都符合本工程的口味。
> 纯文本、和框架无关，沉淀一次、处处生效。
>
> **本版本升级**：从"项目级 Rules"升级为**企业级 Rules 体系**——包含工程宪法、安全/合规、可观测、AgentOps 约定，并配套子目录拆分建议。

---

## 1. 这个模板怎么用

1. 复制整份到项目根，文件名：
   - `AGENTS.md`（跨工具：Codex / Cursor / Aider / Junie / CC）
   - `CLAUDE.md`（Claude Code 原厂识别）
   - `.cursorrules`（Cursor 旧版识别，新版也吃 `AGENTS.md`）
   - 同一份内容可复制到多个文件名，工具按优先级读取。
2. **5–8 条起步**，别一上来写满。每次 AI 跑偏一次，回来补一条"禁止/必须"。
3. **拆子目录**（超过 20 条时）：`AGENTS.md` 留总纲，`<lang>/AGENTS.md` / `<module>/AGENTS.md` 放细则。
4. Rules **跨工具生效**——换工具不丢口味，这是企业级知识沉淀的最小单元。

---

## 2. 模板（直接复制后改占位符）

```markdown
# <项目名> · Agent Rules（工程宪法）

> 项目级"工程口味"。AI 必须遵守；违反要主动指出并改正。
> 本文件跨工具生效（Claude Code / Codex / Cursor / Junie …）。

## 0. 元信息
- 技术栈：<语言 / 框架 / 运行时版本>
- 包管理器：<npm / pnpm / uv / poetry / go mod>
- 部署目标：<容器 / serverless / VM>
- 最后更新：YYYY-MM-DD
- 维护者：<团队 / 人>

## 1. 命名
- 文件 / 目录：<你的约定，如 snake_case / kebab-case>
- 函数：动词开头；布尔量用 `is_/has_/can_` 前缀
- 常量：大写下划线；类名 PascalCase
- 提交信息：Conventional Commits（feat/fix/docs/...）

## 2. 目录
- 业务逻辑放 <where>；测试放 <where>，文件名 `test_*.py` / `*.spec.ts`
- 不在 <where> 放 <what>（防止 AI 把测试 / 临时脚本 / 资源混进源码树）
- 生成的代码（typed client / mock）放 `gen/` 并加 .gitignore 行级注解

## 3. 写代码的口味
- **节奏**：先 spec、再测试、再实现；一个改动一个小提交
- 公共函数要有类型签名；副作用要写在名字里（`save_*` / `send_*` / `delete_*`）
- 错误要抛明确异常，不静默吞掉；日志要带上下文（who/when/id/correlation_id）
- 不可变优先；可变状态集中管理（避免散落全局变量）

## 4. 安全 / 合规
- 不引入未在 requirements 里的新依赖（先问）
- **不进 secrets / API key 到代码或日志**——用 secret manager
- SQL 用参数化查询，不用字符串拼接
- 用户输入必须校验；输出必须转义（防 XSS）
- 不可逆操作（删数据 / 动钱 / 对外发布 / 改线上配置）必须留给人确认
- 涉及 PII / GDPR 范围的数据，按 [07 §合规](07_CI门与发版策略.md) 走

## 5. 禁止
- 不要为通过类型检查加无意义的抽象
- 不要把失败测试注释掉来"通过"——让它红着被看见
- 不要在 commit / PR 信息里编造未发生的事
- 不要绕过 CI 硬关（force push to main / 关闭 required check）
- 不要在生产分支直接 force push
- 不要用 `any`（TS）/ 不要 catch 所有异常后只 print（Python / Java）

## 6. 测试
- 改了行为就更新 / 补测试；测试是"机器能判的合同"
- 一个端点一个 TDD 循环；不要一次让 AI 写完整个服务
- 故意改坏一处实现 → 对应测试应立刻变红（自检：测试真的在兜底）
- 覆盖率门槛见 [02](02_测试先行清单.md)，降覆盖需 PR 显式说明

## 7. 契约
- 后端实现必须导出 OpenAPI；前端 typed client 必须从 OpenAPI 生成
- 改契约 = 改 spec = 改测试 + 改 changelog（按 SemVer）
- 契约 diff 进 CI（见 [03](03_API契约约束前端_方法卡.md)）

## 8. 可观测
- 关键路径必须有 metric（counter / histogram）+ log（结构化 JSON）+ trace（trace_id 透传）
- 错误必须有错误码 + 上下文；用户侧错误要可读
- 详见 [08](08_AgentOps_可观测与回滚.md)

## 9. AgentOps
- agent 调用必须记录：prompt / 工具调用 / 产物 diff / 测试结果
- agent 触发的不可逆操作必须有人确认（见 §4）
- agent 行为异常（超时 / 失败 / 越权）必须有告警
- 详见 [08](08_AgentOps_可观测与回滚.md)

## 10. 审查（合并前两道关 + CI 硬关）
- **第一关 · AI 自审**：用 [06 审查 prompt](06_审查双关_prompt与checklist.md) 抓"明显错"
- **第二关 · 人来批**：抓"和意图不符 + 不可逆 + 影响范围"
- **CI 硬关**：测试 / 契约 / SAST / SCA / secrets 没过不合并
- 详见 [07](07_CI门与发版策略.md)

## 11. 沟通
- 改实现前先改 spec；spec 是和人对齐的载体
- 回喂 AI 失败信息要具体（"断言 + 输入 + 期望"），不要只说"有 bug"
- 跨模块改动先列影响范围再动手
- PR 标题用 Conventional Commits；body 写"动机 / 改动 / 影响 / 回滚"

## 12. 演进
- 规则被违反 3 次以上 → 写进 Rules
- 规则超过 20 条 → 拆 `<lang>/AGENTS.md` / `<module>/AGENTS.md` 别让根 Rules 变天书
```

---

## 3. 填法示例（以"待办 API"为例）

```markdown
# todo-api · Agent Rules

## 0. 元信息
- 技术栈：Python 3.10 + FastAPI 0.110 + Pydantic v2
- 包管理器：uv
- 部署：Docker
- 最后更新：2026-06-07
- 维护者：@team-platform

## 1. 命名
- snake_case；模块名单数
- 动词开头（`create_todo` / `mark_done` / `list_todos`）

## 2. 目录
- 业务：`app/`（按 domain 划：todos/ users/）
- 测试：`tests/`，镜像 `app/` 结构
- Spec：`docs/spec/`，**绝不放进源码树**

## 3. 口味
- FastAPI + Pydantic v2；端点签名要带类型
- 错误统一抛 HTTPException + 具体状态码
- 日志带 todo_id + request_id

## 4. 安全 / 合规
- 不引 ORM（题目限定内存存储）
- 不做鉴权 / 持久化 / 分页（明确划出范围）
- 不可逆操作（清空存储）必须人确认 + 二次确认
- API key / 数据库连接串走 secret manager

## 5. 禁止
- 不引未在 requirements.txt 里的新依赖
- 不许用 `print()` 调试，统一 logging
- 不许在 commit 里出现 `TODO` 没跟踪 issue

## 6. 测试
- pytest；spec 边界小节每条对应一个 test
- 故意改坏 → 测试必须红
- 覆盖率门槛 80%，CI 强制

## 7. 契约
- FastAPI 自动导出 openapi.json
- typed client 从 openapi.json 生成

## 8. 可观测
- 关键指标：todo_create_total / todo_done_total / request_duration_seconds
- 日志：JSON 格式，含 request_id

## 9. AgentOps
- agent 改 `app/` 必须在 PR body 标注 "agent-assisted"

## 10. 审查
- AI 自审 prompt 见 [06](06_审查双关_prompt与checklist.md)
- 合并前问：业务语义对吗？影响范围清楚吗？
- CI 硬关：pytest + spectral(openapi) + bandit(SAST) + safety(SCA) + gitleaks(secrets)
```

---

## 4. 常见反模式（写 Rules 时避坑）

| 反模式 | 为什么坏 | 改成什么 |
|---|---|---|
| "代码要优雅" | 不可执行 | "函数不超过 N 行 / 嵌套不超过 3 层" |
| "尽量做单元测试" | 不可验证 | "每个端点 + spec 边界各 1 条 pytest 用例" |
| "性能要好" | 没有指标 | "列表接口 P95 < 200ms（压测脚本：…）" |
| "尽量不要……" | AI 听不懂"尽量" | 直接说"不要……"或"必须……" |
| Rules 一次写满 30 条 | AI 注意力分散 | 5–8 条起步，跑偏一次补一条 |
| Rules 全是禁止项 | 缺少正向引导 | 禁止 + 必须 + 风格 三者并重 |
| Rules 不分场景 | 通用条目太多 | 按模块拆 `<module>/AGENTS.md` |

---

## 5. 多文件拆分（企业级项目必备）

```
project/
├── AGENTS.md                  ← 总纲（5-8 条）
├── backend/AGENTS.md          ← 后端专属（语言/框架/部署）
├── frontend/AGENTS.md         ← 前端专属（组件/状态/样式）
├── infra/AGENTS.md            ← IaC 专属（Terraform/Helm/K8s）
└── docs/
    ├── adr/                   ← 架构决策记录
    └── runbooks/              ← 操作手册
```

> **进入子目录时，工具会优先读最近的 AGENTS.md，再读父级**——这是天然的"作用域继承"。

---

## 6. 一句话心法

> **Rules 是被教训喂出来的，不是从想象里长出来的。**
> 第一次写 5 条，写完去干活；跑偏一次回来补一条；半年后它就长成了你团队真正的口味。
