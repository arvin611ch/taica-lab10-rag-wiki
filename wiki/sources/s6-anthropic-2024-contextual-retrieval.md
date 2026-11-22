---
id: S6
title: S6｜Anthropic 2024：Contextual Retrieval
type: source
url: https://www.anthropic.com/engineering/contextual-retrieval
updated: 2026-11-23
---
# S6｜Anthropic 2024：Contextual Retrieval

**原文：** Anthropic, *Introducing Contextual Retrieval*（2024 年 9 月技術文章）. <https://www.anthropic.com/engineering/contextual-retrieval>

**一句話摘要：** 實務角度的 RAG 前處理教學：切塊、轉向量、加上關鍵字檢索；並提出在每個切塊前補一段說明（情境化），大幅減少找不到資料的情況。

## 重點

### S6-c1｜RAG 的前處理：把文件切成通常不超過數百 token 的小塊、轉成向量、存進向量資料庫 {#s6-c1}

> 證據（A primer on RAG）：「Break down the knowledge base (the “corpus” of documents) into smaller chunks of text, usually no more than a few hundred tokens;」

> 證據（A primer on RAG）：「Use an embedding model to convert these chunks into vector embeddings that encode meaning;」

> 證據（A primer on RAG）：「Store these embeddings in a vector database that allows for searching by semantic similarity.」

白話說明：token 是模型讀文字的基本單位，大約是一個英文單字的一部分或一兩個中文字。見 [切塊](../concepts/chunking.md)、[向量嵌入](../concepts/embedding.md)。

### S6-c2｜向量檢索可能漏掉精確比對，例如錯誤代碼「TS-999」；BM25 能補上 {#s6-c2}

> 證據（A primer on RAG）：「While embedding models excel at capturing semantic relationships, they can miss crucial exact matches.」

> 證據（A primer on RAG）：「An embedding model might find content about error codes in general, but could miss the exact "TS-999" match. BM25 looks for this specific text string to identify the relevant documentation.」

白話說明：跟 [S2-c5](s2-karpukhin-2020-dpr.md#s2-c5) 的結論一致。見 [關鍵字檢索 BM25](../concepts/bm25.md)、[混合檢索與重排](../concepts/hybrid-search.md)。

### S6-c3｜切塊會丟掉上下文：「營收成長 3%」這一塊本身沒寫是哪家公司、哪一季 {#s6-c3}

> 證據（The context conundrum）：「A relevant chunk might contain the text: "The company's revenue grew by 3% over the previous quarter." However, this chunk on its own doesn't specify which company it's referring to or the relevant time period」

白話說明：一段話被切出來之後，原本靠前文才看得懂的「這家公司」就失去指涉對象，檢索時也就對不上問題。

### S6-c4｜情境化檢索：在每塊前面補一段 50 到 100 token 的說明，再建向量與 BM25 索引 {#s6-c4}

> 證據（Implementing Contextual Retrieval）：「To implement Contextual Retrieval, we turn to Claude.」

> 證據（Implementing Contextual Retrieval）：「The resulting contextual text, usually 50-100 tokens, is prepended to the chunk before embedding it and before creating the BM25 index.」

> 證據（Introducing Contextual Retrieval）：「This chunk is from an SEC filing on ACME corp's performance in Q2 2023」

白話說明：說明文字由 LLM 讀整份文件後自動寫，例如「這段出自 ACME 公司 2023 年第二季的財報」。

### S6-c5｜效果：找不到資料的比例下降 35%、49%，加上重排後下降 67% {#s6-c5}

> 證據（Performance improvements）：「Contextual Embeddings reduced the top-20-chunk retrieval failure rate by 35% (5.7% → 3.7%).」

> 證據（Performance improvements）：「Combining Contextual Embeddings and Contextual BM25 reduced the top-20-chunk retrieval failure rate by 49% (5.7% → 2.9%).」

> 證據（Further boosting performance with Reranking）：「Reranked Contextual Embedding and Contextual BM25 reduced the top-20-chunk retrieval failure rate by 67% (5.7% → 1.9%).」

白話說明：「失敗率」是相關資料沒有出現在前 20 塊的比例。原本是 5.7%，三種做法依序降到 3.7%、2.9%、1.9%。這是 Anthropic 在自家測試資料上的結果。

### S6-c6｜重排：先粗找一大批（文中 150 塊），再用重排模型逐塊打分，只留最好的（文中 20 塊） {#s6-c6}

> 證據（Further boosting performance with Reranking）：「Perform initial retrieval to get the top potentially relevant chunks (we used the top 150);」

> 證據（Further boosting performance with Reranking）：「Using a reranking model, give each chunk a score based on its relevance and importance to the prompt, then select the top-K chunks (we used the top 20);」

白話說明：見 [混合檢索與重排](../concepts/hybrid-search.md)。

### S6-c7｜知識庫不到 20 萬 token（約 500 頁）時，可以整份放進提示詞，不一定需要 RAG {#s6-c7}

> 證據（A note on simply using a longer prompt）：「If your knowledge base is smaller than 200,000 tokens (about 500 pages of material), you can just include the entire knowledge base in the prompt that you give the model, with no need for RAG or similar methods.」

白話說明：RAG 是為了「資料太多、放不進去」而存在。資料少的時候，最簡單的做法就是全部給模型看。這個門檻取決於模型能讀多長，文中指的是 Claude 當時的上限。

### S6-c8｜混合檢索：BM25 與向量檢索各找一批，再合併、去掉重複 {#s6-c8}

> 證據（A primer on RAG）：「Combine and deduplicate results from (3) and (4) using rank fusion techniques;」

> 證據（A primer on RAG）：「By leveraging both BM25 and embedding models, traditional RAG systems can provide more comprehensive and accurate results」

白話說明：(3) 是用 BM25 找字面相符的塊，(4) 是用向量找意思相近的塊。兩份名單合併、去掉重複後，取前幾名放進提示詞。見 [混合檢索與重排](../concepts/hybrid-search.md)。

## 這篇沒有強調的部分

提示詞快取的成本估算、各家嵌入模型的比較，入門簡報不使用。

## 用到這篇的頁面

[切塊](../concepts/chunking.md)、[向量嵌入](../concepts/embedding.md)、[關鍵字檢索 BM25](../concepts/bm25.md)、[混合檢索與重排](../concepts/hybrid-search.md)、[RAG 的常見失敗](../concepts/rag-failures.md)、[檢索增強生成](../concepts/rag.md)
