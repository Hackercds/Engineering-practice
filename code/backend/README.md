# 待办事项 API · 后端示例骨架

> **代码不在这里**——它是企业级 Spec 驱动的示例：只有 spec、env、目录约定，**实现由 AI 在 CI 12 门 + 测试先行的约束下生成**。
> 这正是 vibe coding 在企业里应该有的样子：Spec 是真相源，AI 干苦力，CI/AgentOps 兜底。

---

## 这是什么

演示"从一份人能审完的 spec，用 SDD + TDD + 契约 + CI 现场长出可信代码"的企业级流程：

```
spec 探讨（人确认）
  ↓
TDD 红 → AI 按 spec 写测试（先红）
  ↓
TDD 绿 → AI 补实现（跑到全绿）
  ↓
OpenAPI 契约导出（机器可读）
  ↓
前端 typed client 自动生成 + mock 自动起
  ↓
CI 12 门（测试/契约/SAST/SCA/secrets）全过 → 合并
```

详细工作流见根目录 [CLAUDE.md](../CLAUDE.md) 与 [materials/01-09](../materials/)。

---

## 目录

```
backend/
├── SPEC-001-todo-api.md            ← SDD 产物：人确认的规格
├── AGENTS.md                        ← 后端专属 Rules（如有）
├── requirements.txt
├── pyproject.toml / package.json   ← 锁版本
├── app/                             ← 业务代码（AI 生成）
│   ├── todos/
│   ├── users/
│   └── main.py
├── tests/                           ← 测试（AI 写 + 人审）
│   ├── unit/
│   ├── integration/
│   └── contract/                    ← 从 OpenAPI 派生
├── gen/                             ← 自动生成（git 忽略行级注解）
│   └── client/                      ← 给前端用的 typed client
└── deploy/
    ├── Dockerfile
    └── k8s/
```

---

## 演示用的 Spec

见同目录 `SPEC-001-todo-api.md`（与 materials/01 等价，但更"成品化"——带元信息、验收、计划、任务）。

---

## 环境

```bash
# Python（以 uv 为例）
uv venv
uv pip install -r requirements.txt

# 启动
uvicorn app.main:app --reload

# 测试
pytest --cov=app --cov-fail-under=80

# 契约
oasdiff diff origin/main HEAD
spectral lint openapi.yaml

# 安全
bandit -r app/
safety check
gitleaks detect --redact
```

---

## 文件 × 谁产生

| 文件 | 作用 | 谁产生 |
|---|---|---|
| `SPEC-001-todo-api.md` | SDD 产物：人确认的规格 | **人写、AI 辅助** |
| `requirements.txt` / `pyproject.toml` | 依赖 | 人定 + 工具装 |
| `app/**` | 业务实现 | **AI 按 spec + TDD 生成** |
| `tests/**` | 测试 | **AI 先写（红）、人审、AI 补（绿）** |
| `openapi.yaml` | 契约 | **自动导出** |
| `gen/client/**` | 前端 typed client | **自动生成** |

> **人 / AI 的边界**：人定 spec、审 PR、批不可逆；AI 写代码、写测试、跑命令、回填反馈。CI/AgentOps 兜底。
