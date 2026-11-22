---
id: S3
title: S3｜Gao et al. 2023：大型語言模型的 RAG 綜述
type: source
url: https://arxiv.org/abs/2312.10997
updated: 2026-11-23
---
# S3｜Gao et al. 2023：大型語言模型的 RAG 綜述

**原文：** Yunfan Gao et al., *Retrieval-Augmented Generation for Large Language Models: A Survey*, arXiv 2312.10997（v5, 2024）. <https://arxiv.org/abs/2312.10997>

**一句話摘要：** 整理 ChatGPT 之後的 RAG 研究：基本流程分成建索引、檢索、生成三步，方法演進分成 Naive、Advanced、Modular 三個階段，並整理評估 RAG 的面向。

## 重點

### S3-c1｜大型語言模型會幻覺、知識會過時、推理過程無法追溯；RAG 用外部資料庫來補 {#s3-c1}

> 證據（Abstract）：「Large Language Models (LLMs) showcase impressive capabilities but encounter challenges like hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes.」

白話說明：跟 [S1-c1](s1-lewis-2020-rag.md#s1-c1) 說的是同一組問題，只是對象換成 ChatGPT 這類大型語言模型。見 [參數記憶與幻覺](../concepts/parametric-memory.md)。

### S3-c2｜基本 RAG 有三步：建索引、檢索、生成 {#s3-c2}

> 證據（Fig. 2 說明）：「It mainly consists of 3 steps. 1) Indexing. Documents are split into chunks, encoded into vectors, and stored in a vector database.」

> 證據（Fig. 2 說明）：「2) Retrieval. Retrieve the Top k chunks most relevant to the question based on semantic similarity. 3) Generation. Input the original question and the retrieved chunks together into LLM to generate the final answer.」

白話說明：建索引是事前準備（切塊、轉向量、存起來）；使用者發問時才做檢索與生成。見 [檢索增強生成](../concepts/rag.md)。

### S3-c3｜檢索時，問題要用跟建索引時同一個模型轉成向量 {#s3-c3}

> 證據（§II-A Naive RAG）：「the RAG system employs the same encoding model utilized during the indexing phase to transform the query into a vector representation」

白話說明：問題和文件要放在同一個「向量空間」裡才能比遠近，所以必須用同一個嵌入模型。見 [向量嵌入](../concepts/embedding.md)。

### S3-c4｜基本 RAG 常見的毛病：找錯或漏找資料，以及寫出資料裡沒有的內容 {#s3-c4}

> 證據（§II-A Naive RAG）：「The retrieval phase often struggles with precision and recall, leading to the selection of misaligned or irrelevant chunks, and the missing of crucial information.」

> 證據（§II-A Naive RAG）：「the model may face the issue of hallucination, where it produces content not supported by the retrieved context」

白話說明：RAG 不會讓幻覺消失。檢索可能找錯，模型也可能沒照著資料寫。見 [RAG 的常見失敗](../concepts/rag-failures.md)。

### S3-c5｜RAG 的演進分成 Naive、Advanced、Modular 三個階段 {#s3-c5}

> 證據（§II）：「we categorize it into three stages: Naive RAG, Advanced RAG, and Modular RAG」

> 證據（§II-B Advanced RAG）：「Focusing on enhancing retrieval quality, it employs pre-retrieval and post-retrieval strategies.」

白話說明：Advanced RAG 在檢索前改寫問題、檢索後重排與精簡資料；Modular RAG 把流程拆成可以替換、重組的模組，例如多次檢索、視情況決定要不要檢索。見 [RAG 的三個階段](../concepts/rag-paradigms.md)。

### S3-c6｜切塊大小是取捨：大塊上下文多但雜訊多，小塊雜訊少但可能資訊不完整 {#s3-c6}

> 證據（§III-B Indexing Optimization）：「Larger chunks can capture more context, but they also generate more noise, requiring longer processing time and higher costs. While smaller chunks may not fully convey the necessary context, they do have less noise.」

白話說明：見 [切塊](../concepts/chunking.md)。

### S3-c7｜RAG 像給模型一本專用課本；微調像學生把知識內化，適合學格式與風格 {#s3-c7}

> 證據（§II-D RAG vs Fine-tuning）：「RAG can be likened to providing a model with a tailored textbook for information retrieval, ideal for precise information retrieval tasks. In contrast, FT is comparable to a student internalizing knowledge over time, suitable for scenarios requiring replication of specific structures, styles, or formats.」

> 證據（§II-D RAG vs Fine-tuning）：「RAG and FT are not mutually exclusive and can complement each other」

白話說明：「微調」（fine-tuning）是拿新資料再訓練模型、改變模型參數。RAG 不改模型，只在回答時給資料。兩者可以並用。見 [RAG 與微調](../concepts/rag-vs-finetuning.md)。

### S3-c8｜評估 RAG 有三個品質分數：資料相關性、答案忠實度、答案切題度 {#s3-c8}

> 證據（§VI-C Evaluation Aspects）：「Quality scores include context relevance, answer faithfulness, and answer relevance.」

白話說明：見 [怎麼評估 RAG](../concepts/rag-evaluation.md)。

## 這篇沒有強調的部分

各種進階技術（查詢改寫、HyDE、迭代檢索、知識圖譜檢索等）與評估資料集清單，對入門讀者太細，Wiki 只在 [RAG 的三個階段](../concepts/rag-paradigms.md) 提到名稱。

## 用到這篇的頁面

[檢索增強生成](../concepts/rag.md)、[參數記憶與幻覺](../concepts/parametric-memory.md)、[向量嵌入](../concepts/embedding.md)、[切塊](../concepts/chunking.md)、[RAG 的三個階段](../concepts/rag-paradigms.md)、[RAG 與微調](../concepts/rag-vs-finetuning.md)、[RAG 的常見失敗](../concepts/rag-failures.md)、[怎麼評估 RAG](../concepts/rag-evaluation.md)
