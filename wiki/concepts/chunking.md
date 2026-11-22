---
title: 切塊
type: concept
updated: 2026-11-23
---
# 切塊

**一句話定義：** 切塊（chunking）是在建索引時，把長文件切成一段段較短的文字（chunk），讓檢索可以只取出最相關的那幾段。

## 白話解釋

整本手冊太長，不可能每次都全部交給模型，也很難整本拿去跟問題比對。所以先把它切成小段，每段單獨轉成向量。

切多大是一個取捨：

| 切得大 | 切得小 |
| --- | --- |
| 每段的上下文完整 | 每段的主題單純、雜訊少 |
| 雜訊多、處理慢、成本高 | 可能少了理解這段所需的前後文 |

切塊還有一個副作用：被切出來的一段，可能失去原本靠前文才看得懂的資訊。例如「這家公司營收成長 3%」，單看這一段不知道是哪家公司。[S6-c3](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c3)補救方法之一是在每段前面加上一小段說明（情境化檢索）。

## 來源怎麼說

- 2020 年的 RAG 論文把維基百科切成 100 字一段，共 2,100 萬段。[S1-c4](../sources/s1-lewis-2020-rag.md#s1-c4)
- 實務上通常切成不超過數百 token 的小塊。[S6-c1](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c1)
- 大塊上下文多但雜訊多，小塊雜訊少但可能資訊不完整。[S3-c6](../sources/s3-gao-2023-rag-survey.md#s3-c6)
- 切塊會丟掉上下文。[S6-c3](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c3)
- 情境化檢索在每塊前補一段說明，通常 50 到 100 token。[S6-c4](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c4)

## 相關頁面

[向量嵌入](embedding.md)、[RAG 的常見失敗](rag-failures.md)、[混合檢索與重排](hybrid-search.md)
