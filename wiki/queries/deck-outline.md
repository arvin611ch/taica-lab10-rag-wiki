---
title: 查詢紀錄：教學簡報大綱
type: query
updated: 2026-11-23
---
# 查詢紀錄：教學簡報大綱

**查詢：** 怎麼用這個 Wiki，教沒學過機器學習的大學生認識 RAG？

**做法：** 先讀 [目錄](../index.md) 與 [總覽](../overview.md)，依學習目標挑概念頁，每個重點都對到來源頁的主張。結果寫成 `deck/outline.json`，再由程式產生簡報與這一頁，所以兩者永遠一致。

## 學習目標

- **O1** 說出只靠模型記憶會有哪些問題，以及 RAG 怎麼補
- **O2** 依序說明 RAG 的三個步驟各在做什麼
- **O3** 分辨關鍵字檢索與語意檢索，知道為什麼要混合
- **O4** 指出 RAG 會出錯的地方，以及怎麼檢查答案

## 每頁引用了 Wiki 的哪些內容

| 頁 | 標題 | 目標 | 主張 | 概念頁 |
| --- | --- | --- | --- | --- |
| 1 | RAG 是什麼？ | — | — | — |
| 2 | 今天的目標 | — | — | — |
| 3 | 先想一個問題（示意例子） | O1 | — | — |
| 4 | 為什麼會這樣：模型只靠「記憶」 | O1 | [S1-c1](../sources/s1-lewis-2020-rag.md#s1-c1)、[S3-c1](../sources/s3-gao-2023-rag-survey.md#s3-c1) | [參數記憶與幻覺](../concepts/parametric-memory.md) |
| 5 | 解法：把閉卷考試變成開卷考試（含比喻） | O1 | [S1-c3](../sources/s1-lewis-2020-rag.md#s1-c3)、[S3-c2](../sources/s3-gao-2023-rag-survey.md#s3-c2)、[S1-c2](../sources/s1-lewis-2020-rag.md#s1-c2) | [檢索增強生成（RAG）](../concepts/rag.md) |
| 6 | RAG 的三個步驟 | O2 | [S3-c2](../sources/s3-gao-2023-rag-survey.md#s3-c2)、[S1-c3](../sources/s1-lewis-2020-rag.md#s1-c3) | [檢索增強生成（RAG）](../concepts/rag.md)、[檢索器](../concepts/retriever.md) |
| 7 | 步驟一：建索引（1）切塊 | O2 | [S3-c2](../sources/s3-gao-2023-rag-survey.md#s3-c2)、[S6-c1](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c1)、[S1-c4](../sources/s1-lewis-2020-rag.md#s1-c4)、[S3-c6](../sources/s3-gao-2023-rag-survey.md#s3-c6) | [切塊](../concepts/chunking.md) |
| 8 | 步驟一：建索引（2）轉成向量（含比喻） | O2 | [S2-c2](../sources/s2-karpukhin-2020-dpr.md#s2-c2)、[S3-c3](../sources/s3-gao-2023-rag-survey.md#s3-c3) | [向量嵌入](../concepts/embedding.md) |
| 9 | 步驟二：檢索有兩種找法 | O3 | [S2-c1](../sources/s2-karpukhin-2020-dpr.md#s2-c1)、[S2-c2](../sources/s2-karpukhin-2020-dpr.md#s2-c2)、[S6-c2](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c2)、[S6-c8](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c8)、[S2-c5](../sources/s2-karpukhin-2020-dpr.md#s2-c5) | [檢索器](../concepts/retriever.md)、[關鍵字檢索 BM25](../concepts/bm25.md)、[混合檢索與重排](../concepts/hybrid-search.md) |
| 10 | 跟著一個問題走一遍（示意例子） | O2 | — | — |
| 11 | 好處：換掉資料庫，就能更新知識 | O1 | [S1-c5](../sources/s1-lewis-2020-rag.md#s1-c5)、[S1-c6](../sources/s1-lewis-2020-rag.md#s1-c6) | [檢索增強生成（RAG）](../concepts/rag.md) |
| 12 | RAG 和微調有什麼不同？ | O1 | [S3-c7](../sources/s3-gao-2023-rag-survey.md#s3-c7)、[S1-c5](../sources/s1-lewis-2020-rag.md#s1-c5)、[S1-c2](../sources/s1-lewis-2020-rag.md#s1-c2) | [RAG 與微調](../concepts/rag-vs-finetuning.md) |
| 13 | 出錯①：找不到對的資料 | O4 | [S6-c3](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c3)、[S6-c4](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c4)、[S6-c6](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c6)、[S6-c5](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c5) | [RAG 的常見失敗](../concepts/rag-failures.md)、[混合檢索與重排](../concepts/hybrid-search.md)、[切塊](../concepts/chunking.md) |
| 14 | 出錯②：找到了，卻沒用好 | O4 | [S4-c1](../sources/s4-liu-2023-lost-in-the-middle.md#s4-c1)、[S4-c2](../sources/s4-liu-2023-lost-in-the-middle.md#s4-c2)、[S4-c4](../sources/s4-liu-2023-lost-in-the-middle.md#s4-c4) | [長上下文的位置效應](../concepts/lost-in-the-middle.md) |
| 15 | 出錯③：沒照資料寫，怎麼檢查？ | O4 | [S3-c4](../sources/s3-gao-2023-rag-survey.md#s3-c4)、[S5-c1](../sources/s5-es-2023-ragas.md#s5-c1)、[S5-c3](../sources/s5-es-2023-ragas.md#s5-c3)、[S5-c2](../sources/s5-es-2023-ragas.md#s5-c2)、[S3-c8](../sources/s3-gao-2023-rag-survey.md#s3-c8) | [怎麼評估 RAG](../concepts/rag-evaluation.md)、[RAG 的常見失敗](../concepts/rag-failures.md) |
| 16 | 延伸：RAG 的演進，與這份簡報的來源 | O2 | [S3-c5](../sources/s3-gao-2023-rag-survey.md#s3-c5)、[S7-c1](../sources/s7-karpathy-2026-llm-wiki.md#s7-c1)、[S7-c2](../sources/s7-karpathy-2026-llm-wiki.md#s7-c2)、[S7-c5](../sources/s7-karpathy-2026-llm-wiki.md#s7-c5) | [RAG 的三個階段](../concepts/rag-paradigms.md)、[LLM Wiki 與 RAG 的差別](../concepts/llm-wiki-vs-rag.md) |
| 17 | 小測驗（上） | O1、O2 | [S1-c1](../sources/s1-lewis-2020-rag.md#s1-c1)、[S3-c2](../sources/s3-gao-2023-rag-survey.md#s3-c2) | — |
| 18 | 小測驗（下） | O3、O4 | [S6-c2](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c2)、[S5-c3](../sources/s5-es-2023-ragas.md#s5-c3) | — |
| 19 | 重點回顧 | — | [S1-c1](../sources/s1-lewis-2020-rag.md#s1-c1)、[S3-c2](../sources/s3-gao-2023-rag-survey.md#s3-c2)、[S2-c5](../sources/s2-karpukhin-2020-dpr.md#s2-c5)、[S3-c4](../sources/s3-gao-2023-rag-survey.md#s3-c4)、[S4-c1](../sources/s4-liu-2023-lost-in-the-middle.md#s4-c1)、[S5-c1](../sources/s5-es-2023-ragas.md#s5-c1) | — |

簡報網址：[docs/slides/index.html](https://arvin611ch.github.io/taica-lab10-rag-wiki/slides/)
