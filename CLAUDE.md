# CLAUDE.md · Claude Code 入口

> **Claude Code 第一份要读的文件。**
> 它放 **Claude 专属习惯**（MCP / plan mode / 子代理 / 上下文管理……），并引用 [`AGENTS.md`](AGENTS.md) 里的通用工程规则。
>
> ## 为什么双文件
>
> - **`AGENTS.md`**（[打开](AGENTS.md)）= 通用工程规则（命名/安全/测试/审査/AgentOps……），跨工具生效（Codex/Cursor/Aider/Junie/Devin……），换工具不丢口味。
> - **`CLAUDE.md`**（本文件）= Claude Code 专属使用习惯（plan mode、MCP、子代理、上下文管理、slash command……），只 Claude 读。
> - 通用规则改 `AGENTS.md`；Claude 偏好改本文件。**不要重复**。
> - 担心多一个文件？—— 改一处通用规则，Codex/Cursor/Aider 也跟着生效，这是可移植性的最小成本。
>
> ## 速查
>
> | 我想知道…… | 看哪里 |
> |---|---|
> | 命名/安全/测试/审査/AgentOps | [AGENTS.md](AGENTS.md) |
> | 工作流（9 步）/ 必读清单 / 跑偏自检 | 本文件 §2 / §5 / §7 |
> | Claude 怎么用 / MCP / plan mode | §8（Claude 专属） |

---

## 0. 30 秒看懂

| 维度 | 答案 |
|---|---|
| 我是谁 | 工程师 + Claude 协作者（agent + harness） |
| 我用什么工具 | Claude Code——**工具是杠杆，spec + AGENTS.md 才是支点** |
| 我按什么顺序干 | **宪法 → Spec → 计划 → 任务 → 测试 → 实现 → 契约 → 审查 → 部署** |
| 我怎么知道干对了 | 测试全绿 + 审查双关 + 安全门放行 + 监控指标达标 |

> **一句话心法**：把 AI 当一匹马，你的工作是**造 Harness**（缰绳 + 路线 + 围栏 + 反馈），不是写更长的 prompt。

---

## 1. 角色与原则

**人**：定义意图、范围、不可逆边界、最终质量担保。
**AI（agent）**：在 Harness 约束下生成、迭代、验证。
**Harness（你搭的工作环境）**：Rules / Spec / Skills / CI / 契约 / 监控——把 AI 的自由发挥空间一层层夹紧。

七条铁律（详 `AGENTS.md` §4 / §5）：

1. **Spec 先于代码**——Spec 是意图的可执行表达；人审 Spec，不审实现。
2. **AGENTS.md 划界**——技术栈、命名、目录、禁止项；AI 必须遵守。
3. **测试是 AI 的退出标准**——红→绿→重构，不许"它说写好了就算了"。
4. **范围划死**——"明确不做"必须写，否则 AI 默认会做你没禁止的事。
5. **契约往下游传导**——后端 OpenAPI 约束前端；typed client 落到代码级别。
6. **两道审查 + 自动化安全门**——AI 自审抓明显错 + 人批抓意图错/不可逆 + SAST/SCA/secrets 硬关。
7. **可观测可回滚**——任何 agent 行为可回放（AgentOps），任何发版可秒级回退。

---

## 2. 工作流（9 步走，按顺序，不可跳）

```
[0] 宪法/约束      →  AGENTS.md                （Harness 起点）
[1] Spec 探讨       →  materials/01_spec模板
[2] 实现计划        →  materials/01 §计划      （从 spec 派生的任务分解）
[3] 任务清单        →  materials/01 §任务      （可逐项验收的小块）
[4] 测试先行（红）  →  materials/02_测试先行清单 （单元 + 契约 + 边界）
[5] 实现（绿）      →  遵守 AGENTS.md 口味
[6] 契约导出        →  materials/03_API契约约束前端
[7] 合并前审查      →  materials/06_审查双关
[8] CI/CD + 监控    →  materials/07_CI门 + 08_AgentOps
```

> 工具选型见 [04](materials/04_coding-agent选型对照表.md)。Harness 整体设计见 [09](materials/09_Harness工程化指南.md)。

---

## 3. 框架结构（一次看全）

