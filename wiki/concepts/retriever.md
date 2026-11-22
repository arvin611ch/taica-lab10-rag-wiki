---
title: 檢索器
type: concept
updated: 2026-11-23
---
# 檢索器

**一句話定義：** 檢索器（retriever）是 RAG 裡負責「找資料」的元件：輸入一個問題，回傳資料庫中最相關的前 K 段文字。

## 白話解釋

檢索器有兩大類：

| 類型 | 怎麼比 | 擅長 | 代表 |
| --- | --- | --- | --- |
| 關鍵字檢索（稀疏檢索） | 問題的詞有沒有出現在文件裡 | 專有名詞、編號、罕見詞 | [BM25](bm25.md) |
| 語意檢索（稠密檢索） | 問題和文件的「意思」近不近 | 換句話說、同義詞 | DPR（見 [向量嵌入](embedding.md)） |

「前 K 段」的 K 是自己設定的數字，例如 Anthropic 的實驗最後取前 20 段。[S6-c6](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c6)K 越大越不容易漏掉答案，但交給模型的內容也越多。

## 來源怎麼說

- RAG 由檢索器與生成器組成，檢索器回傳前 K 段。[S1-c3](../sources/s1-lewis-2020-rag.md#s1-c3)
- 傳統檢索用 TF-IDF 或 BM25 比對關鍵字。[S2-c1](../sources/s2-karpukhin-2020-dpr.md#s2-c1)
- DPR 用兩個編碼器把問題和段落轉成向量，比較向量的接近程度。[S2-c3](../sources/s2-karpukhin-2020-dpr.md#s2-c3)
- 在前 20 筆的檢索準確率上，DPR 比 BM25 高 9 到 19 個百分點。[S2-c4](../sources/s2-karpukhin-2020-dpr.md#s2-c4)
- 但兩者各有所長，可以合併使用。[S2-c5](../sources/s2-karpukhin-2020-dpr.md#s2-c5)

## 相關頁面

[檢索增強生成](rag.md)、[向量嵌入](embedding.md)、[關鍵字檢索 BM25](bm25.md)、[混合檢索與重排](hybrid-search.md)
