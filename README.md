# RAG 入門：LLM Wiki × 教學 HTML 簡報

陽明交大 113611097 百川 江晟維｜TAICA Lab 10

先照 Karpathy 的〈LLM Wiki〉構想，讓 Claude Code 把 7 篇關於檢索增強生成（RAG）的資料整理成一個每句話都能追到原文的 Wiki，再只用這個 Wiki 產生一份給沒學過機器學習的大學生看的教學簡報。

- **網站首頁：** https://arvin611ch.github.io/taica-lab10-rag-wiki/
- **教學簡報：** https://arvin611ch.github.io/taica-lab10-rag-wiki/slides/
- **LLM Wiki：** https://arvin611ch.github.io/taica-lab10-rag-wiki/wiki/
- **流程設計與反思：** https://arvin611ch.github.io/taica-lab10-rag-wiki/workflow.html
- **執行與檢查紀錄：** https://arvin611ch.github.io/taica-lab10-rag-wiki/runs/
- **規則檔（schema）：** [AGENTS.md](AGENTS.md)

## 專案結構

```text
AGENTS.md                 Wiki 規則檔：頁面格式、操作流程、流程圖 v1/v2
raw/manifest.json         7 篇原始資料的網址、取得時間、SHA-256（全文只留本機，不公開）
wiki/                     LLM Wiki（Markdown）：來源頁、概念頁、名詞表、總覽、目錄、log、討論與查詢紀錄
deck/outline.json         簡報大綱：每個重點都附 Wiki 主張編號，或標成比喻／例子／本專案說明
pipeline/                 流程中的程式節點與檢查關卡
  fetch_sources.py        ① 取得資料
  lint_wiki.py            ④ 單頁檢查（--page）與 ⑤ Wiki 檢查
  claims_packet.py        ④ AI 主張審查的材料
  check_deck.py           ⑧ 大綱檢查（--content-only）與 ⑩ 畫面檢查、⑪ AI 審查材料
  render_deck.py          ⑨ 產生簡報
  build_site.py           產生 GitHub Pages 網站 docs/
report/                   網站首頁、流程與反思頁、流程圖
runs/                     每次執行的檢查報告與 AI 審查原文
docs/                     產生後的網站（GitHub Pages 從 main 的 /docs 發布）
```

## 重跑

需要 Python 3.10+、`markdown`、`playwright`（畫面檢查用）。

```bash
uv venv .venv && uv pip install --python .venv/bin/python markdown==3.7 playwright==1.64.1
.venv/bin/python -m playwright install chromium
.venv/bin/python -I pipeline/fetch_sources.py           # 下載原始資料到 raw/（本機）
.venv/bin/python -I pipeline/lint_wiki.py               # Wiki 檢查
.venv/bin/python -I pipeline/check_deck.py --content-only   # 大綱檢查
.venv/bin/python -I pipeline/render_deck.py             # 產生簡報
.venv/bin/python -I pipeline/build_site.py              # 產生網站
.venv/bin/python -I pipeline/check_deck.py --out runs/new/  # 畫面檢查＋截圖＋AI 審查材料
```

原始資料的版權屬於原作者。本專案只在 Wiki 中引用短句作為證據，並附上原文連結。