```
vibe-coding-starter/                            ← 项目根
├── CLAUDE.md                                   ← ★ 你在这里（Claude 入口 + 习惯）
├── AGENTS.md                                   ← ★ 通用工程规则（跨工具）
├── README.md                                   ← 起步指引
├── .editorconfig / .gitignore / CODEOWNERS
├── .github/                                    ← CI / PR / Issue 模板
├── docs/                                       ← ADRs / 架构图
├── materials/                                  ← ★ SKILL 本体（9 份）
│   ├── 01_spec模板.md                          ← Spec / 计划 / 任务
│   ├── 02_测试先行清单.md
│   ├── 03_API契约约束前端_方法卡.md
│   ├── 04_coding-agent选型对照表.md
│   ├── 05_Rules模板_AGENTS.md                  ← 通用 Rules 详细模板
│   ├── 06_审查双关_prompt与checklist.md
│   ├── 07_CI门与发版策略.md
│   ├── 08_AgentOps_可观测与回滚.md
│   └── 09_Harness工程化指南.md
├── code/                                       ← 示例骨架（仅 spec，无实现）
│   ├── backend/SPEC-001-todo-api.md            ← 成品 Spec 范例
│   └── frontend/README.md
└── assets/                                     ← 流程图
```

---

## 4. 工具与契约

### 4.1 Spec 是单一真相源

```
Spec（人确认的意图）
  ├─▶ 计划（任务分解）→ 任务清单
  ├─▶ 测试（退出标准）→ 实现
  ├─▶ OpenAPI（机器可读契约）→ typed client / mock / 文档
  └─▶ ADRs / 变更日志（派生物）
```

### 4.2 改 Spec 才能改实现

- 实现和 Spec 冲突 → 先改 Spec → 再让 AI 改实现。
- 改 Spec 必须同步改测试 + 同步下游契约。

### 4.3 测试 = 机器能判的合同

- 一个端点一个 TDD 循环；不要一次让 AI 写完整个服务。
- 故意改坏一处实现 → 对应测试**必须**立刻红（验证"测试真的在兜底"）。

---

## 5. 必读清单（按角色）

**Claude 进入本项目，按顺序读 1–4：**

1. **[AGENTS.md](AGENTS.md)** — 通用工程规则（必读）
2. [01_spec模板.md](materials/01_spec模板.md) — 知道"做什么、做到什么程度"
3. [02_测试先行清单.md](materials/02_测试先行清单.md) — 知道"做完怎么算对"
4. [05_Rules模板_AGENTS.md](materials/05_Rules模板_AGENTS.md) — 通用 Rules 详细写法（与 AGENTS.md 互补）

**人进入项目评审 / 合并，追加 5–7：**

5. [06_审查双关_prompt与checklist.md](materials/06_审查双关_prompt与checklist.md)
6. [07_CI门与发版策略.md](materials/07_CI门与发版策略.md)
7. [08_AgentOps_可观测与回滚.md](materials/08_AgentOps_可观测与回滚.md)

**架构师 / Harness 设计者，追加 8–9：**

8. [09_Harness工程化指南.md](materials/09_Harness工程化指南.md)
9. [04_coding-agent选型对照表.md](materials/04_coding-agent选型对照表.md)

---

## 6. 反模式（看到就停）

| 反模式 | 后果 | 改成什么 |
|---|---|---|
| AI 写完实现再补 Spec | Spec 是事后合理化，约束失效 | Spec 先于实现 |
| "尽量做单元测试" | AI 听不懂"尽量" | "每个端点 + Spec 边界各 1 条 pytest" |
| 让 AI 一次写完整个服务 | 复杂度爆炸，测试一片红不知从哪修 | 一个端点一个 TDD 循环 |
| 把失败测试注释掉"通过" | 失去兜底 | 失败保留，红着被看见 |
| 不可逆操作（删数据/动钱/发布）由 AI 直接执行 | 出事救不回来 | 强制留给人确认 + 灰度 + feature flag |
| 把 API 文档当"待办事项"手维护 | 文档必然过期 | 文档 = 派生物（OpenAPI 派生） |
| Rules 一次写 30 条 | AI 注意力分散 | 5–8 条起步，跑偏一次补一条 |
| Harness 缺位（裸 prompt） | "提示词炼丹" | 约束 + 反馈 + 验证 三件套先搭好 |
| Agent 行为无观测 | 出问题无法回溯 | 至少记录：prompt/工具调用/产物 diff/测试结果 |
| 把"安全"留给代码评审 | 漏掉就是事故 | SAST/SCA/secrets 进 CI 硬关 |

---

## 7. 跑偏时怎么回看（自检流程）

