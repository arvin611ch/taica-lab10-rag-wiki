---
title: 混合檢索與重排
type: concept
updated: 2026-11-23
---
# 混合檢索與重排

**一句話定義：** 混合檢索（hybrid search）同時用關鍵字檢索和向量檢索找資料再合併結果；重排（reranking）是先粗找一大批，再用另一個模型逐段打分，只留下最相關的幾段。

## 白話解釋

比喻：混合檢索像同時請兩位圖書館員找書，一位只看書名關鍵字、一位看內容意思，最後把兩人的書單合併。重排像再請一位專家把合併後的書單逐本翻過，挑出最該讀的幾本。

重排還有一個好處：把最相關的資料排在前面。模型比較容易用到放在開頭的資料（見 [長上下文的位置效應](lost-in-the-middle.md)）。

## 來源怎麼說

- BM25 擅長罕見關鍵字，DPR 擅長同義改寫，兩者可以互補。[S2-c5](../sources/s2-karpukhin-2020-dpr.md#s2-c5)
- 向量檢索可能漏掉精確代碼，加上 BM25 可以補上。[S6-c2](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c2)
- 混合檢索的做法：BM25 與向量檢索各找一批，合併並去掉重複。[S6-c8](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c8)
- 重排的做法：先取 150 塊，再打分留下 20 塊。[S6-c6](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c6)
- 情境化向量＋情境化 BM25＋重排，讓找不到資料的比例下降 67%。[S6-c5](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c5)
- 把相關文件重排到前面，是改善位置效應的建議方向。[S4-c5](../sources/s4-liu-2023-lost-in-the-middle.md#s4-c5)

## 相關頁面

[檢索器](retriever.md)、[關鍵字檢索 BM25](bm25.md)、[向量嵌入](embedding.md)、[RAG 的三個階段](rag-paradigms.md)
