"""產生 GitHub Pages 網站 docs/。

wiki/**/*.md   → docs/wiki/**/*.html（加上導覽列與「連到這頁的頁面」）
report/*.md    → docs/*.html（首頁、流程與反思）
runs/**/*.md   → docs/runs/**/*.html（每次執行的檢查紀錄）
簡報 docs/slides/index.html 由 render_deck.py 產生，這裡不動。

用法：.venv/bin/python -I pipeline/build_site.py
"""

from __future__ import annotations

import re
import sys
from html import escape
from pathlib import Path

import markdown

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MD_LINK, ROOT, WIKI, parse_frontmatter  # noqa: E402

DOCS = ROOT / "docs"
REPORT = ROOT / "report"
RUNS = ROOT / "runs"
TYPE_LABEL = {"source": "來源頁", "concept": "概念頁", "overview": "總覽", "query": "查詢紀錄", "discussion": "討論紀錄", "meta": "Wiki"}

CSS = """
:root{--paper:#fffdf8;--ink:#1d2433;--muted:#5b6475;--line:#e2dccf;--accent:#0f6e6e;--accent-soft:#e3f1ef;--warm:#c2410c}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;line-height:1.75;font-size:17px}
header.top{border-bottom:1px solid var(--line);background:#fff}
header.top .in{max-width:1000px;margin:0 auto;padding:12px 20px;display:flex;flex-wrap:wrap;gap:6px 18px;align-items:center}
header.top b{font-size:18px;margin-right:12px}
header.top a{color:var(--accent);text-decoration:none}
header.top a:hover{text-decoration:underline}
main{max-width:1000px;margin:0 auto;padding:24px 20px 60px}
.badge{display:inline-block;font-size:13px;font-weight:700;color:#fff;background:var(--accent);border-radius:6px;padding:0 8px;margin-right:8px}
.meta{color:var(--muted);font-size:14px}
h1{font-size:32px;line-height:1.3;margin:10px 0 18px}
h2{font-size:24px;margin:34px 0 10px;padding-bottom:4px;border-bottom:1px solid var(--line)}
h3{font-size:19px;margin:26px 0 8px;scroll-margin-top:12px}
h3:target{background:#fff4d6;border-radius:6px}
a{color:var(--accent)}
blockquote{margin:10px 0;padding:8px 14px;border-left:4px solid var(--accent);background:var(--accent-soft);border-radius:0 8px 8px 0;font-size:15px}
blockquote p{margin:0}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:15px;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}
th{background:#f3efe6}
code{background:#f1eee6;padding:1px 5px;border-radius:4px;font-size:14px}
pre{background:#1f2430;color:#e8e8e8;padding:14px;border-radius:8px;overflow-x:auto;font-size:14px;line-height:1.5}
pre code{background:none;padding:0;color:inherit}
.backlinks{margin-top:40px;padding:14px 18px;background:#f6f3ec;border-radius:10px;font-size:15px}
.backlinks b{display:block;margin-bottom:6px}
img,svg{max-width:100%;height:auto}
footer.site{max-width:1000px;margin:0 auto;padding:20px;color:var(--muted);font-size:13px;border-top:1px solid var(--line)}
"""


def md_to_html(text: str) -> str:
    html = markdown.markdown(text, extensions=["tables", "attr_list", "fenced_code", "sane_lists"])
    # 站內 .md 連結改成 .html
    return re.sub(r'href="(?![a-z]+:)([^"#]*?)\.md(#[^"]*)?"', lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', html)


def page(title: str, body: str, depth: int, meta_line: str = "") -> str:
    up = "../" * depth
    nav = [("首頁", "index.html"), ("Wiki 目錄", "wiki/index.html"), ("總覽", "wiki/overview.html"), ("名詞表", "wiki/glossary.html"),
           ("教學簡報", "slides/index.html"), ("流程與反思", "workflow.html"), ("執行紀錄", "runs/index.html")]
    links = "".join(f'<a href="{up}{href}">{escape(name)}</a>' for name, href in nav)
    return f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}｜RAG 入門 LLM Wiki</title><link rel="stylesheet" href="{up}assets/site.css"></head>
