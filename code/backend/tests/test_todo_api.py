"""SPEC-001 端到端测试（happy path 3 + 边界 5 = 8 条 · 与 SPEC §5 一一对应）"""
from __future__ import annotations

from fastapi.testclient import TestClient

from app import _todos, app  # noqa: E402  sys.path 由 pytest 注入

client = TestClient(app)


def _reset() -> None:
    """每个测试前清空内存存储。"""
    _todos.clear()
    import app as _app

    _app._next_id = 1  # type: ignore[attr-defined]


# ---------- happy path（3 条） ----------

def test_create_todo_happy() -> None:
    _reset()
    r = client.post("/todos", json={"title": "买菜"})
    assert r.status_code == 201
    body = r.json()
    assert body["id"] == 1
    assert body["title"] == "买菜"
    assert body["done"] is False


def test_list_todos_happy() -> None:
    _reset()
    client.post("/todos", json={"title": "a"})
    client.post("/todos", json={"title": "b"})
    r = client.get("/todos")
    assert r.status_code == 200
    assert len(r.json()) == 2
    assert [t["id"] for t in r.json()] == [1, 2]


def test_mark_done_happy() -> None:
    _reset()
    client.post("/todos", json={"title": "a"})
    r = client.post("/todos/1/done")
    assert r.status_code == 200
    assert r.json()["done"] is True


# ---------- 边界（5 条 · SPEC §5） ----------

def test_blank_title_rejected_422() -> None:
    _reset()
    r = client.post("/todos", json={"title": ""})
    assert r.status_code == 422


def test_whitespace_only_title_rejected_422() -> None:
    _reset()
    r = client.post("/todos", json={"title": "   "})
    assert r.status_code == 422


def test_overlong_title_rejected_422() -> None:
    _reset()
    r = client.post("/todos", json={"title": "x" * 101})
    assert r.status_code == 422


def test_mark_nonexistent_id_returns_404() -> None:
    _reset()
    r = client.post("/todos/999/done")
    assert r.status_code == 404


def test_mark_done_is_idempotent() -> None:
    _reset()
    client.post("/todos", json={"title": "a"})
    r1 = client.post("/todos/1/done")
    r2 = client.post("/todos/1/done")
    assert r1.status_code == 200 and r1.json()["done"] is True
    assert r2.status_code == 200 and r2.json()["done"] is True
