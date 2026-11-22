---
title: LLM Wiki 與 RAG 的差別
type: concept
updated: 2026-11-23
---
# LLM Wiki 與 RAG 的差別

**一句話定義：** RAG 在每次提問時才去原始文件找片段；LLM Wiki 則讓 LLM 事先把原始文件整理成互相連結的 Wiki 頁面，之後提問時先查 Wiki。

## 白話解釋

| | 一般 RAG | LLM Wiki |
| --- | --- | --- |
| 什麼時候整理知識 | 每次提問時臨時找 | 加入資料時就整理好 |
| 知識會不會累積 | 不會，每次從頭找 | 會，頁面持續更新 |
| 矛盾與交叉引用 | 每次重新發現 | 整理時就標記 |
| 需要的工具 | 切塊、向量資料庫 | Markdown 檔案、目錄頁、規則檔 |

比喻：RAG 像每次考試前才翻原文書；LLM Wiki 像平常就把讀過的書整理成筆記，考試時翻筆記，筆記上還標了出處。

兩者不衝突：Wiki 變大以後，也可以對 Wiki 頁面做 RAG。本專案的資料量不大，用目錄頁就夠了。

## 來源怎麼說

- 一般 RAG 每次都從頭找，知識沒有累積。[S7-c1](../sources/s7-karpathy-2026-llm-wiki.md#s7-c1)
- LLM Wiki 讓 LLM 逐步建立並維護 Wiki。[S7-c2](../sources/s7-karpathy-2026-llm-wiki.md#s7-c2)
- 三層結構與三種操作。[S7-c3](../sources/s7-karpathy-2026-llm-wiki.md#s7-c3)、[S7-c4](../sources/s7-karpathy-2026-llm-wiki.md#s7-c4)
- 查詢結果（例如簡報）可以存回 Wiki。[S7-c5](../sources/s7-karpathy-2026-llm-wiki.md#s7-c5)

## 相關頁面

[檢索增強生成](rag.md)、[總覽](../overview.md)
