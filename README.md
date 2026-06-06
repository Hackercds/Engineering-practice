# Vibe Coding 企业级起点（SDD + TDD 驱动）

> **把"提示词炼丹"升级为"工程化的约束 + 反馈 + 验证"系统。**
> 本仓库是一套**企业级可复用**的 AI 辅助开发起点：宪法（Rules）→ Spec → 计划 → 任务 → 测试 → 实现 → 契约 → 审查 → 部署。
> 核心：**Spec 是意图、测试是合同、Harness 是缰绳、CI/AgentOps 是兜底。**

---

## 0. 30 秒看懂

| 维度 | 答案 |
|---|---|
| 我是谁 | 工程师 + AI 协作者（agent + harness） |
| 我用什么工具 | 任一 coding agent——**工具是杠杆，spec 才是支点** |
| 我按什么顺序干 | 宪法 → Spec → 计划 → 任务 → 测试 → 实现 → 契约 → 审查 → 部署 |
| 我怎么知道干对了 | 测试全绿 + 审查双关 + 安全门放行 + 监控指标达标 |

完整框架总览见 **[CLAUDE.md](CLAUDE.md)**——Claude Code 入口；通用工程规则见 **[AGENTS.md](AGENTS.md)**——跨工具生效。

---

## 为什么需要这个

| 没有这套 | 有了这套 |
|---|---|
| AI 跑偏 67% 项目失败 | Spec 划界、Harness 兜底，失败可回溯 |
| 提示词越写越长还记不住 | Rules（AGENTS.md）跨工具生效，沉淀一次到处用 |
| 测试 = 文档（事后写） | 测试 = 退出标准（红→绿→重构） |
| 联调时发现接口对不上 | 契约（OpenAPI）→ typed client，编译期就拦 |
| 一次写完整个服务崩了 | 一个端点一个循环，渐进式复杂度管理 |
| Agent 行为黑盒 | AgentOps 轨迹/回放/审计 |
| 不可逆操作出事救不回来 | 强制人确认 + feature flag + 秒级回滚 |
| 不可重复 / 不可规模化 | 9 步流水线化，团队复用 |

---

## 关于 CLAUDE.md 与 AGENTS.md（双文件设计）

| 文件 | 谁读 | 内容 |
|---|---|---|
| **[AGENTS.md](AGENTS.md)** | 任何 AI 编码工具（Codex / Cursor / Aider / Junie / Devin / Claude Code ……） | **通用工程规则**：命名/目录/安全/测试/审査/AgentOps——与工具无关 |
| **[CLAUDE.md](CLAUDE.md)** | **仅** Claude Code | **Claude 专属使用习惯**：plan mode / MCP / 子代理 / 上下文管理——换工具就丢 |

**为什么不冲突 / 为什么建议双文件**：
- 通用规则改 `AGENTS.md` → 任何工具都生效，换工具不丢"工程口味"。
- Claude 偏好改 `CLAUDE.md` → 不污染通用规则。
- 担心多一个文件？—— 改一处通用规则，多个工具跟着生效，这是可移植性的**最小成本**。
- 只想用 Claude、不想维护两份？→ 删 `AGENTS.md`，把内容合进 `CLAUDE.md` 即可（`AGENTS.md` 是 superset，向下兼容）。

---

## 怎么用（三种姿势）

### 姿势 A · 团队新项目（最常用）

```bash
# 1. 复制本仓库
npx degit <your-org>/vibe-coding-starter my-project
cd my-project

# 2. 改 AGENTS.md（工程宪法）
#    - 技术栈、目录、命名、禁止项
#    - 5-8 条起步，跑偏一次补一条

# 3. 写第一份 Spec
cp materials/01_spec模板.md docs/spec/001-<feature>.md
# 填完六节，2 分钟自检通过

# 4. 让 AI 按 Spec 干活（红→绿→重构）
#    一个端点一个循环，遵守 AGENTS.md 口味

# 5. 提 PR 触发 CI（自动跑测试/契约/SCA/SAST/secrets）
#    AI 自审 + 人批 checklist → 两道关都过 → 合并
```

### 姿势 B · 接入现有项目

1. 把 [AGENTS.md](AGENTS.md) 复制到项目根（改名也行：`CLAUDE.md` / `.cursorrules`）
2. 把 [materials/01](materials/01_spec模板.md) 作为新 PR 的 Spec 模板
3. 把 [materials/06](materials/06_审查双关_prompt与checklist.md) 作为 PR template
4. 把 [materials/07](materials/07_CI门与发版策略.md) 的工作流片段接入 CI

