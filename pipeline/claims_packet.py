"""v2 新增：Wiki 階段的 AI 主張審查材料。

把來源頁的每條主張（中文標題、白話說明、英文證據）整理成一份檔案，交給沒看過製作過程的 AI，
核對「中文有沒有比英文證據說得更強、或多出證據沒有的內容」。程式只能比對字面與數字，這一步補語意。

用法：.venv/bin/python -I pipeline/claims_packet.py runs/<run>/claims_packet.md [wiki/sources/<slug>.md ...]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_pages, parse_claims  # noqa: E402


def main(out: Path, only: list[Path]) -> int:
    targets = {p.resolve() for p in only}
    lines = ["# Wiki 主張審查材料", "", "每條主張：中文標題、白話說明、英文證據（逐字出自原文）。", ""]
    n = 0
    for page in load_pages():
        if page.meta.get("type") != "source" or (targets and page.path.resolve() not in targets):
            continue
        lines += [f"## {page.meta['title']}", ""]
        for c in parse_claims(page):
            n += 1
            lines.append(f"### {c.cid}｜{c.title}")
            lines += [f"- 證據：{e}" for e in c.evidence]
            lines += [f"- 說明：{x}" for x in c.explanation]
            lines.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{n} 條主張 → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), [Path(a) for a in sys.argv[2:]]))
