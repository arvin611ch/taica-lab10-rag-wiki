---
title: 名詞表
type: meta
updated: 2026-11-23
---
# 名詞表

簡報檢查程式會讀這張表：簡報裡出現的名詞（含別名），必須在當頁或更早的投影片先定義過。

| 名詞 | 別名 | 一句話定義 | 頁面 |
| --- | --- | --- | --- |
| 檢索增強生成 | RAG、Retrieval-Augmented Generation | 回答前先找資料，連同問題一起交給模型再作答 | [檢索增強生成](concepts/rag.md) |
| 大型語言模型 | LLM、語言模型 | 讀過大量文字、能接著寫出文字的 AI 模型，例如 ChatGPT 背後的模型 | [參數記憶與幻覺](concepts/parametric-memory.md) |
| 參數記憶 | parametric memory | 模型在訓練時存進參數裡的知識 | [參數記憶與幻覺](concepts/parametric-memory.md) |
| 幻覺 | hallucination | 模型寫出聽起來合理、但沒有根據或錯誤的內容 | [參數記憶與幻覺](concepts/parametric-memory.md) |
| 檢索器 | retriever | 負責找資料的元件，回傳最相關的前 K 段 | [檢索器](concepts/retriever.md) |
| 向量嵌入 | embedding、嵌入、向量 | 用一串數字表示文字的意思，意思越近、向量越近 | [向量嵌入](concepts/embedding.md) |
| 切塊 | chunk、chunking、小塊 | 把長文件切成短段落，方便逐段比對 | [切塊](concepts/chunking.md) |
| BM25 | 關鍵字檢索 | 比對關鍵字、看詞有多罕見的傳統檢索方法 | [關鍵字檢索 BM25](concepts/bm25.md) |
| 混合檢索 | hybrid search | 同時用關鍵字與向量檢索再合併結果 | [混合檢索與重排](concepts/hybrid-search.md) |
| 重排 | reranking、rerank | 先粗找一大批，再逐段打分只留最相關的 | [混合檢索與重排](concepts/hybrid-search.md) |
| 上下文 | context | 模型一次讀進去的全部文字，包括問題與資料 | [長上下文的位置效應](concepts/lost-in-the-middle.md) |
| 提示詞 | prompt | 交給模型的輸入文字 | [檢索增強生成](concepts/rag.md) |
| token | | 模型切分文字的單位，長度依模型而定 | [切塊](concepts/chunking.md) |
| 忠實度 | faithfulness | 答案的每一句是否都能在資料裡找到依據 | [怎麼評估 RAG](concepts/rag-evaluation.md) |
| 微調 | fine-tuning | 用新資料再訓練模型、改變模型參數 | [RAG 與微調](concepts/rag-vs-finetuning.md) |
| LLM Wiki | | 讓 LLM 事先把資料整理成持續維護的 Wiki | [LLM Wiki 與 RAG 的差別](concepts/llm-wiki-vs-rag.md) |
