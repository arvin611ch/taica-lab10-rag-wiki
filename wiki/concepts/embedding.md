---
title: 向量嵌入
type: concept
updated: 2026-11-23
---
# 向量嵌入

**一句話定義：** 向量嵌入（embedding）是用一串數字（向量）表示一段文字的意思；意思越接近的兩段文字，向量越接近。

## 白話解釋

比喻：把每段文字想成地圖上的一個點。「魔戒裡的壞人」和「反派索倫」雖然用字完全不同，但意思相近，所以兩個點離得很近；「今天天氣很好」就離得很遠。檢索時，只要找離問題最近的幾個點就好。

實際上的「地圖」有數百到上千個維度，由一個嵌入模型負責把文字轉成點。有兩個要注意的地方：

1. 問題和文件必須用**同一個**嵌入模型轉換，才能放在同一張地圖上比較。
2. 嵌入看的是整體意思，對「TS-999」這種精確代碼不一定敏感。[S6-c2](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c2)

## 來源怎麼說

- 同義詞或換句話說，即使用字完全不同，也可能被轉成相近的向量；例如「bad guy」比較能對到「villain」。[S2-c2](../sources/s2-karpukhin-2020-dpr.md#s2-c2)
- 實務流程是先切塊，再用嵌入模型把每塊轉成向量。[S6-c1](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c1)
- 檢索時，問題要用跟建索引時相同的模型轉成向量。[S3-c3](../sources/s3-gao-2023-rag-survey.md#s3-c3)
- 嵌入可能漏掉精確比對。[S6-c2](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c2)

## 相關頁面

[檢索器](retriever.md)、[切塊](chunking.md)、[關鍵字檢索 BM25](bm25.md)
