# CLAUDE.md · Wiki Schema（极简版 · nashsu 范式）

> **本文件是 LLM 维护 `wiki/` 的唯一配置文件。**
> 配合根目录 [`AGENTS.md`](../AGENTS.md)（工程宪法）和 [`CLAUDE.md`](../CLAUDE.md)（Claude 使用习惯）。
>
> ## 为什么极简
>
> 很多 LLM Wiki 实践会演化成十几个 K 的"次级应用"（前端 / MCP server / 几十个 skills / 复杂子目录）。**这是反模式**——
> wiki 的价值是"AI 看得懂、人能维护、git 可追溯"，**不是"工具多"**。
> 本仓库坚持**单一文件配置 + 纯 Markdown + Python 脚本**的极简范式（参考 [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki) 的核心理念）。

---

## 一、Wiki 使命

> **知识不复利消失。** 每次 Q&A 的有价值输出，AI 自动归档回 Wiki。

服务于企业级项目的：
- **架构决策可追溯**（ADRs / Why 文档）
- **AI Agent 协作上下文**（任何 agent 都能秒级找到所需信息）
- **团队 onboarding**（新人 / 新 agent 第一周就能贡献）

---

## 二、目录结构（极简）

```
project/
├── raw/                       ← ★ 原始资料（只读，AI 不可修改）
│   ├── specs/                 ← SDD 产物
│   ├── adrs/                  ← 架构决策记录
│   ├── runbooks/              ← 运维手册
│   ├── incidents/             ← 事故复盘
│   └── external/              ← 外部资料
│
├── wiki/                      ← ★ LLM 维护的知识层（所有页面平铺）
│   ├── CLAUDE.md              ← 本文件（Schema · 唯一配置文件）
│   ├── index.md               ← 目录（AI 必读 · 唯一导航）
│   ├── log.md                 ← 时间线（可解析前缀，append-only）
│   ├── *.md                   ← 所有知识页平铺（无子目录）
│   └── graphs/                ← 关系图（自动生成）
│
├── scripts/wiki/              ← 4 个 Python 脚本（CI 用）
│   ├── ingest.py              ← 把 raw 编译为 wiki
│   ├── lint.py                ← 健康检查
│   ├── render_graph.py        ← 渲染 Mermaid
│   └── mcp_server.py          ← 可选：把 wiki 暴露为 MCP
│
└── .github/workflows/
    └── wiki-ci.yml            ← Wiki 独立 CI（每周 + 每次 PR）
```

**禁止**：
- ❌ 子目录（`concepts/` `entities/` `summaries/`）—— 用 frontmatter `type` 字段区分
- ❌ 多份 Schema（`README.md` `INSTRUCTIONS.md` `AGENTS.md` 重复内容）
- ❌ 前端 / UI（Obsidian 就是 UI）
- ❌ 复杂 skill 系统（4 个 Python 脚本足够）

---

## 三、5 个核心操作

| 操作 | 何时 | 做什么 |
|---|---|---|
| **ingest** | raw 新增资料 | 读源 → 写新页 / 更新旧页 → 更新 index → append log |
| **query** | 用户 / agent 提问 | 读 index → 读相关页 → 综合回答 → 归档有价值的输出 |
| **lint** | 每周 + 每次 PR | 检查死链/孤儿/过时/frontmatter/Mermaid |
| **render-graph** | 任何页面前置 | 从 wikilinks 派生 → `wiki/graphs/*.mmd` |
| **audit** | 收到人工反馈 | 修页面 → append log |

---

## 四、命名与格式

### 4.1 文件命名

| 类型 | 风格 | 示例 | frontmatter `type` |
|---|---|---|---|
| 概念页 | Title Case + `.md` | `Spec Driven Development.md` | `concept` |
| 实体页 | kebab-case + `.md` | `todo-api.md` | `entity` |
| 摘要页 | `<source-slug>.md` | `spec-001-todo-api.md` | `summary` |
| 图 | `<scope>.mmd` | `concepts.mmd` | — |

### 4.2 Frontmatter（每个页顶部必须）

```yaml
---
title: <Page Title>
type: concept | entity | summary
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [raw/specs/SPEC-001-todo-api.md]
---
```

### 4.3 Wikilink

- `[[Page Title]]`（推荐）或 `[[page-slug]]`
- 首次提及加链接；同一页最多 2 次
- 链接目标必须存在（lint 校验）

### 4.4 页面长度

| 类型 | 目标 | 上限 |
|---|---|---|
| concept | 400–800 | 1200 |
| entity | 200–400 | 500 |
| summary | 150–300 | 400 |

