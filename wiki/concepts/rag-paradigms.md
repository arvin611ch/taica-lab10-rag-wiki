---
title: RAG 的三個階段
type: concept
updated: 2026-11-23
---
# RAG 的三個階段

**一句話定義：** 綜述論文把 RAG 的發展分成 Naive RAG（基本型）、Advanced RAG（進階型）、Modular RAG（模組型）三個階段。

## 白話解釋

| 階段 | 做法 | 例子 |
| --- | --- | --- |
| Naive RAG | 固定的三步：建索引 → 檢索 → 生成 | 本 Wiki 的 [檢索增強生成](rag.md) 頁描述的流程 |
| Advanced RAG | 在檢索前後各加一道處理 | 檢索前改寫問題；檢索後[重排](hybrid-search.md)、精簡資料 |
| Modular RAG | 流程拆成可替換、可重組的模組 | 多次檢索、讓模型決定要不要檢索、混合多種資料來源 |

入門只要先懂 Naive RAG；後兩個階段都是為了修補 [RAG 的常見失敗](rag-failures.md)。

## 來源怎麼說

- 三個階段的分法與 Advanced RAG 的檢索前後處理。[S3-c5](../sources/s3-gao-2023-rag-survey.md#s3-c5)
- Naive RAG 的三步。[S3-c2](../sources/s3-gao-2023-rag-survey.md#s3-c2)
- Naive RAG 的毛病是後兩個階段要解決的問題。[S3-c4](../sources/s3-gao-2023-rag-survey.md#s3-c4)

## 相關頁面

[檢索增強生成](rag.md)、[混合檢索與重排](hybrid-search.md)、[RAG 的常見失敗](rag-failures.md)
