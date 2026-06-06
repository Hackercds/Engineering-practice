<!-- .github/PULL_REQUEST_TEMPLATE.md -->

## 关联

- **Spec**：[docs/spec/SPEC-XXX.md](../docs/spec/SPEC-XXX.md)
- **Issue**：#XXX
- **ADR**（如有）：[docs/adr/XXXX.md](../docs/adr/XXXX.md)

## 动机

为什么改？改了什么问题？背景是什么？

## 改动

- 改动 1
- 改动 2
- 改动 3

## 影响范围

- 影响的下游 / 调用方：
- 是否需要数据迁移：
- 是否需要客户端升级：
- 是否需要发公告 / changelog：

## 测试

- 单元 / 集成：
- 契约（OpenAPI）：
- E2E（关键旅程）：
- 覆盖率：__%（降覆盖需说明）
- **故意改坏自检**：✅ / ❌（描述）

## 风险与回滚

- **风险等级**：低 / 中 / 高 / **不可逆**
- **不可逆操作**：（无 / 列出 + 确认人）
- **回滚方案**：
- **feature flag**：

## 文档

- README / ADR / Runbook / Changelog：（已更新 / N/A）

## Checklist（agent-assisted PR 必勾）

- [ ] 本 PR 由 AI 协助完成，run_id：<run_id>
- [ ] CI 12 门硬关全过（test / contract / lint / security / build）
- [ ] AI 自审 prompt 已跑（[06 §第一关](../materials/06_审查双关_prompt与checklist.md)）
- [ ] 上方所有强制项已勾选
- [ ] 至少 1 位 reviewer approve（**高风险 2 位**）
- [ ] 已读 [AGENTS.md](../AGENTS.md)
