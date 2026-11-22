"""各檢查節點共用的讀檔、數字比對與報告輸出。"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW_TEXT = ROOT / "raw" / "text"

CLAIM_ID = re.compile(r"S\d+-c\d+")
CLAIM_HEADING = re.compile(r"^### (S\d+-c\d+)｜(.+?)\s*\{#([^}]+)\}\s*$")
EVIDENCE = re.compile(r"^> 證據（[^）]*）：「(.+)」\s*$")
MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")


def normalize(text: str) -> str:
    """比對證據用：統一全半形、引號、連字號，合併空白。"""
    text = unicodedata.normalize("NFKC", text)
    for a, b in {"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", "−": "-", "∼": "~"}.items():
        text = text.replace(a, b)
    return " ".join(text.split())


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, text[end + 5 :]


@dataclass
class Page:
    path: Path
    meta: dict
    body: str

    @property
    def rel(self) -> str:
        return self.path.relative_to(WIKI).as_posix()


def load_pages() -> list[Page]:
    pages = []
    for path in sorted(WIKI.rglob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        pages.append(Page(path, meta, body))
    return pages


@dataclass
class Claim:
    cid: str
    title: str
    anchor: str
    page: str
    evidence: list[str] = field(default_factory=list)
    explanation: list[str] = field(default_factory=list)

    def evidence_text(self) -> str:
        return self.title + " " + " ".join(self.evidence)


def parse_claims(page: Page) -> list[Claim]:
    claims: list[Claim] = []
    current: Claim | None = None
    for line in page.body.splitlines():
        m = CLAIM_HEADING.match(line)
        if m:
            current = Claim(m.group(1), m.group(2), m.group(3), page.rel)
            claims.append(current)
            continue
        if line.startswith("## "):
            current = None
            continue
        if current is None:
            continue
        e = EVIDENCE.match(line)
        if e:
            current.evidence.append(e.group(1))
        elif line.strip():
            current.explanation.append(line)
    return claims


def all_claims(pages: list[Page]) -> dict[str, Claim]:
    out = {}
    for page in pages:
        if page.meta.get("type") == "source":
            for claim in parse_claims(page):
                out[claim.cid] = claim
    return out


# ---- 數字比對 ----------------------------------------------------------------

_UNIT = {"萬": 1e4, "億": 1e8, "千": 1e3, "M": 1e6, "K": 1e3, "k": 1e3, "million": 1e6}
_NUM = re.compile(r"(?<![A-Za-z0-9.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*(萬|億|千|million|M|K|k)?(?![A-Za-z])")


def numbers(text: str) -> set[float]:
    """抽出文字裡的數值；『2,100 萬』與『21M』都算成 21000000。"""
    text = CLAIM_ID.sub(" ", text)
    text = re.sub(r"§[\d.]+", " ", text)
    text = MD_LINK.sub(lambda m: m.group(1) if not CLAIM_ID.fullmatch(m.group(1)) else " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"`[^`]*`", " ", text)
    found = set()
    for m in _NUM.finditer(text):
        value = float(m.group(1).replace(",", ""))
        if m.group(2):
            value *= _UNIT[m.group(2)]
        found.add(round(value, 6))
    return found


def fmt_num(value: float) -> str:
    return f"{value:g}" if value < 1e5 else f"{value:,.0f}"


# ---- 報告 --------------------------------------------------------------------


@dataclass
class Check:
    code: str
    name: str
    problems: list[str] = field(default_factory=list)
    checked: int = 0

    @property
    def ok(self) -> bool:
        return not self.problems


def write_report(checks: list[Check], node: str, out_dir: Path | None) -> bool:
    ok = all(c.ok for c in checks)
    lines = [f"# {node}：{'通過' if ok else '未通過'}", ""]
    lines += ["| 代號 | 檢查 | 檢查數 | 問題數 |", "| --- | --- | --- | --- |"]
    for c in checks:
        lines.append(f"| {c.code} | {c.name} | {c.checked} | {len(c.problems)} |")
    for c in checks:
        if c.problems:
            lines += ["", f"## {c.code} {c.name}", ""]
            lines += [f"- {p}" for p in c.problems]
    report = "\n".join(lines) + "\n"
    print(report)
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)
        stem = node.split("（")[0].strip().replace(" ", "_")
        (out_dir / f"{stem}.md").write_text(report, encoding="utf-8")
        data = [{"code": c.code, "name": c.name, "checked": c.checked, "problems": c.problems} for c in checks]
        (out_dir / f"{stem}.json").write_text(json.dumps({"node": node, "ok": ok, "checks": data}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return ok