```
跑偏了
  ↓
[1] AGENTS.md 写清楚了吗？（技术栈/目录/命名/禁止）
   没写 → 补 AGENTS.md，**别让 AI 猜**
  ↓
[2] Spec 写清楚了吗？（边界/失败码/范围/不做）
   没写清 → 改 Spec，**别让 AI 补范围**
  ↓
[3] 测试写到位了吗？（边界每条 1 条，故意改坏会红吗）
   没到位 → 补测试，**别让 AI 改实现来迁就**
  ↓
[4] Harness 搭了吗？（约束/反馈/验证）
   没搭 → 先把 Harness 补齐，再让 AI 干活
  ↓
[5] 工具选错了吗？（spec 强遵从场景却用了 Copilot？）
   选错 → 看 04 选型表，先别急着换工具
  ↓
[6] 审查 + CI 跑了吗？（AI 自审 + 人批 + SAST/SCA/secrets）
   没跑 → 跑，**硬关没过不合并**
  ↓
[7] AgentOps 开了吗？（轨迹/回放/告警）
   没开 → 开，否则下次跑偏还是看不见
```

> **90% 的"AI 跑偏"是宪法/Spec/Harness 没搭好**——先看自己这头，别急着换模型换工具。

---

## 8. Claude Code 专属习惯（仅 Claude 读 · 与工具无关的规则放 AGENTS.md）

> 这里的都是 **Claude Code 使用习惯**，不是工程规则——换工具就丢，无所谓。

### 8.1 工作模式

- **默认开启 plan mode**：复杂任务先出方案，确认后再执行。
- **一个任务一个子代理**：搜索/审査/重构拆子代理，主对话保持简洁。
- **避免"循环对话"**：超过 3 轮同主题未推进 → `/clear` 后用更具体的 prompt 重启。

### 8.2 上下文管理

- **优先用 `AGENTS.md` 注入项目规则**，不要在 prompt 里重复。
- **大段代码**用 `@` 引用文件路径，不要 paste。
- **历史超长**时主动用 `/compact` 或 `/clear`，别等 Claude"自己忘"。
- **MCP 工具**按需启用，不常用的 disable（避免选择困难）。

### 8.3 必用工具

| 工具 | 什么时候用 |
|---|---|
| `Read` / `Grep` / `Glob` | 进入新项目、改 bug 前必跑——别凭印象改 |
| `Bash` | 跑测试 / lint / typecheck——反馈拿回来再让 AI 改 |
| `Agent`（子代理） | 搜索、审査、跨文件重构 |
| `TodoWrite` | 任务 ≥ 3 步时启用——让 AI 自己跟踪进度 |
| `Skill` | 复用动作（如 `code-review` / `verify`）——别每次重写 prompt |

### 8.4 反馈约定

- **失败信息要喂回来**：测试红的具体断言 + 输入 + 期望值（见 [02 §3](materials/02_测试先行清单.md)）。
- **改坏自检**后让 Claude 恢复 + 加 regression test。
- **不要"我看你修一下"**——给具体位置 + 期望行为。

### 8.5 不可做的事

- **不要让 Claude 直接跑**：`git push --force` / `rm -rf` / `chmod 777` / 改 prod 配置 / 删数据库——Claude 必须先停下问人。
- **不要让 Claude 编 commit**——commit 信息人写或人审。
- **不要在 prod 分支直接 force push**——这条由 CI 保护规则兜底（[07 §4](materials/07_CI门与发版策略.md)）。

### 8.6 退出标准

- 测试全绿 + 故意改坏自检通过 + review prompt 跑过 + AGENTS.md 没新增违反项 → 任务完成。
- 任一项没过 → **不算完**，继续。

---

## 9. 一句话收束

> **确定性逐层传导**：Spec 决定测试，测试决定实现，实现导出契约，契约约束前端，AGENTS.md 约束一切，CI/AgentOps 兜底一切。
> AI 自由发挥的空间被 Harness 一层层夹紧——这才是"AI 写的代码信得过"的真正来源。

---

## 附：跳读指引

- 我是新来的 Claude → §5 必读清单 1–4 + §8 Claude 习惯
- 我要给团队搭 Harness → [09](materials/09_Harness工程化指南.md) + [AGENTS.md](AGENTS.md)
- 我要起一个新项目 → 复制本仓库 → 改 AGENTS.md 占位符 → 写第一份 Spec
- 我要给前端写约束 → [03](materials/03_API契约约束前端_方法卡.md)
- 我要审一段 PR → [06](materials/06_审查双关_prompt与checklist.md) + [07](materials/07_CI门与发版策略.md)
- 我跑偏了 → §7 自检流程
- Claude 使用习惯相关 → §8
