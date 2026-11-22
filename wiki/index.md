---
title: RAG 入門 LLM Wiki：目錄
type: meta
updated: 2026-11-23
---
# RAG 入門 LLM Wiki：目錄

主題：檢索增強生成（RAG）。讀者：沒學過機器學習的大學生。7 篇原始資料，所有事實都附主張編號，可追到原文。規則見 [AGENTS.md](https://github.com/arvin611ch/taica-lab10-rag-wiki/blob/main/AGENTS.md)。

## 總覽

- [總覽：RAG 是什麼、為什麼需要、會在哪裡出錯](overview.md) — 7 篇來源串成的故事線，也是簡報骨架
- [名詞表](glossary.md) — 16 個名詞的一句話定義，簡報檢查會用到

## 概念

- [檢索增強生成（RAG）](concepts/rag.md) — 先找資料再回答；建索引、檢索、生成三步
- [參數記憶與幻覺](concepts/parametric-memory.md) — 為什麼只靠模型記憶不夠
- [檢索器](concepts/retriever.md) — 關鍵字檢索與語意檢索兩大類
- [向量嵌入](concepts/embedding.md) — 用數字表示意思，換句話說也找得到
- [關鍵字檢索 BM25](concepts/bm25.md) — 比對字面，擅長代碼與專有名詞
- [切塊](concepts/chunking.md) — 長文件切成小段；大小是取捨，會丟上下文
- [混合檢索與重排](concepts/hybrid-search.md) — 兩種檢索合併，再挑出最相關的
- [長上下文的位置效應](concepts/lost-in-the-middle.md) — 放中間的資料容易被忽略
- [RAG 的常見失敗](concepts/rag-failures.md) — 找不到、沒用好、沒照資料寫
- [怎麼評估 RAG](concepts/rag-evaluation.md) — 資料相關性、忠實度、答案切題度
- [RAG 的三個階段](concepts/rag-paradigms.md) — Naive、Advanced、Modular
- [RAG 與微調](concepts/rag-vs-finetuning.md) — 換資料 vs 改模型
- [LLM Wiki 與 RAG 的差別](concepts/llm-wiki-vs-rag.md) — 臨時找 vs 事先整理

## 來源

- [S1｜Lewis et al. 2020：RAG 原始論文](sources/s1-lewis-2020-rag.md) — 6 條主張
- [S2｜Karpukhin et al. 2020：DPR 稠密段落檢索](sources/s2-karpukhin-2020-dpr.md) — 5 條主張
- [S3｜Gao et al. 2023：大型語言模型的 RAG 綜述](sources/s3-gao-2023-rag-survey.md) — 8 條主張
- [S4｜Liu et al. 2023：Lost in the Middle](sources/s4-liu-2023-lost-in-the-middle.md) — 5 條主張
- [S5｜Es et al. 2023：RAGAS 自動評估](sources/s5-es-2023-ragas.md) — 5 條主張
- [S6｜Anthropic 2024：Contextual Retrieval](sources/s6-anthropic-2024-contextual-retrieval.md) — 8 條主張
- [S7｜Karpathy 2026：LLM Wiki](sources/s7-karpathy-2026-llm-wiki.md) — 5 條主張

## 討論與查詢紀錄

- [討論紀錄：先討論、後生成](discussions/2026-11-23-ingest-discussion.md) — 動筆前 AI 與使用者的兩輪討論，照實記錄
- [查詢紀錄：教學簡報大綱](queries/deck-outline.md) — 用 Wiki 回答「怎麼教 RAG」的結果，簡報由它產生
- [時間紀錄](log.md) — 每次 ingest、lint、查詢的紀錄
