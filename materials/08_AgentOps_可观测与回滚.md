# AgentOps · 可观测与回滚（企业级 · 新增）

> **没有 AgentOps，就没有"AI 写的代码信得过"**——你不知道它干了啥、出错了怎么救。
> 本卡定义：如何记录 agent 行为、如何回放调试、如何审计、如何告警、如何回滚。
>
> 对应生产环境 SRE 体系，本卡聚焦 **agent 行为 + AI 产物** 的可观测。

---

## 1. 为什么需要 AgentOps

| 没 AgentOps | 有 AgentOps |
|---|---|
| Agent 跑了 30 分钟，最后出 bad diff——为什么？不知道 | 轨迹全记录，**回放** 看每一步 prompt / 工具 / 产物 |
| 线上故障，怀疑是上周的 AI PR——找证据？ | commit ↔ agent run 一一对应 |
| 团队想用 AI，但合规说"不可审计" | 审计日志按法务要求导出 |
| Agent 在 prod 跑了危险操作 | 告警 + 自动回滚 + 二次确认 |
| Agent 失败率突增 | 指标看板 + 自动告警 |

---

## 2. AgentOps 5 维

```
            ┌─ 轨迹 ──── 每次 run 完整记录
            │
   Agent ───┼─ 评估 ──── 产出自动打分
            │
            ├─ 监控 ──── 指标 / 告警
            │
            ├─ 审计 ──── 合规 / 法务 / 复盘
            │
            └─ 回滚 ──── 出问题秒退
```

---

## 3. 维度 1 · 轨迹（Trace · 必备）

> **每次 agent run 必须记录以下字段**——这是"AI 时代的应用日志"。

### 3.1 必记字段

| 字段 | 含义 | 示例 |
|---|---|---|
| `run_id` | 唯一 ID | `run-2026-06-07-001` |
| `agent_name` / `model` | 哪个 agent / 哪个模型 | `claude-opus-4-8` |
| `trigger` | 谁触发的 | `pr-123` / `user@team` / `cron` |
| `inputs` | 输入 | spec 内容、上下文 |
| `tool_calls` | 工具调用序列 | `[{tool: read_file, args: ...}]` |
| `outputs` | 产物 | diff、commit hash、PR url |
| `tokens` | 用量 | input/output/cache |
| `cost` | 花费 | USD |
| `duration` | 时长 | ms |
| `result` | 成功 / 失败 / 部分 | `success` |
| `error` | 失败原因 | exception + stack |
| `git_sha` | 关联 commit | `abc123` |
| `user_id` | 谁点的"运行" | `alice@team` |
| `correlation_id` | 与上游 trace 打通 | `trace-...` |

### 3.2 存储与查询

| 量级 | 存储 |
|---|---|
| < 1000 runs/天 | Postgres / SQLite |
| 1000–100k | ClickHouse / BigQuery / Elasticsearch |
| > 100k | 专用 AgentOps 平台（AgentOps.ai / Langfuse / Arize / Helicone） |

### 3.3 工具

| 工具 | 特点 |
|---|---|
| **AgentOps.ai** | 400+ LLM/Agent 集成，开箱即用 |
| **Langfuse** | 开源，self-host 可控 |
| **Arize Phoenix** | 开源，evaluation 强 |
| **Helicone** | 反向代理，零代码接入 |
| **OpenLLMetry** | OpenTelemetry 标准 |

---

## 4. 维度 2 · 评估（Eval · 强烈建议）

> **Eval = agent 产物的自动打分**——避免"看起来 OK 实际跑偏"。

### 4.1 Eval 4 维

| 维度 | 含义 | 怎么评 |
|---|---|---|
| **Correctness** | 产物对吗 | 测试是否绿 / 是否符合 spec |
| **Style** | 风格符合吗 | Lint / format / Rules 偏离度 |
| **Safety** | 安全吗 | SAST / secrets / PII 漏出 |
| **Cost** | 性价比 | tokens / 耗时 / 通过率 |

### 4.2 Eval 触发点

| 触发 | 评什么 |
|---|---|
| PR 提交 | 产物是否通过 CI 12 门 + 是否符合 spec |
| 合并后 | prod 运行 1h / 1d 后关键指标是否异常 |
| 模型升级 | 用历史轨迹回放，diff 指标 |
| 重大事故 | 复盘——这个 run 当时为什么这么走 |

### 4.3 Eval 数据集

> **不要临时造 eval**——建一个"金标集"，每次重大变更跑一遍。

```
eval/
├── gold_set.jsonl       # {input, expected_output, expected_behavior}
├── run_eval.py
└── report/
    ├── 2026-06-07.html
    └── trend.png
```

---

## 5. 维度 3 · 监控（Metrics & Alerts）

### 5.1 关键指标

| 指标 | 类型 | 告警阈值（示例） |
|---|---|---|
| `agent_run_total` | counter | — |
| `agent_run_duration_seconds` | histogram | P95 > 5min |
| `agent_run_error_rate` | gauge | > 5% |
| `agent_run_cost_usd_total` | counter | 单日 > 预算 |
| `agent_correction_rate` | gauge | 同一任务被改 > 1 次 |
| `agent_first_pass_success_rate` | gauge | < 70% |
| `agent_test_pass_rate` | gauge | < 95% |
| `agent_token_usage` | histogram | 单 run > X |

### 5.2 告警分级