### 姿势 C · 评估/培训/分享

读 [CLAUDE.md](CLAUDE.md) 即可——它就是讲义本体。
需要图示见 [assets/](assets/)（4 张流程图：SDD+TDD / spec 传导 / 流水线 / 审查双关）。

---

## 框架结构

```
vibe-coding-starter/
├── CLAUDE.md                          ← ★ Claude Code 入口（习惯 + 引用 AGENTS.md）
├── AGENTS.md                          ← ★ 工程宪法（跨工具通用）
├── README.md                          ← 你正在看
├── .editorconfig / .gitignore / CODEOWNERS
├── .github/                           ← CI / PR / Issue 模板
├── docs/                              ← ADRs / 架构图
├── materials/                         ← ★ SKILL 本体（9 份带走物）
│   ├── 01_spec模板.md                 ← [1-3] Spec / 计划 / 任务
│   ├── 02_测试先行清单.md              ← [4] 红→绿→重构 + 验证
│   ├── 03_API契约约束前端_方法卡.md    ← [6] 契约 → typed client / mock
│   ├── 04_coding-agent选型对照表.md    ← 工具杠杆评估
│   ├── 05_Rules模板_AGENTS.md         ← 工程口味（与 AGENTS.md 互补）
│   ├── 06_审查双关_prompt与checklist.md ← [7] 合并前两道关
│   ├── 07_CI门与发版策略.md           ← ★ CI 硬关 / 分支 / 回滚
│   ├── 08_AgentOps_可观测与回滚.md     ← ★ 轨迹/回放/审计/告警
│   └── 09_Harness工程化指南.md        ← ★ Harness 9 维设计
├── code/                              ← 示例骨架（仅 spec，无实现）
│   ├── backend/spec/todo_api_spec.md
│   └── frontend/README.md
└── assets/                            ← 流程图（drawio + svg）
```

---

## 工作流（9 步走）

```
[0] 宪法/约束      →  AGENTS.md / CLAUDE.md
[1] Spec 探讨       →  materials/01
[2] 实现计划        →  materials/01 §计划
[3] 任务清单        →  materials/01 §任务
[4] 测试先行（红）  →  materials/02
[5] 实现（绿）      →  遵守 materials/05
[6] 契约导出        →  materials/03
[7] 合并前审查      →  materials/06
[8] CI/CD + 监控    →  materials/07 + 08
```

工具选型单独看 [04](materials/04_coding-agent选型对照表.md)。Harness 整体设计见 [09](materials/09_Harness工程化指南.md)。

---

## 必读清单（按角色）

**AI / agent 进入项目，按顺序读 1–4：**

1. [AGENTS.md](AGENTS.md) — 工程宪法（跨工具）
2. [01_spec模板.md](materials/01_spec模板.md) — 做什么、做到什么程度
3. [02_测试先行清单.md](materials/02_测试先行清单.md) — 做完怎么算对
4. [05_Rules模板_AGENTS.md](materials/05_Rules模板_AGENTS.md) — 通用 Rules 详细写法

**Claude Code 用户**，加读 0：

0. [CLAUDE.md](CLAUDE.md) — Claude 专属习惯（plan mode / MCP / 子代理 / 上下文管理）

**人进入评审 / 合并，追加 5–7：**

5. [06_审查双关_prompt与checklist.md](materials/06_审查双关_prompt与checklist.md)
6. [07_CI门与发版策略.md](materials/07_CI门与发版策略.md)
7. [08_AgentOps_可观测与回滚.md](materials/08_AgentOps_可观测与回滚.md)

**架构师 / Harness 设计者，追加 8–9：**

8. [09_Harness工程化指南.md](materials/09_Harness工程化指南.md)
9. [04_coding-agent选型对照表.md](materials/04_coding-agent选型对照表.md)

---

## 跑偏时怎么回看

**90% 的"AI 跑偏"是宪法/Spec/Harness 没搭好**——见 [CLAUDE.md §7](CLAUDE.md) 自检流程。先看自己这头，别急着换模型换工具。

---

## License

MIT。拿走即用，欢迎把你们团队的"工程口味"沉淀进 AGENTS.md 后再开源。
