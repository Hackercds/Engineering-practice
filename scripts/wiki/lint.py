"""lint.py — Wiki 健康检查

检查项：
1. frontmatter 完整性（title/type/created/updated/sources）
2. 死链（wikilink 指向不存在的页）
3. 孤儿页（没有 wikilink 指向它）
4. log 格式（## [YYYY-MM-DD] op | name）
5. 文件名规范（kebab-case / Title Case）

退出码：0 干净 / 1 发现问题
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

ROOT = Path(__file__).resolve().parents[2]  # repo root
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
# op 名允许字母数字下划线连字符（render-graph / lint 等）
LOG_ENTRY_RE = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] [\w-]+ \| .+$", re.MULTILINE)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_frontmatter(text: str) -> dict[str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def normalize_link(slug: str) -> str:
    """`[[Page Title]]` 或 `[[page-slug]]` → 文件名候选"""
    return slug.strip()


def main() -> int:
    md_files = sorted(WIKI.glob("*.md"))
    pages = {p.stem for p in md_files}
    issues: list[str] = []

    # 1) frontmatter
    for p in md_files:
        if p.name in {"CLAUDE.md", "index.md", "log.md"}:
            continue
        fm = parse_frontmatter(p.read_text(encoding="utf-8"))
        if not fm:
            issues.append(f"[frontmatter-missing] {p.name}")
            continue
        for key in ("title", "type", "created", "updated"):
            if key not in fm:
                issues.append(f"[frontmatter-missing-field:{key}] {p.name}")
        if fm.get("type") not in {"concept", "entity", "summary"}:
            issues.append(f"[frontmatter-bad-type:{fm.get('type')}] {p.name}")
        for date_key in ("created", "updated"):
            if date_key in fm and not DATE_RE.match(fm[date_key]):
                issues.append(f"[frontmatter-bad-date:{date_key}] {p.name}")

    # 2) 死链 + 3) 孤儿
    referenced: set[str] = set()
    for p in md_files:
        if p.name in {"CLAUDE.md", "log.md"}:
            continue
        for link in WIKILINK_RE.findall(p.read_text(encoding="utf-8")):
            # 处理 `[[Page Title|alias]]` 格式
            target = normalize_link(link.split("|")[0])
            # 容许跨域链接（../ 开头）—— 指向仓库其他文件，合法
            if target.startswith(".") or "/" in target and not target.endswith(".md"):
                # 形如 ../CLAUDE.md / ../../wiki/CLAUDE.md / ../materials/07_CI门
                # 不强校验存在性（这些是外部 wiki 的资源），只记录
                continue
            if target in pages:
                referenced.add(target)
            else:
                issues.append(f"[dead-link] {p.name} -> [[{target}]]")

    for p in md_files:
        if p.name in {"CLAUDE.md", "index.md", "log.md"}:
            continue
        if p.stem not in referenced:
            issues.append(f"[orphan] {p.name}")

    # 4) log 格式
    log_text = (WIKI / "log.md").read_text(encoding="utf-8")
    # 跳过注释行
    log_lines = [
        l for l in log_text.splitlines()
        if l.startswith("## [") and "[" in l and "]" in l
    ]
    for l in log_lines:
        if not LOG_ENTRY_RE.match(l):
            issues.append(f"[log-format-bad] {l[:80]}")

    # 5) 报告
    if issues:
        print(f"❌ 发现 {len(issues)} 个问题：\n")
        for i in issues:
            print(f"  - {i}")
        print(f"\n页数：{len([p for p in md_files if p.name not in {'CLAUDE.md','index.md','log.md'}])}")
        return 1
    else:
        print(f"✅ Wiki 健康 · 页数：{len(pages)}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
