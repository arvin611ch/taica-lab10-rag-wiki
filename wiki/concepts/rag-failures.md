---
title: RAG 的常見失敗
type: concept
updated: 2026-11-23
---
# RAG 的常見失敗

**一句話定義：** RAG 可能在三個地方出錯：沒找到對的資料、找到了但模型沒用好、模型寫了資料裡沒有的內容。

## 白話解釋

| 出錯的地方 | 例子 | 可以怎麼改 |
| --- | --- | --- |
| 檢索：找錯或漏找 | 切塊丟了上下文，「這家公司」對不上問題 | 情境化切塊、混合檢索、重排 |
| 放進提示詞：沒用好 | 答案夾在中間幾篇，模型沒注意到 | 把相關資料排到前面、少放幾篇 |
| 生成：沒照資料寫 | 資料沒提到的數字，模型自己補上 | 用忠實度檢查答案 |

## 來源怎麼說

- 基本 RAG 的檢索常有找錯、漏找的問題；生成時也可能寫出資料不支持的內容。[S3-c4](../sources/s3-gao-2023-rag-survey.md#s3-c4)
- 切塊會丟掉上下文，導致找不到。[S6-c3](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c3)
- 情境化與重排讓找不到資料的比例下降 35% 到 67%。[S6-c5](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c5)
- 相關資料放在中間時，模型容易忽略。[S4-c1](../sources/s4-liu-2023-lost-in-the-middle.md#s4-c1)

## 相關頁面

[切塊](chunking.md)、[長上下文的位置效應](lost-in-the-middle.md)、[混合檢索與重排](hybrid-search.md)、[怎麼評估 RAG](rag-evaluation.md)
