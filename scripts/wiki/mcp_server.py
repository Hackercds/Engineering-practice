"""mcp_server.py — 可选：把 wiki 暴露为 MCP Resources

启动：python scripts/wiki/mcp_server.py
接入：Claude Desktop / Cursor MCP config 加：
  {"mcpServers": {"wiki": {"command": "python", "args": ["scripts/wiki/mcp_server.py"]}}}

需要：pip install mcp
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Resource, TextContent
except ImportError:
    print("❌ 缺 mcp 包：pip install mcp", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"

app = Server("llm-wiki")


@app.list_resources()
async def list_resources() -> list[Resource]:
    """列出所有 wiki 页作为可读资源"""
    out: list[Resource] = []
    for p in sorted(WIKI.glob("*.md")):
        out.append(Resource(
            uri=f"wiki://{p.stem}",
            name=p.stem,
            description=f"Wiki page: {p.stem}",
            mimeType="text/markdown",
        ))
    return out


@app.read_resource()
async def read_resource(uri: str) -> str:
    """读单个 wiki 页"""
    if not uri.startswith("wiki://"):
        raise ValueError(f"Unknown URI scheme: {uri}")
    slug = uri[len("wiki://"):]
    path = WIKI / f"{slug}.md"
    if not path.exists():
        raise FileNotFoundError(f"No wiki page: {slug}")
    return path.read_text(encoding="utf-8")


async def main() -> None:
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
