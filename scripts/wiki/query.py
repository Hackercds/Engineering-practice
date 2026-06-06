"""query.py — Wiki 本地搜索

简单的关键字搜索：扫描 wiki/*.md，找含查询词的页。
> 100 页时建议接入 qmd（https://github.com/tobi/qmd）做 BM25/vector 搜索。

用法：
    python scripts/wiki/query.py "<query>"

退出码：0 找到 / 1 没找到
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Windows GBK 终端兼容
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python query.py <query>")
        return 1

    query = sys.argv[1].lower()
    found: list[tuple[str, str, str]] = []  # (file, snippet, score)
    for p in sorted(WIKI.glob("*.md")):
        if p.name in {"CLAUDE.md", "log.md"}:
            continue
        text = p.read_text(encoding="utf-8")
        # 简单行级匹配
        for i, line in enumerate(text.splitlines(), 1):
            if query in line.lower():
                score = line.lower().count(query)
                found.append((p.name, f"L{i}: {line.strip()[:100]}", score))

    if not found:
        print(f"❌ 未找到：{query!r}")
        print("→ 看 wiki/index.md 找全目录")
        return 1

    found.sort(key=lambda x: -x[2])
    print(f"🔍 找到 {len(found)} 处匹配（按相关度）：\n")
    for fname, snippet, _ in found[:20]:
        print(f"  [{fname}]")
        print(f"    {snippet}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
