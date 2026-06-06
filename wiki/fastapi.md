---
title: fastapi
type: entity
entity_type: component
created: 2026-06-07
updated: 2026-06-07
sources: [code/backend/requirements.txt]
---

# fastapi

> 本项目后端框架。FastAPI 0.110+ · Pydantic v2。

## Key Features / Known Issues

- 自动 OpenAPI 文档（`/docs` `/openapi.json`）
- Pydantic v2 校验（`min_length` `max_length` `field_validator`）
- 内存存储（SPEC §2.2 明确不做持久化）

## Related Concepts

- [[todo-api]] — 用 FastAPI 实现
- [[Spec Driven Development]] — FastAPI 是 OpenAPI 契约的源头

## Sources

- `code/backend/requirements.txt`
- [FastAPI 官方](https://fastapi.tiangolo.com/)
