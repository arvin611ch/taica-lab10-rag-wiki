---
title: 總覽：RAG 是什麼、為什麼需要、會在哪裡出錯
type: overview
updated: 2026-11-23
---
# 總覽：RAG 是什麼、為什麼需要、會在哪裡出錯

這頁把 7 篇來源串成一條故事線，也是教學簡報的骨架。

## 1. 問題：模型只靠記憶

大型語言模型的知識存在參數裡，難更新、說不出依據、會幻覺。[S1-c1](sources/s1-lewis-2020-rag.md#s1-c1)、[S3-c1](sources/s3-gao-2023-rag-survey.md#s3-c1) → [參數記憶與幻覺](concepts/parametric-memory.md)

## 2. 做法：先找資料再回答

RAG 分三步：建索引、檢索、生成。[S3-c2](sources/s3-gao-2023-rag-survey.md#s3-c2) 2020 年的原始論文用維基百科當文件庫。[S1-c3](sources/s1-lewis-2020-rag.md#s1-c3)、[S1-c4](sources/s1-lewis-2020-rag.md#s1-c4) → [檢索增強生成](concepts/rag.md)

- 建索引要先 [切塊](concepts/chunking.md)，再轉成 [向量嵌入](concepts/embedding.md)。
- 找資料靠 [檢索器](concepts/retriever.md)：關鍵字檢索 [BM25](concepts/bm25.md) 看字面，向量檢索看意思，兩者互補。[S2-c5](sources/s2-karpukhin-2020-dpr.md#s2-c5)

## 3. 好處：知識可以換、答案可以查

換掉文件庫就能更新知識，不用重新訓練。[S1-c5](sources/s1-lewis-2020-rag.md#s1-c5) 回答也比純生成模型更符合事實。[S1-c6](sources/s1-lewis-2020-rag.md#s1-c6) RAG 不改模型，跟 [微調](concepts/rag-vs-finetuning.md) 解決的問題不同。[S3-c7](sources/s3-gao-2023-rag-survey.md#s3-c7)

## 4. 會出錯的地方

- **找不到：** 切塊丟了上下文。[S6-c3](sources/s6-anthropic-2024-contextual-retrieval.md#s6-c3) 情境化、混合檢索、重排可以讓失敗率下降 35%–67%。[S6-c5](sources/s6-anthropic-2024-contextual-retrieval.md#s6-c5) → [混合檢索與重排](concepts/hybrid-search.md)
- **找到了沒用好：** 資料放中間容易被忽略。[S4-c1](sources/s4-liu-2023-lost-in-the-middle.md#s4-c1) → [長上下文的位置效應](concepts/lost-in-the-middle.md)
- **沒照資料寫：** 生成時仍可能幻覺。[S3-c4](sources/s3-gao-2023-rag-survey.md#s3-c4) → [RAG 的常見失敗](concepts/rag-failures.md)

## 5. 怎麼知道答得好不好

看資料相關性、忠實度、答案切題度。[S5-c1](sources/s5-es-2023-ragas.md#s5-c1)、[S5-c3](sources/s5-es-2023-ragas.md#s5-c3) → [怎麼評估 RAG](concepts/rag-evaluation.md)

## 6. 延伸：RAG 的演進與 LLM Wiki

RAG 從基本型發展到進階型與模組型。[S3-c5](sources/s3-gao-2023-rag-survey.md#s3-c5) → [RAG 的三個階段](concepts/rag-paradigms.md)
LLM Wiki 把「每次臨時找」改成「事先整理、持續累積」。[S7-c1](sources/s7-karpathy-2026-llm-wiki.md#s7-c1) → [LLM Wiki 與 RAG 的差別](concepts/llm-wiki-vs-rag.md)

## 來源之間的關係

- S1 用的檢索器就是 S2 的 DPR。
- S2 與 S6 都說關鍵字與向量檢索各有所長，S6 給出實務做法（混合檢索＋重排）。
- S4 說資料位置會影響答案，S6 的重排與 S3 的 Advanced RAG 都把相關資料排到前面。
- S3 的三個評估分數，S5 給出可自動計算的版本。
- 目前 7 篇來源之間沒有發現互相矛盾的主張。
