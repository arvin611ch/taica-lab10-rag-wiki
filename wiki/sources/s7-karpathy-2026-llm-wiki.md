---
id: S7
title: S7｜Karpathy 2026：LLM Wiki
type: source
url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
updated: 2026-11-23
---
# S7｜Karpathy 2026：LLM Wiki

**原文：** Andrej Karpathy, *LLM Wiki*（GitHub Gist 構想文件）. <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>

**一句話摘要：** 與其每次提問都讓 RAG 重新從原始文件找片段，不如讓 LLM 事先把資料整理成一個互相連結、持續維護的 Wiki。本專案就是照這個構想做的。

## 重點

### S7-c1｜一般 RAG 每次提問都從頭找資料，知識沒有累積 {#s7-c1}

> 證據（The core idea）：「the LLM is rediscovering knowledge from scratch on every question. There's no accumulation.」

白話說明：見 [LLM Wiki 與 RAG 的差別](../concepts/llm-wiki-vs-rag.md)。

### S7-c2｜LLM Wiki 讓 LLM 逐步建立並維護一個持續存在的 Wiki {#s7-c2}

> 證據（The core idea）：「the LLM **incrementally builds and maintains a persistent wiki**」

白話說明：新增一篇資料時，LLM 不只是存起來等人查，而是讀完、整理、更新相關頁面，並標出新舊資料的矛盾。

### S7-c3｜三層結構：原始資料（不修改）、Wiki（LLM 寫）、規則檔（規定格式與流程） {#s7-c3}

> 證據（Architecture）：「There are three layers:」

> 證據（Architecture）：「These are immutable — the LLM reads from them but never modifies them.」

白話說明：本專案的對應是 `raw/`、`wiki/` 與 `AGENTS.md`。

### S7-c4｜三種操作：Ingest（加入資料）、Query（提問）、Lint（健康檢查） {#s7-c4}

> 證據（Operations）：「Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search.」

白話說明：上面這段是 Lint 要找的問題清單。本專案的 `pipeline/lint_wiki.py` 實作了其中可以用程式判斷的部分（孤兒頁、壞連結、缺頁），並加上「證據必須逐字出自原文」的檢查。

### S7-c5｜好的查詢結果可以存回 Wiki，簡報也是查詢結果的一種 {#s7-c5}

> 證據（Operations）：「**good answers can be filed back into the wiki as new pages.**」

> 證據（Operations）：「Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (Marp), a chart (matplotlib), a canvas.」

白話說明：本專案的簡報大綱存在 [查詢紀錄：教學簡報大綱](../queries/deck-outline.md)。

## 這篇沒有強調的部分

Obsidian、qmd 等工具建議，本專案沒有使用。

## 用到這篇的頁面

[LLM Wiki 與 RAG 的差別](../concepts/llm-wiki-vs-rag.md)