| 级别 | 触发 | 处理 |
|---|---|---|
| P1 | agent 触发了不可逆操作 | **立即**：人确认 / 暂停 agent / 回滚 |
| P2 | 错误率 / 成本突增 | 15 分钟：人查 |
| P3 | 单 run 超时 / 单测失败 | 1 小时：自愈 or 工单 |
| P4 | 趋势异常 | 次日：周会回顾 |

### 5.3 看板

- **团队看板**：本日 run 数 / 通过率 / 成本 / Top 失败模式
- **个人看板**：我的 agent 任务 / 节省时间 / 失败任务
- **管理层看板**：AI 投入产出 / 趋势 / 风险

---

## 6. 维度 4 · 审计（Audit · 合规必备）

### 6.1 审计日志

| 必记 | 用途 |
|---|---|
| 谁（user / system）触发了 agent | 责任追溯 |
| agent 跑了什么（diff / 工具调用） | 复盘 |
| 是否触发了不可逆操作 | 法务 |
| 是否有人确认 | 流程合规 |
| 模型版本 / provider | 模型供应链 |

### 6.2 合规场景

| 场景 | 要求 |
|---|---|
| 金融 / 医疗 | 全量轨迹 + 留痕 N 年 + 法务可查 |
| GDPR | PII 不入轨迹 / 脱敏 / 主体删除权 |
| 出口管制 | 模型 / 数据地域合规 |
| 客户合同 | 明确"AI 参与"声明 / 可选 opt-out |

### 6.3 数据保留

| 类型 | 保留期 |
|---|---|
| 元数据（run_id / user / cost） | 1+ 年 |
| 完整轨迹（prompt / 工具 / 产物） | 90 天（按需） |
| 审计关键事件（不可逆 / 越权） | 3+ 年 |
| 评估金标集 | 永久 |

---

## 7. 维度 5 · 回滚（Rollback · 出事用）

### 7.1 Agent 产物回滚

| 产物 | 回滚方式 |
|---|---|
| Code diff | `git revert` / 关闭 PR |
| 部署 | 镜像版本回退 / K8s rollout undo |
| 数据库迁移 | 配套 down migration |
| 配置 | GitOps revert |
| Feature flag | 关 flag（不需重部署） |

### 7.2 Agent 行为回滚（必要时）

> **不是回滚代码，而是回滚 agent 行为策略**。

- agent 跑了危险操作 → 关 agent 通道 → 人审 → 改 prompt/Rules → 重启
- 评估分数突降 → 暂停自动合并 → 回到 manual review → 修 Eval

### 7.3 不可逆操作的"软回滚"

| 操作 | 软回滚 |
|---|---|
| 删数据 | 备份 + 演练恢复（每月） |
| 动钱 | 复核窗口 + 撤销机制 |
| 对外发布 | 版本可下线 / 客户可降级 |
| 改线上配置 | 配置可秒还原（GitOps） |

---

## 8. 落地清单（企业级最少集）

### 8.1 必做（Week 1）

- [ ] agent 跑的所有 PR 自动打 label `agent-assisted`
- [ ] PR body 自动带 run_id 链接
- [ ] 关键文件改动 → 自动 +1 reviewer
- [ ] 不可逆操作 → 强制人二次确认（PR body + 审批流）

### 8.2 应做（Month 1）

- [ ] 接入 AgentOps / Langfuse，跑通轨迹记录
- [ ] 关键 5 指标进监控 + 告警
- [ ] 建 eval 金标集（≥ 30 条）
- [ ] CI 加 mutation testing（验证测试有效）

### 8.3 长期（Quarter 1）

- [ ] eval 跑分进 release gate
- [ ] 审计日志按法务要求导出 / 保留
- [ ] 模型升级走回放评估（不拍脑袋切）
- [ ] 团队月度 AI 复盘（指标 / 事故 / 改进）

---

## 9. 工具速查

| 能力 | 工具 |
|---|---|
| 轨迹 | AgentOps.ai / Langfuse / Arize / Helicone |
| 评估 | Promptfoo / Ragas / Braintrust / 自己脚本 |
| 监控 | Prometheus / Grafana / Datadog |
| 日志 | ELK / Loki / ClickHouse |
| 告警 | Alertmanager / PagerDuty / Opsgenie |
| 审计 | SIEM（Splunk / Elastic SIEM） |
| 编排（agent） | Temporal / Prefect / LangGraph Platform |
| Secret | HashiCorp Vault / AWS Secrets Manager |

---

## 10. 反模式（看到就停）

| 反模式 | 后果 | 改成什么 |
|---|---|---|
| "agent 跑完就完了" | 出事没法复盘 | 必记轨迹 + run_id 关联 commit |
| eval 凭感觉 | 升级翻车 | 建金标集 + 量化指标 |
| 不可逆操作没二次确认 | 出事救不回来 | 强制人确认 + feature flag |
| 监控只看模型指标 | 业务出错看不见 | agent 指标 + 业务指标 一起看 |
| 审计日志脱敏过度 | 出事查不到 | 关键字段按法务分级 |
| 模型升级拍脑袋 | 表现突降 | 回放评估 + 灰度 |
| 一次性大改 Eval | 没法对比趋势 | 锁定金标集，diff 增量 |

---

## 一句话判断

> **AI 代码进了生产，AgentOps 就是 SRE 体系**——轨迹 / 评估 / 监控 / 审计 / 回滚，一个都不能少。
> **没 AgentOps 的 AI Coding，是裸奔**。
