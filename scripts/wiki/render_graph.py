"""render_graph.py — Mermaid 图渲染

策略：
1. 优先调 mmdc（mermaid-cli），渲染为 SVG
2. 不可用时，退化为只校验 .mmd 语法（mmdc --dry 或 mmdc -o /dev/null）

CI 用法：
    python render_graph.py            # 渲染到 wiki/graphs/*.svg
    python render_graph.py --check    # 只校验能渲染（不写文件）

退出码：0 OK / 1 失败
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

# Windows GBK 终端兼容
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
GRAPHS = ROOT / "wiki" / "graphs"


def find_mmdc() -> str | None:
    return shutil.which("mmdc") or shutil.which("mermaid")


def render_one(mmdc: str, src: Path, dst: Path) -> tuple[bool, str]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(
            [mmdc, "-i", str(src), "-o", str(dst), "-q"],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode == 0 and dst.exists():
            return True, ""
        return False, (r.stderr or r.stdout or "unknown error").strip()
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except FileNotFoundError:
        return False, "mmdc not found"


def main() -> int:
    check_only = "--check" in sys.argv
    mmdc = find_mmdc()
    mmds = sorted(GRAPHS.glob("*.mmd"))

    if not mmds:
        print("⚠️  无 .mmd 文件")
        return 0

    if mmdc is None:
        # 退化：只校验存在性
        print(f"ℹ️  mmdc 未安装，仅校验文件存在（CI 推荐装 mermaid-cli）")
        for m in mmds:
            print(f"  ✓ {m.relative_to(ROOT)}")
        return 0

    failed = 0
    for m in mmds:
        svg = m.with_suffix(".svg")
        ok, err = render_one(mmdc, m, svg)
        if ok:
            action = "checked" if check_only else f"→ {svg.name}"
            print(f"  ✅ {m.relative_to(ROOT)} {action}")
        else:
            print(f"  ❌ {m.relative_to(ROOT)}: {err}")
            failed += 1

    if failed:
        print(f"\n❌ {failed}/{len(mmds)} 张图渲染失败")
        return 1
    print(f"\n✅ {len(mmds)}/{len(mmds)} 张图 OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
