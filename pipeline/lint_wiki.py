"""Wiki 檢查（Lint）。

W1 frontmatter 欄位        W2 證據逐字出自原文        W3 主張格式
W4 數字有證據支撐          W5 引用的主張存在且連對    W6 站內連結與錨點
W7 孤兒頁                  W8 目錄完整                W9 log 格式
W10 每篇來源都被概念頁用到

用法：.venv/bin/python -I pipeline/lint_wiki.py [--out runs/<run>/]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    CLAIM_ID,
    MD_LINK,
    RAW_TEXT,
    WIKI,
    Check,
    all_claims,
    fmt_num,
    load_pages,
    normalize,
    numbers,
    parse_claims,
    write_report,
)

TYPES = {"source", "concept", "overview", "query", "discussion", "meta"}
LOG_ENTRY = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] [a-z]+ \| .+")
ATTR_ANCHOR = re.compile(r"\{#([^}]+)\}")
LIST_MARK = re.compile(r"^\s*(?:\d+\.|[-*])\s+")


def anchors_of(page) -> set[str]:
    return set(ATTR_ANCHOR.findall(page.body))


def resolve(page, target: str) -> tuple[Path, str]:
    path, _, anchor = target.partition("#")
    return (page.path.parent / path).resolve() if path else page.path.resolve(), anchor


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    pages = load_pages()
    by_path = {p.path.resolve(): p for p in pages}
    claims = all_claims(pages)
    raw_cache: dict[str, str] = {}

    w1 = Check("W1", "frontmatter 欄位")
    w2 = Check("W2", "證據逐字出自原文")
    w3 = Check("W3", "主張格式")
    w4 = Check("W4", "數字有證據支撐")
    w5 = Check("W5", "引用的主張存在且連對")
    w6 = Check("W6", "站內連結與錨點")
    w7 = Check("W7", "孤兒頁")
    w8 = Check("W8", "目錄完整")
    w9 = Check("W9", "log 格式")
    w10 = Check("W10", "每篇來源都被概念頁用到")

    inbound: dict[Path, set[str]] = {p.path.resolve(): set() for p in pages}
    cited_sources: set[str] = set()

    for page in pages:
        # W1
        w1.checked += 1
        need = ["title", "type", "updated"] + (["id", "url"] if page.meta.get("type") == "source" else [])
        missing = [k for k in need if not page.meta.get(k)]
        if missing:
            w1.problems.append(f"{page.rel}：缺少 {', '.join(missing)}")
        if page.meta.get("type") not in TYPES:
            w1.problems.append(f"{page.rel}：type「{page.meta.get('type')}」不在允許清單")

        # 來源頁：W2、W3、W4
        if page.meta.get("type") == "source":
            sid = page.meta.get("id", "")
            if not page.path.name.startswith(sid.lower() + "-"):
                w1.problems.append(f"{page.rel}：檔名開頭應為 {sid.lower()}-")
            raw_path = RAW_TEXT / f"{sid}.txt"
            if sid not in raw_cache:
                raw_cache[sid] = normalize(raw_path.read_text(encoding="utf-8")) if raw_path.exists() else ""
            raw = raw_cache[sid]
            seen = set()
            for claim in parse_claims(page):
                w3.checked += 1
                if not claim.cid.startswith(sid + "-"):
                    w3.problems.append(f"{claim.cid}：編號不屬於 {sid}")
                if claim.anchor != claim.cid.lower():
                    w3.problems.append(f"{claim.cid}：錨點應為 #{claim.cid.lower()}，實際是 #{claim.anchor}")
                if claim.cid in seen:
                    w3.problems.append(f"{claim.cid}：編號重複")
                seen.add(claim.cid)
                if not claim.evidence:
                    w3.problems.append(f"{claim.cid}：沒有證據")
                for quote in claim.evidence:
                    w2.checked += 1
                    q = normalize(quote)
                    if not raw:
                        w2.problems.append(f"{claim.cid}：找不到原文 raw/text/{sid}.txt")
                    elif q not in raw:
                        # 找出從哪個字開始對不上，方便修正
                        k = 0
                        while k < len(q) and q[: k + 1] in raw:
                            k += 1
                        w2.problems.append(f"{claim.cid}：證據不在原文中，前 {k} 字對得上，之後是「{q[k:k + 40]}…」")
                w4.checked += 1
                extra = numbers(claim.title + " " + " ".join(claim.explanation)) - numbers(" ".join(claim.evidence))
                if extra:
                    w4.problems.append(f"{claim.cid}：說明裡的數字 {', '.join(fmt_num(x) for x in sorted(extra))} 不在證據中")

        # 概念頁、總覽：W4（逐行）與 W5
        if page.meta.get("type") in {"concept", "overview"}:
            in_code = False
            for line in page.body.splitlines():
                if line.startswith("```"):
                    in_code = not in_code
                if in_code or line.startswith("#") or not line.strip():
                    continue
                text = LIST_MARK.sub("", line)
                cited = [m.group(1) for m in MD_LINK.finditer(text) if CLAIM_ID.fullmatch(m.group(1))]
                nums = numbers(text)
                if not nums:
                    continue
                w4.checked += 1
                support = set()
                for cid in cited:
                    if cid in claims:
                        support |= numbers(claims[cid].evidence_text())
                extra = nums - support
                if extra:
                    where = "沒有引用任何主張" if not cited else f"引用 {', '.join(cited)} 的證據裡沒有"
                    w4.problems.append(f"{page.rel}：數字 {', '.join(fmt_num(x) for x in sorted(extra))}（{where}）｜{text[:50]}")

        # 所有連結：W5、W6，順便統計 inbound
        for m in MD_LINK.finditer(page.body):
            label, target = m.group(1), m.group(2)
            if re.match(r"^[a-z]+:", target):
                continue
            w6.checked += 1
            path, anchor = resolve(page, target)
            if path not in by_path:
                w6.problems.append(f"{page.rel}：連結到不存在的檔案 {target}")
                continue
            if anchor and anchor not in anchors_of(by_path[path]):
                w6.problems.append(f"{page.rel}：{target} 的錨點 #{anchor} 不存在")
            if path != page.path.resolve() and page.path.name not in {"index.md", "log.md"}:
                inbound[path].add(page.rel)
            if CLAIM_ID.fullmatch(label):
                w5.checked += 1
                claim = claims.get(label)
                if not claim:
                    w5.problems.append(f"{page.rel}：引用不存在的主張 {label}")
                elif by_path[path].rel != claim.page or anchor != claim.anchor:
                    w5.problems.append(f"{page.rel}：{label} 應連到 {claim.page}#{claim.anchor}，實際是 {target}")
                elif page.meta.get("type") == "concept":
                    cited_sources.add(label.split("-")[0])

    # W7 孤兒頁
    for page in pages:
        if page.path.name in {"index.md", "log.md"}:
            continue
        w7.checked += 1
        if not inbound[page.path.resolve()]:
            w7.problems.append(f"{page.rel}：除了目錄以外，沒有任何頁面連到這頁")

    # W8 目錄完整
    index = next(p for p in pages if p.rel == "index.md")
    listed = {resolve(index, m.group(2))[0] for m in MD_LINK.finditer(index.body) if not re.match(r"^[a-z]+:", m.group(2))}
    for page in pages:
        if page.rel == "index.md":
            continue
        w8.checked += 1
        if page.path.resolve() not in listed:
            w8.problems.append(f"{page.rel}：沒有列在 index.md")

    # W9 log 格式
    log = next(p for p in pages if p.rel == "log.md")
    for line in log.body.splitlines():
        if line.startswith("## "):
            w9.checked += 1
            if not LOG_ENTRY.match(line):
                w9.problems.append(f"格式不符：{line}")

    # W10 每篇來源都被概念頁用到
    for page in pages:
        if page.meta.get("type") == "source":
            w10.checked += 1
            if page.meta["id"] not in cited_sources:
                w10.problems.append(f"{page.meta['id']}：沒有任何概念頁引用這篇的主張")

    ok = write_report([w1, w2, w3, w4, w5, w6, w7, w8, w9, w10], "lint_wiki（Wiki 檢查）", args.out)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
