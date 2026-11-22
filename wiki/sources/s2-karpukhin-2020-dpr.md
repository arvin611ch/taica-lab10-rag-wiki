---
id: S2
title: S2｜Karpukhin et al. 2020：DPR 稠密段落檢索
type: source
url: https://arxiv.org/abs/2004.04906
updated: 2026-11-23
---
# S2｜Karpukhin et al. 2020：DPR 稠密段落檢索

**原文：** Vladimir Karpukhin et al., *Dense Passage Retrieval for Open-Domain Question Answering*, EMNLP 2020. <https://arxiv.org/abs/2004.04906>

**一句話摘要：** 把問題和段落都轉成向量，用「意思相近」而不是「字面相同」來找資料；在多個問答資料集上贏過傳統關鍵字檢索 BM25。S1 的 RAG 用的檢索器就是 DPR。

## 重點

### S2-c1｜傳統的關鍵字檢索（TF-IDF、BM25）是比對字詞，像查索引 {#s2-c1}

> 證據（§1 Introduction）：「Retrieval in open-domain QA is usually implemented using TF-IDF or BM25 (Robertson and Zaragoza, 2009), which matches keywords efficiently with an inverted index」

白話說明：關鍵字檢索看的是問題裡的詞有沒有出現在文件裡。見 [關鍵字檢索 BM25](../concepts/bm25.md)。

### S2-c2｜用向量表示意思，換句話說也比較容易找到：「bad guy」比較能對到「villain」 {#s2-c2}

> 證據（§1 Introduction）：「synonyms or paraphrases that consist of completely different tokens may still be mapped to vectors close to each other」

> 證據（§1 Introduction）：「a dense retrieval system would be able to better match “bad guy” with “villain” and fetch the correct context」

> 證據（§1 Introduction）：「“Who is the bad guy in lord of the rings?”, which can be answered from the context “Sala Baker is best known for portraying the villain Sauron in the Lord of the Rings trilogy.”」

白話說明：問題說「壞人（bad guy）」，答案段落說「反派（villain）」。兩句都提到魔戒，但關鍵的這兩個詞字面不同，只比對字詞容易漏掉；向量檢索看的是意思，比較有機會找到。見 [向量嵌入](../concepts/embedding.md)。

### S2-c3｜DPR 用兩個編碼器，分別把問題和段落轉成向量，再用內積找最接近的段落 {#s2-c3}

> 證據（§3.1 Overview）：「uses a dense encoder EP (·) which maps any text passage to a ddimensional real-valued vectors」

> 證據（§3.1 Overview）：「At run-time, DPR applies a different encoder EQ (·) that maps the input question to a d-dimensional vector, and retrieves k passages of which vectors are the closest to the question vector.」

> 證據（§1 Introduction）：「the embedding is optimized for maximizing inner products of the question and relevant passage vectors」

白話說明：「雙編碼器」就是兩個轉換器：一個專門轉問題、一個專門轉段落。訓練目標是讓「問題」和「能回答它的段落」的向量越接近越好。見 [檢索器](../concepts/retriever.md)。

### S2-c4｜在多個開放領域問答資料集上，DPR 的前 20 筆檢索準確率比 BM25 高 9 到 19 個百分點（SQuAD 例外） {#s2-c4}

> 證據（Abstract）：「our dense retriever outperforms a strong LuceneBM25 system greatly by 9%-19% absolute in terms of top-20 passage retrieval accuracy」

> 證據（Table 2 說明）：「measured as the percentage of top 20/100 retrieved passages that contain the answer」

> 證據（§5.1 Main Results）：「With the exception of SQuAD, DPR performs consistently better than BM25 on all datasets.」

白話說明：「前 20 筆準確率」是指檢索器找回的前 20 段裡含有答案的比例。在 SQuAD 這個資料集上，問題是看著段落寫的、字面重疊多，BM25 反而比較好。

### S2-c5｜兩種方法各有所長：BM25 擅長罕見關鍵字，DPR 擅長同義改寫 {#s2-c5}

> 證據（§5.3 Qualitative Analysis）：「Term-matching methods like BM25 are sensitive to highly selective keywords and phrases, while DPR captures lexical variations or semantic relationships better.」

白話說明：遇到專有名詞、編號、少見人名，字面比對反而準；遇到換句話說，向量比對比較好。論文也發現把兩者分數合併，有些情況下結果更好。

> 證據（§5.1）：「Results can be improved further in some cases by combining DPR with BM25 in both single- and multi-dataset settings.」

這是 [混合檢索](../concepts/hybrid-search.md) 的理由。

## 這篇沒有強調的部分

訓練細節（同一批次內互為負例的訓練方式、只用 1,000 筆訓練資料就贏過 BM25）與端到端問答成績，入門簡報不使用。

## 用到這篇的頁面

[檢索器](../concepts/retriever.md)、[向量嵌入](../concepts/embedding.md)、[關鍵字檢索 BM25](../concepts/bm25.md)、[混合檢索與重排](../concepts/hybrid-search.md)