**超长必须拆**（拆为多个子页 + `index.md` 索引页）。

### 4.5 Mermaid 图

- **每个 concept 页 ≥ 1 个 Mermaid 图**
- 复杂图（> 20 节点）拆为多图
- 嵌入代码块 ` ```mermaid `，无需单独文件
- 关系图（跨页）放 `wiki/graphs/*.mmd`，CI 渲染 SVG/PNG

### 4.6 章节结构

**概念页**：
```markdown
# <Title>

<一句话定义>

## What it is
## Key Properties / Tradeoffs
## Relationship to Other Concepts
## Mermaid Diagram
## Open Questions
## Sources
```

**实体页**：
```markdown
# <Name>

<一句话描述>

## Key Features / Known Issues
## Related Concepts
## Mermaid Diagram (optional)
## Sources
```

---

## 五、index.md（唯一目录）

> **不要建子目录索引页**——`index.md` 是 wiki 唯一目录。
> 任何 agent 接入的**第一步**：读 `CLAUDE.md` → 读 `index.md` → 干活。

格式：
```markdown
# Wiki Index

> 最后更新：YYYY-MM-DD
> 总页数：N

## 概念（按主题分组）
- [[Spec Driven Development]] — 一句话
- [[Harness Engineering]] — 一句话

## 实体
- [[todo-api]] — 一句话
- [[claude-code]] — 一句话

## 摘要
- [[spec-001-todo-api]] — 一句话

## 图
- `graphs/concepts.mmd` — 概念关系
```

**AI 自动维护**（人不要手写）——跑 `python scripts/wiki/lint.py` 会提示差异。

---

## 六、log.md（可解析时间线）

> **append-only，绝对不要改历史行。** CI 用 `grep "^## \["` 解析。

格式：
```markdown
## [YYYY-MM-DD] ingest | <source-slug>
- 写入: [[page-a]], [[page-b]]
- 更新: [[index]]
- 摘要: [[summary-name]]

## [YYYY-MM-DD] query | <一句话问题>
- 引用: [[page-x]], [[page-y]]
- 产出: 新页 [[new-insight]]（如有价值）

## [YYYY-MM-DD] lint
- 发现: 3 orphan / 1 dead link / 2 missing frontmatter
- 已修: ...

## [YYYY-MM-DD] render-graph
- 渲染: concepts.mmd, entities.mmd, full.mmd
```

**为什么用 `[YYYY-MM-DD] op | name` 前缀**：
- `grep "^## \[" log.md | tail -5` 看最近 5 条
- `grep "^## \[2026-06\]" log.md` 看本月所有
- `grep "ingest" log.md` 看所有 ingest
- Unix 工具友好

---

## 七、敏感信息

- **不写**：API Key、密码、内网地址、PII
- **占位符**：`${ENV_VAR}`、`<YOUR_KEY>`、`<REDACTED>`
- 事故脱敏后的复盘才入 raw

---

## 八、自动化（CI · 极简）

`.github/workflows/wiki-ci.yml` 跑 2 个 job：

1. **lint**（每周 + PR）：`python scripts/wiki/lint.py`
2. **render**（PR）：`python scripts/wiki/render_graph.py --check`（Mermaid 能编译）

**MCP server 是可选**——`scripts/wiki/mcp_server.py` 单文件 80 行，按需启用。

---

## 九、工具链（外部）

| 工具 | 用途 |
|---|---|
| **Obsidian** | 本地浏览 + 图谱视图（推荐 UI） |
| **`scripts/wiki/*.py`** | 4 个脚本，CI 跑 |
| **`qmd`** | > 100 页时启用，本地全文搜索 |
| **MCP（可选）** | 把 wiki 暴露给外部 agent |

---

## 十、与根 CLAUDE.md / AGENTS.md 的边界

| 文件 | 内容 | 谁改 |
|---|---|---|
| `AGENTS.md` | 工程宪法 | 慢 |
| `CLAUDE.md`（根） | Claude 使用习惯 | 慢 |
| **`wiki/CLAUDE.md`（本文件）** | **Wiki Schema** | 中 |
| `wiki/index.md` | Wiki 目录 | 快（AI） |
| `wiki/log.md` | 时间线 | 快（AI） |
| `wiki/*.md` | 知识页 | 快（AI） |

**绝不重复**——AGENTS.md 写规则，wiki 写知识。

---

## 十一、本 Schema 的演化

- 新增操作类型 → 第三章补充
- 新增格式 → 第四章
- 任何变更 → 同步在 `log.md` 写一行
