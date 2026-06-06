"""wiki_ask.py — 按需查询 wiki（Claude 主动调，避免默认全读爆 context）

为什么有这个脚本：
- Wiki 几十页时，Claude 默认加载会爆 context window
- 改用"按需检索"：Claude 想查时调本脚本，**只返回相关页摘要**

用法：
    python scripts/wiki/wiki_ask.py "<query>"

行为：
1. 检查 wiki/.wiki-enabled 标记文件——不存在直接退出（Wiki 关闭）
2. 读 wiki/index.md 拿页列表
3. 关键词匹配每个页的 frontmatter.title + 第一段
4. 打印前 N 条匹配（默认 3 条），每条只显示 title + 一句话 + 路径

退出码：
    0 找到 / 1 没找到 / 2 Wiki 未启用
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
ENABLED_FLAG = WIKI / ".wiki-enabled"
TOP_N = 3

# Windows GBK 终端兼容
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def main() -> int:
    if not ENABLED_FLAG.exists():
        print("[wiki disabled] 未找到 wiki/.wiki-enabled，跳过", file=sys.stderr)
        return 2

    if len(sys.argv) < 2:
        print("用法: python wiki_ask.py <query>")
        return 1

    query = sys.argv[1].lower()
    matches: list[tuple[int, Path, str, str]] = []  # (score, file, title, first_para)

    for p in sorted(WIKI.glob("*.md")):
        if p.name in {"CLAUDE.md", "log.md", "index.md"}:
            continue
        text = p.read_text(encoding="utf-8")

        # 取 frontmatter title
        m = re.match(r"^---\n.*?title:\s*(.+?)\n.*?---\n", text, re.DOTALL)
        title = m.group(1).strip() if m else p.stem

        # 取第一段
        body_after_fm = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
        first_para = ""
        for line in body_after_fm.splitlines():
            if line.strip().startswith("#"):
                continue
            if line.strip():
                first_para = line.strip()[:120]
                break

        # 评分：title 命中权重高
        score = title.lower().count(query) * 5
        score += first_para.lower().count(query) * 2
        score += text.lower().count(query)  # 全文命中，权重合理
        if query in title.lower():
            score += 10  # title 包含子串必上榜

        if score > 0:
            matches.append((score, p, title, first_para))

    matches.sort(key=lambda x: -x[0])
    matches = matches[:TOP_N]

    if not matches:
        print(f"无匹配: {query!r}")
        return 1

    print(f"找到 {len(matches)} 条相关（按相关度）：\n")
    for score, p, title, snippet in matches:
        print(f"  [{p.name}] {title}")
        print(f"    {snippet}…")
        print(f"    全文: {p.relative_to(ROOT)}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
