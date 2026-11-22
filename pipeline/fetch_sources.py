"""節點 1：取得資料。

依 raw/manifest.json 下載每篇原始資料，轉成純文字存到 raw/text/<id>.txt，
並把 SHA-256、取得時間、字數寫回清單。原始資料一旦取得就不再修改（Wiki 只讀不寫）。

用法：.venv/bin/python -I pipeline/fetch_sources.py [S1 S2 ...]
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import subprocess
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "raw" / "manifest.json"
FILES = ROOT / "raw" / "files"
TEXT = ROOT / "raw" / "text"
UA = "Mozilla/5.0 (X11; Linux x86_64) course-lab-fetcher"


class _TextOnly(HTMLParser):
    """把 HTML 轉成段落文字；略過 script、style、nav、footer。"""

    SKIP = {"script", "style", "noscript", "svg", "nav", "footer", "header"}
    BLOCK = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "br", "pre", "blockquote", "section", "article"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip_depth:
            self.skip_depth -= 1
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        lines = [" ".join(line.split()) for line in "".join(self.parts).splitlines()]
        out, blank = [], False
        for line in lines:
            if line:
                out.append(line)
                blank = False
            elif not blank:
                out.append("")
                blank = True
        return "\n".join(out).strip() + "\n"


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def to_text(kind: str, path: Path) -> str:
    if kind == "pdf":
        return subprocess.run(["pdftotext", "-enc", "UTF-8", str(path), "-"], check=True, capture_output=True, text=True).stdout
    raw = path.read_text(encoding="utf-8", errors="replace")
    if kind == "html":
        parser = _TextOnly()
        parser.feed(raw)
        return parser.text()
    return raw


def main(only: list[str]) -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    FILES.mkdir(parents=True, exist_ok=True)
    TEXT.mkdir(parents=True, exist_ok=True)
    for src in manifest["sources"]:
        if only and src["id"] not in only:
            continue
        ext = {"pdf": ".pdf", "html": ".html", "md": ".md"}[src["kind"]]
        file_path = FILES / f"{src['id']}{ext}"
        if not file_path.exists():
            file_path.write_bytes(download(src["fetch_url"]))
            src["retrieved_at"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
        data = file_path.read_bytes()
        src["sha256"] = hashlib.sha256(data).hexdigest()
        text = to_text(src["kind"], file_path)
        (TEXT / f"{src['id']}.txt").write_text(text, encoding="utf-8")
        src["text_chars"] = len(text)
        print(f"{src['id']}: {len(data):>9} bytes -> {len(text):>7} chars  {src['title'][:60]}")
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
