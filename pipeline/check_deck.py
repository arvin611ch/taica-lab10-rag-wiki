"""簡報檢查。

內容（讀 deck/outline.json，對照 Wiki）
  D1 每個重點都有出處，或標明是比喻／例子    D2 引用的主張與 Wiki 頁存在
  D3 數字對得上引用的主張                    D4 名詞先定義後使用（依 wiki/glossary.md）
  D5 每個學習目標都有內容頁、測驗題與回顧    D6 份量：每頁最多 4 點、每點最多 40 字
畫面（用無頭瀏覽器開 docs/slides/index.html）
  D7 版面不溢出（1280×720，測驗題展開解說後也要放得下）
  D8 簡報裡的連結都連得到（檔案與錨點）      D9 鍵盤換頁可用
另外輸出 review_packet.md，交給獨立的 AI 審查（事實查核＋扮演新手作答）。

用法：.venv/bin/python -I pipeline/check_deck.py --out runs/<run>/ [--content-only]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WIKI, Check, all_claims, fmt_num, load_pages, numbers, source_years, write_report  # noqa: E402

OUTLINE = ROOT / "deck" / "outline.json"
DECK = ROOT / "docs" / "slides" / "index.html"
MAX_POINTS, MAX_CHARS = 4, 40
EXEMPT_TERM_KINDS = {"title", "agenda"}


def glossary() -> list[tuple[str, list[str]]]:
    terms = []
    for line in (WIKI / "glossary.md").read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0] not in {"名詞", "---"} and not set(cells[0]) <= {"-"}:
            aliases = [a.strip() for a in cells[1].split("、") if a.strip()]
            terms.append((cells[0], [cells[0]] + aliases))
    return terms


def uses(text: str, alias: str) -> bool:
    if re.fullmatch(r"[A-Za-z0-9 \-]+", alias):
        return re.search(rf"(?<![A-Za-z]){re.escape(alias)}(?![A-Za-z])", text, re.I) is not None
    return alias in text


def strings(obj) -> list[str]:
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, (int, float)) and not isinstance(obj, bool):
        return [f"{obj:g}"]
    if isinstance(obj, dict):
        return [s for k, v in obj.items() if k not in {"type", "tone", "refs", "ok"} for s in strings(v)]
    if isinstance(obj, list):
        return [s for v in obj for s in strings(v)]
    return []


def content_checks(outline: dict) -> list[Check]:
    pages = load_pages()
    rels = {p.rel for p in pages}
    claims = all_claims(pages)
    years = source_years()
    d1, d2, d3 = Check("D1", "每個重點都有出處或標明比喻／例子"), Check("D2", "引用的主張與 Wiki 頁存在"), Check("D3", "數字對得上引用的主張")
    d4, d5, d6 = Check("D4", "名詞先定義後使用"), Check("D5", "學習目標都有內容、測驗與回顧"), Check("D6", "份量（每頁 ≤4 點、每點 ≤40 字）")

    def support(refs):
        s = set()
        for r in refs:
            if r in claims:
                s |= numbers(claims[r].evidence_text()) | {years.get(r.split("-")[0])}
        return s

    terms = glossary()
    term_names = {t for t, _ in terms}
    introduced: dict[str, str] = {}
    covered = {o["id"]: {"content": 0, "quiz": 0, "summary": 0} for o in outline["objectives"]}

    for s in outline["slides"]:
        sid = s["id"]
        pts = s.get("points", [])
        # D2 Wiki 頁
        for w in s.get("wiki", []) + [w for p in pts for w in p.get("wiki", [])]:
            d2.checked += 1
            if w not in rels:
                d2.problems.append(f"{sid}：Wiki 頁 {w} 不存在")
        for p in pts:
            label = f"{sid}「{p['text'][:18]}…」"
            illustrative = p.get("kind") in {"analogy", "example"}
            # D1
            if s["kind"] in {"content", "summary"}:
                d1.checked += 1
                if not (p.get("refs") or p.get("wiki") or illustrative):
                    d1.problems.append(f"{label}：沒有出處，也沒有標成比喻或例子")
            # D2
            for r in p.get("refs", []):
                d2.checked += 1
                if r not in claims:
                    d2.problems.append(f"{label}：引用不存在的主張 {r}")
            # D3
            if not illustrative:
                nums = numbers(p["text"])
                if nums:
                    d3.checked += 1
                    extra = nums - support(p.get("refs", []))
                    if extra:
                        d3.problems.append(f"{label}：數字 {', '.join(fmt_num(x) for x in sorted(extra))} 不在引用的主張裡")
            # D6
            d6.checked += 1
            if len(p["text"]) > MAX_CHARS:
                d6.problems.append(f"{label}：{len(p['text'])} 字，超過 {MAX_CHARS} 字")
        if len(pts) > MAX_POINTS:
            d6.problems.append(f"{sid}：{len(pts)} 點，超過 {MAX_POINTS} 點")
        # D3 圖裡的數字
        vis = s.get("visual")
        if vis:
            vtext = " ".join(strings(vis))
            nums = numbers(vtext)
            if nums:
                d3.checked += 1
                if vis.get("refs"):
                    extra = nums - support(vis["refs"])
                    if extra:
                        d3.problems.append(f"{sid} 的圖（{vis['type']}）：數字 {', '.join(fmt_num(x) for x in sorted(extra))} 不在引用的主張裡")
                elif "示意" not in vis.get("note", ""):
                    d3.problems.append(f"{sid} 的圖（{vis['type']}）有數字，但沒有引用主張，也沒標成示意")
        # D4 名詞
        for t in s.get("introduces", []):
            if t not in term_names:
                d4.problems.append(f"{sid}：introduces 的「{t}」不在名詞表")
            elif t in introduced:
                d4.problems.append(f"{sid}：「{t}」已在 {introduced[t]} 定義過")
            else:
                introduced[t] = sid
        if s["kind"] not in EXEMPT_TERM_KINDS:
            text = " ".join([s.get("title", "")] + strings(pts) + strings(vis or {}) + strings(s.get("questions", [])))
            for term, aliases in terms:
                hit = next((a for a in aliases if uses(text, a)), None)
                if hit:
                    d4.checked += 1
                    if term not in introduced:
                        d4.problems.append(f"{sid}：用到「{hit}」（{term}），但還沒有任何一頁定義它")
        # D5
        if s["kind"] == "content" and s.get("objective") in covered:
            covered[s["objective"]]["content"] += 1
        for q in s.get("questions", []):
            if q.get("objective") in covered:
                covered[q["objective"]]["quiz"] += 1
            for r in q.get("refs", []):
                d2.checked += 1
                if r not in claims:
                    d2.problems.append(f"{sid} 測驗：引用不存在的主張 {r}")
        if s["kind"] == "summary":
            for p in pts:
                if p.get("objective") in covered:
                    covered[p["objective"]]["summary"] += 1
    for oid, c in covered.items():
        d5.checked += 1
        missing = [k for k, v in c.items() if not v]
        if missing:
            d5.problems.append(f"{oid}：缺少 {'、'.join({'content': '內容頁', 'quiz': '測驗題', 'summary': '回顧'}[m] for m in missing)}")
    return [d1, d2, d3, d4, d5, d6]


class _Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        if a.get("id"):
            self.ids.add(a["id"])


def page_checks(out_dir: Path | None) -> list[Check]:
    from playwright.sync_api import sync_playwright

    d7, d8, d9 = Check("D7", "版面不溢出（1280×720）"), Check("D8", "簡報裡的連結都連得到"), Check("D9", "鍵盤換頁可用")
    # D8：靜態檢查連結
    parser = _Links()
    parser.feed(DECK.read_text(encoding="utf-8"))
    id_cache: dict[Path, set[str]] = {}
    for href in sorted(set(parser.hrefs)):
        if re.match(r"^[a-z]+:", href):
            continue
        d8.checked += 1
        path, _, anchor = href.partition("#")
        target = (DECK.parent / path).resolve()
        if not target.exists():
            d8.problems.append(f"{href}：檔案不存在（是否還沒跑 build_site.py？）")
            continue
        if anchor:
            if target not in id_cache:
                p = _Links()
                p.feed(target.read_text(encoding="utf-8"))
                id_cache[target] = p.ids
            if anchor not in id_cache[target]:
                d8.problems.append(f"{href}：錨點不存在")

    shots = out_dir / "shots" if out_dir else None
    if shots:
        shots.mkdir(parents=True, exist_ok=True)
    measure = """(n) => {
      const s = document.querySelectorAll('.slide')[n];
      const box = s.getBoundingClientRect(); const foot = s.querySelector('footer.src').getBoundingClientRect();
      const bad = [];
      for (const el of s.querySelectorAll('*')) {
        if (el.closest('footer.src') || el.offsetParent === null) continue;
        const r = el.getBoundingClientRect();
        if (r.width === 0 && r.height === 0) continue;
        if (r.bottom > foot.top + 1 || r.right > box.right - 8 || r.left < box.left) {
          bad.push(`${el.tagName.toLowerCase()}.${el.className || ''}「${(el.innerText || el.textContent || '').trim().slice(0, 16)}」超出 ${Math.round(Math.max(r.bottom - foot.top, r.right - box.right + 8, box.left - r.left))}px`);
        }
      }
      for (const svg of s.querySelectorAll('svg')) {
        const sr = svg.getBoundingClientRect();
        for (const t of svg.querySelectorAll('text')) {
          const r = t.getBoundingClientRect();
          if (r.right > sr.right + 1 || r.left < sr.left - 1 || r.bottom > sr.bottom + 1 || r.top < sr.top - 1)
            bad.push(`svg 文字「${t.textContent.trim().slice(0, 16)}」超出圖框`);
        }
      }
      return bad;
    }"""
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 772})
        page.goto(DECK.as_uri())
        total = page.locator(".slide").count()
        for n in range(total):
            page.evaluate(f"show({n})")
            if page.locator(".slide.active .quiz > .q").count():
                # 測驗頁：每題點一個錯的答案，讓解說展開後再量
                for q in page.locator(".slide.active .quiz > .q").all():
                    q.locator('.choice[data-ok="0"]').first.click()
            d7.checked += 1
            bad = page.evaluate(measure, n)
            sid = page.locator(".slide.active").get_attribute("id")
            if bad:
                leaf = [b for b in bad][:3]
                d7.problems.append(f"第 {n + 1} 頁（{sid}）：{len(bad)} 個元素超出內容區，例如 " + "；".join(leaf))
            if shots:
                page.screenshot(path=str(shots / f"{n + 1:02d}-{sid}.png"))
        # D9
        page.evaluate("show(0)")
        page.keyboard.press("ArrowRight")
        d9.checked += 1
        if page.locator("#count").inner_text().strip() != f"2 / {total}":
            d9.problems.append("按 → 之後沒有到第 2 頁")
        page.keyboard.press("End")
        d9.checked += 1
        if page.locator("#count").inner_text().strip() != f"{total} / {total}":
            d9.problems.append("按 End 之後沒有到最後一頁")
        browser.close()
    return [d7, d8, d9]


def review_packet(outline: dict, out_dir: Path) -> None:
    """給獨立 AI 審查的材料：A 部分只有簡報文字（新手測試用），B 部分附上引用主張（事實查核用）。"""
    claims = all_claims(load_pages())
    a, b = ["# A. 簡報文字（不含答案）", ""], ["# B. 每個重點與它引用的 Wiki 主張", ""]
    for i, s in enumerate(outline["slides"], 1):
        a.append(f"## 第 {i} 頁：{s['title']}")
        for p in s.get("points", []):
            tag = {"analogy": "〔比喻〕", "example": "〔例子〕", "project": "〔本專案說明〕"}.get(p.get("kind"), "")
            a.append(f"- {tag}{p['text']}")
            if p.get("refs"):
                b.append(f"- 第 {i} 頁「{p['text']}」")
                for r in p["refs"]:
                    c = claims[r]
                    b.append(f"  - {r}｜{c.title}｜證據：{' / '.join(c.evidence)}")
        if s["kind"] == "agenda":
            a += [f"- 目標 {o['id']}：{o['text']}" for o in outline["objectives"]] + [f"- 路線：{'→'.join(s['agenda'])}"]
        vis = s.get("visual")
        if vis and vis["type"] == "faithfulness":
            marks = "；".join(f"{st['text']}（{'有依據 ✓' if st['ok'] else '沒依據 ✗'}）" for st in vis["statements"])
            good = sum(st["ok"] for st in vis["statements"])
            a.append(f"- 〔圖：faithfulness〕{vis['note']}｜答案：{vis['answer']}｜拆句：{marks}｜忠實度 {good}/{len(vis['statements'])}")
        elif vis:
            a.append(f"- 〔圖：{vis['type']}〕" + "；".join(strings(vis))[:400])
        for q in s.get("questions", []):
            a.append(f"- 題目：{q['q']}　選項：" + "／".join(f"{'ABCD'[k]}. {c}" for k, c in enumerate(q["choices"])))
        a.append("")
    (out_dir / "review_packet.md").write_text("\n".join(a + [""] + b) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path)
    ap.add_argument("--content-only", action="store_true", help="只跑 D1–D6（不開瀏覽器）")
    args = ap.parse_args()
    os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(Path.home() / ".cache" / "pw-x86"))
    outline = json.loads(OUTLINE.read_text(encoding="utf-8"))
    checks = content_checks(outline)
    if not args.content_only:
        checks += page_checks(args.out)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        review_packet(outline, args.out)
    name = "check_outline（大綱檢查）" if args.content_only else "check_deck（簡報檢查）"
    return 0 if write_report(checks, name, args.out) else 1


if __name__ == "__main__":
    sys.exit(main())
