# Git 工作流约定

> **本仓库的双层模型：`main` 维护框架基线，分支承载项目增量。**
> 这不是 Git 官方约定——是本仓库**项目 + 模板**双重身份下的本地约定，团队内全员遵守。

---

## 一、双层模型（一图看明白）

```
   ─────────────  上层 · 框架 ─────────────
   main 分支
   - 角色：vibe coding 起点模板（CLAUDE.md / AGENTS.md / materials / CI）
   - 稳定性：受保护，必须 PR 合并
   - 范围：通用、跨项目、可复用
   - 用户：clone 走本仓库 → 改占位符 → 起新项目的人

   ─────────────  下层 · 项目 ─────────────
   feat/* / fix/* / chore/* 分支
   - 角色：本项目的具体功能 / 实验 / 内部知识
   - 稳定性：自由演进
   - 范围：项目专属
   - 用户：本项目协作者

   不合并（默认）。
```

**为什么不合并到 main？**
1. `main` 是"模板"——别人 clone 要的是空骨架，不要你的 todo-api wiki
2. 项目内容是**本项目专属**（实体页 / 本地 spec），不是通用规则
3. 框架 vs 项目的生命周期不同——升级模板不该被迫升级项目
4. 强行合并 = 把"私有项目"污染进"公共模板"

---

## 二、分支命名规范

| 前缀 | 用途 | 示例 |
|---|---|---|
| `feat/` | 新能力 / 新模块 | `feat/llm-wiki` · `feat/oauth` |
| `fix/` | bug 修复 | `fix/ci-import` · `fix/wiki-ask` |
| `chore/` | 杂项（deps / 文档 / 重构） | `chore/bump-deps` · `chore/docs` |
| `docs/` | 仅文档 | `docs/git-workflow`（本文） |
| `experiment/` | 短期实验（不保证完成） | `experiment/agent-bench` |

**禁止**：
- ❌ 用人名 / 日期 / 内部代号命名（`zhangsan-test` ❌）
- ❌ 长期存活（> 2 周）的"半成品"分支——拆小或删
- ❌ 直接在 main 上工作

---

## 三、三种典型场景

### 场景 A · 给"模板"加新能力（合并到 main）

```
新需求：模板新增一个 "RAG 检索" 能力
  ↓
切到 main  →  git checkout main
  ↓
新建分支  →  git checkout -b feat/rag-template
  ↓
在分支上改 CLAUDE.md / AGENTS.md / materials/ / CI（影响所有人的部分）
  ↓
本地验证 → pytest / lint / CI
  ↓
git push origin feat/rag-template
  ↓
开 PR → main（标准审查流程）
  ↓
合并 → 删除分支
```

**判断标准**：你的改动是否**对所有 clone 这个仓库的人都有用**？是 → 走场景 A。

### 场景 B · 给"本项目"加东西（不合并，留分支）

```
项目需求：写 todo-api 的 wiki 知识页
  ↓
切到本项目的开发分支 →  git checkout feat/llm-wiki
  ↓
在分支上加 wiki/*.md / raw/ / scripts/
  ↓
不碰 main 上的 CLAUDE.md / AGENTS.md / materials
  ↓
git push origin feat/llm-wiki
  ↓
不开 PR（默认） / 团队内 code review
```

**判断标准**：你的改动**只对本项目有用**？是 → 走场景 B。

### 场景 C · 从 main 同步 bug fix 到项目分支

```
main 上有人合并了 CI 修复
  ↓
切到项目分支  →  git checkout feat/llm-wiki
  ↓
拉 main 的 fix  →  git cherry-pick <commit-hash>
                或  git merge main --no-ff
  ↓
推项目分支     →  git push origin feat/llm-wiki
```

**何时需要**：项目分支依赖 main 的新能力 / bug fix 时。

---

## 四、保护规则（main 分支）

设置在 GitHub/GitLab 仓库设置里：

| 规则 | 推荐 |
|---|---|
| Require PR before merging | ✅ |
| Require 1 approval | ✅（含 CODEOWNERS 自动路由） |
| Dismiss stale approvals on push | ✅ |
| Require status checks (CI 12 门) | ✅ |
| Require linear history | ✅ |
| Require signed commits | ✅（高敏项目） |
| Restrict who can push | 仅 release bot / maintainer |
| Allow force pushes | ❌ |
| Allow deletions | ❌ |

---

## 五、常见误区

### 误区 1 · "分支 = 多个版本"

**错**。git branch 是**指向 commit 的指针**，不是"并行版本"。
- main 和 feat/llm-wiki 是**两个指针**指向**不同的 commit**
- 合并 = 把 A 的 commit **并入** B，B 拥有 A 的所有改动，**不会**出现"v1 v2 并行"
- 分支生命周期内是独立空间，合并后归一

### 误区 2 · "必须合并才算数"

**错**。分支可以**长期存在**：
- LLM Wiki 这种"项目专属能力" → 留 `feat/llm-wiki`，长期维护
- bug fix → 留 `fix/xxx` 直到上线验证后归档
- 弃用 → 删分支（git branch -D）

### 误区 3 · "feature 分支必须合到 main"

**错**。这是 Git Flow 模型的"硬合并"假设。
- GitHub Flow：每个 PR 都合并（适合小步快跑）
- **本仓库约定**：按内容性质决定——**模板**合 main，**项目**留分支
- 不要为了"流程正确"而把项目内容强塞 main

### 误区 4 · "分支太多难管理"

**缓解**：
- 分支名规范（按 §二），一眼看出在做什么
- 长期分支 ≤ 3 个（多了就拆或合并到长期分支）
- 删完成的临时分支（合并后默认删）
- 用 `git branch -a` + `git fetch --prune` 定期清理

---

## 六、与本仓库其他文件的关系

| 文件 | 内容 | 何时改 |
|---|---|---|
| `AGENTS.md` | 跨工具工程规则 | main 上改 |
| `CLAUDE.md` | Claude 使用习惯 | main 上改 |
| `README.md` | 项目入门 | main 上改 |
| `materials/01-09` | 通用 SKILL | main 上改 |
| `docs/git-workflow.md`（本文件） | 分支约定 | main 上改 |
| `wiki/**` | 项目专属知识 | 项目分支上改（**不合并**） |
| `raw/**` | 项目原始资料 | 项目分支上改（**不合并**） |
| `scripts/wiki/**` | Wiki 工具脚本 | 项目分支上改（**不合并**） |
| `.github/workflows/wiki-ci.yml` | Wiki CI | 项目分支上改（**不合并**） |

---

## 七、决策树（30 秒判断）

```
我要加一个改动 X
  │
  ├─ X 对所有 clone 这个仓库的人都有用？
  │   │
  │   ├─ 是 → 走场景 A（main 上 feat/ → PR → 合并）
  │   │
  │   └─ 否 → 走场景 B（在项目分支上改，不合并）
  │
  └─ 不确定？问自己：
      "X 改完了，README 需要加一句吗？"
       ├─ 是 → 模板性质 → 场景 A
       └─ 否 → 项目性质 → 场景 B
```

---

## 八、变更本文件

`docs/git-workflow.md` 是**框架文件**——只改 main 分支。
PR 流程：本地改 → 跑 CI → 推 feat 分支 → 开 PR → 团队 review → 合 main。

---

> **一句话**：main 是给别人用的，分支是给自己用的。**合并不是义务，是工具**。
