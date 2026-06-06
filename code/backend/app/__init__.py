"""待办事项 API（按 SPEC-001 实现）"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="SPEC-001 的可执行实现。",
)


# ---------- 数据模型 ----------

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)

    @field_validator("title")
    @classmethod
    def _strip_must_be_nonempty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title must not be blank")
        return v


class Todo(BaseModel):
    id: int
    title: str
    done: bool = False


# ---------- 内存存储（SPEC §2.2：不做持久化） ----------

_todos: list[Todo] = []
_next_id: int = 1


def _new_id() -> int:
    global _next_id
    nid = _next_id
    _next_id += 1
    return nid


# ---------- 端点（SPEC §4） ----------

@app.post("/todos", status_code=201, response_model=Todo)
def create_todo(payload: TodoCreate) -> Todo:
    """新建待办。空/仅空白/超长 → 422（Pydantic 自动）。"""
    todo = Todo(id=_new_id(), title=payload.title, done=False)
    _todos.append(todo)
    return todo


@app.get("/todos", response_model=list[Todo])
def list_todos() -> list[Todo]:
    """列出全部待办，按 id 升序。"""
    return sorted(_todos, key=lambda t: t.id)


@app.post("/todos/{todo_id}/done", response_model=Todo)
def mark_done(todo_id: int) -> Todo:
    """标记完成。id 不存在 → 404；重复调用幂等 → 200。"""
    for todo in _todos:
        if todo.id == todo_id:
            todo.done = True
            return todo
    raise HTTPException(status_code=404, detail="todo not found")