<body><header class="top"><div class="in"><b>RAG 入門 LLM Wiki</b>{links}</div></header>
<main>{meta_line}{body}</main>
<footer class="site">TAICA Lab 10｜陽明交大 113611097 江晟維｜Wiki 由 Claude Code 依 <a href="https://github.com/arvin611ch/taica-lab10-rag-wiki/blob/main/AGENTS.md">AGENTS.md</a> 維護；原始資料版權屬原作者，本站只引用短句並附連結。</footer>
</body></html>
"""


def build_wiki() -> int:
    files = sorted(WIKI.rglob("*.md"))
    parsed = {f: parse_frontmatter(f.read_text(encoding="utf-8")) for f in files}
    inbound: dict[Path, set[Path]] = {f.resolve(): set() for f in files}
    for f, (_, body) in parsed.items():
        for m in MD_LINK.finditer(body):
            target = m.group(2)
            if re.match(r"^[a-z]+:", target):
                continue
            path = (f.parent / target.split("#")[0]).resolve() if not target.startswith("#") else f.resolve()
            if path in inbound and path != f.resolve():
                inbound[path].add(f)
    for f, (meta, body) in parsed.items():
        rel = f.relative_to(WIKI)
        out = DOCS / "wiki" / rel.with_suffix(".html")
        out.parent.mkdir(parents=True, exist_ok=True)
        depth = len(rel.parts)  # docs/wiki/<...>/x.html → 回到 docs/ 的層數
        label = TYPE_LABEL.get(meta.get("type", ""), "")
        meta_line = f'<p class="meta"><span class="badge">{label}</span>更新：{escape(meta.get("updated", ""))}'
        if meta.get("url"):
            meta_line += f'｜原文：<a href="{escape(meta["url"])}">{escape(meta["url"])}</a>'
        meta_line += "</p>"
        html = md_to_html(body)
        backs = sorted(inbound[f.resolve()], key=lambda p: p.as_posix())
        if backs:
            items = "、".join(f'<a href="{Path("../" * (len(rel.parts) - 1) + b.relative_to(WIKI).with_suffix(".html").as_posix()).as_posix()}">{escape(parsed[b][0].get("title", b.stem))}</a>' for b in backs)
            html += f'<div class="backlinks"><b>連到這頁的頁面（{len(backs)}）</b>{items}</div>'
        out.write_text(page(meta.get("title", rel.stem), html, depth, meta_line), encoding="utf-8")
    return len(files)


def build_report() -> int:
    n = 0
    for f in sorted(REPORT.glob("*.md")):
        meta, body = parse_frontmatter(f.read_text(encoding="utf-8"))
        html = md_to_html(body)
        graph = REPORT / "graph_v2.svg"
        if "@@GRAPH@@" in html and graph.exists():  # 流程圖直接內嵌，不另外載入
            html = html.replace("@@GRAPH@@", graph.read_text(encoding="utf-8"))
        (DOCS / f.with_suffix(".html").name).write_text(page(meta.get("title", f.stem), html, 0), encoding="utf-8")
        n += 1
    return n


def build_runs() -> int:
    n = 0
    for f in sorted(RUNS.rglob("*.md")):
        rel = f.relative_to(RUNS)
        out = DOCS / "runs" / rel.with_suffix(".html")
        out.parent.mkdir(parents=True, exist_ok=True)
        meta, body = parse_frontmatter(f.read_text(encoding="utf-8"))
        title = meta.get("title") or (body.splitlines()[0].lstrip("# ") if body else rel.stem)
        out.write_text(page(title, md_to_html(body), len(rel.parts)), encoding="utf-8")
        n += 1
    return n


def main() -> int:
    (DOCS / "assets").mkdir(parents=True, exist_ok=True)
    (DOCS / "assets" / "site.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print(f"wiki {build_wiki()} 頁、報告 {build_report()} 頁、執行紀錄 {build_runs()} 頁 → docs/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
