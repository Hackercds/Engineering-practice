"""ingest.py — 把 raw 资料编译为 wiki 页（半自动版）

用法：
    python scripts/wiki/ingest.py <raw-file-path>

做什么：
1. 读取 raw 资料
2. 写一个 summary 页到 wiki/<slug>.md
3. 提示 AI 去更新 / 新建 concept 与 entity 页
4. append log.md

注意：本脚本只做"机械部分"——真正的"读懂 + 写概念页"由 AI 完成。
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

# Windows GBK 终端兼容
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace("_", "-").replace("/", "-")


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python ingest.py <raw-file>")
        return 1

    src = Path(sys.argv[1])
    if not src.exists():
        print(f"❌ 找不到：{src}")
        return 1

    rel = src.relative_to(ROOT) if src.is_absolute() else src
    slug = slugify(src.stem)
    summary = WIKI / f"{slug}.md"

    if summary.exists():
        print(f"⚠️  {summary.name} 已存在，跳过")
        return 0

    today = date.today().isoformat()
    body = f"""---
title: {src.stem}
type: summary
created: {today}
updated: {today}
sources: [{rel.as_posix()}]
---

# {src.stem}（摘要）

> 自动从 `{rel.as_posix()}` 生成的占位摘要。
> **AI 需补全**：读源后写一段 200-300 字的摘要 + 关键概念链接。

## 来源
- `{rel.as_posix()}`

## 待 AI 补全
- [ ] 一句话定义
- [ ] 关键要点（3-5 条）
- [ ] 相关 wiki 页链接
"""
    summary.write_text(body, encoding="utf-8")
    print(f"✅ 已创建占位摘要：{summary.relative_to(ROOT)}")
    print("→ 下一步：让 AI 读源 + 补全 + 更新 index.md + 写新概念页（如有）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
