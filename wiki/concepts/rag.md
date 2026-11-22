---
title: 檢索增強生成（RAG）
type: concept
updated: 2026-11-23
---
# 檢索增強生成（RAG）

**一句話定義：** 讓語言模型回答之前，先從外部資料庫找出相關資料，連同問題一起交給模型，再根據這些資料產生答案。英文是 Retrieval-Augmented Generation。

## 白話解釋

一般的聊天機器人只能靠訓練時記住的內容回答，像閉卷考試。RAG 把它變成開卷考試：先翻書（檢索），把找到的幾頁夾進題目裡（增強），再作答（生成）。

比喻：閉卷考試靠記憶，記錯了自己也不知道；開卷考試可以翻書，但翻錯頁一樣會答錯。

RAG 分成「事前準備」與「每次提問」兩段：

1. **建索引（事前）：** 把文件切成小塊，每塊轉成向量，存進資料庫。
2. **檢索（提問時）：** 把問題也轉成向量，找出最接近的前 K 塊。
3. **生成（提問時）：** 把問題和找到的資料一起放進提示詞，讓模型寫答案。

## 來源怎麼說

- 這個名稱來自 2020 年的論文：檢索器負責找文件，生成器根據文件與問題寫答案。[S1-c3](../sources/s1-lewis-2020-rag.md#s1-c3)
- 綜述論文把基本流程整理成建索引、檢索、生成三步。[S3-c2](../sources/s3-gao-2023-rag-survey.md#s3-c2)
- 它要解決的是模型只靠參數記憶的問題：不易更新、難說明依據、可能幻覺。[S1-c1](../sources/s1-lewis-2020-rag.md#s1-c1)、[S3-c1](../sources/s3-gao-2023-rag-survey.md#s3-c1)
- 好處之一是換掉文件庫就能更新知識，不必重新訓練模型。[S1-c5](../sources/s1-lewis-2020-rag.md#s1-c5)
- 資料量小到能整份放進提示詞時，不一定需要 RAG。[S6-c7](../sources/s6-anthropic-2024-contextual-retrieval.md#s6-c7)

## 常見誤解

- **「用了 RAG 就不會幻覺」**：不對。檢索可能找錯，模型也可能寫出資料裡沒有的內容。見 [RAG 的常見失敗](rag-failures.md)。
- **「RAG 會讓模型學會新知識」**：不對。模型參數沒有改變，只是回答時多看了資料。要改變模型本身是 [微調](rag-vs-finetuning.md)。

## 相關頁面

[參數記憶與幻覺](parametric-memory.md)、[檢索器](retriever.md)、[切塊](chunking.md)、[向量嵌入](embedding.md)、[RAG 的三個階段](rag-paradigms.md)、[RAG 與微調](rag-vs-finetuning.md)、[總覽](../overview.md)
