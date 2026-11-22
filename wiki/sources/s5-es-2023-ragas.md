---
id: S5
title: S5｜Es et al. 2023：RAGAS 自動評估
type: source
url: https://arxiv.org/abs/2309.15217
updated: 2026-11-23
---
# S5｜Es et al. 2023：RAGAS 自動評估

**原文：** Shahul Es et al., *RAGAS: Automated Evaluation of Retrieval Augmented Generation*, EACL 2024 demo. <https://arxiv.org/abs/2309.15217>

**一句話摘要：** 提出三個不需要標準答案、由 LLM 自動打分的 RAG 評估指標：忠實度、答案切題度、資料相關性。

## 重點

### S5-c1｜忠實度：答案應該建立在找回來的資料上 {#s5-c1}

> 證據（§3）：「Faithfulness refers to the idea that the answer should be grounded in the given context.」

白話說明：答案裡的每一句話，都應該能從找回來的資料推得出來。見 [怎麼評估 RAG](../concepts/rag-evaluation.md)。

### S5-c2｜答案切題度與資料相關性：答案要回應問題，找回的資料要精簡 {#s5-c2}

> 證據（§3）：「Answer Relevance refers to the idea that the generated answer should address the actual question that was provided.」

> 證據（§3）：「Context Relevance refers to the idea that the retrieved context should be focused, containing as little irrelevant information as possible.」

白話說明：答案可能句句屬實卻答非所問（切題度低）；找回來的資料也可能一大堆、真正有用的只有一句（相關性低）。

### S5-c3｜忠實度的算法：把答案拆成短句，逐條檢查能否從資料推出，算出支持的比例 {#s5-c3}

> 證據（§3 Faithfulness）：「we first use an LLM to extract a set of statements」

> 證據（§3 Faithfulness）：「the LLM determines if si can be inferred from c(q) using a verification function」

白話說明：例如答案拆成 4 句，其中 3 句能在資料裡找到依據，忠實度就是 3/4。本專案檢查簡報的方式也借用這個想法：每個重點都要對到 Wiki 裡的一條主張。

### S5-c4｜這些指標不需要人工標的標準答案 {#s5-c4}

> 證據（Abstract）：「we put forward a suite of metrics which can be used to evaluate these different dimensions without having to rely on ground truth human annotations」

白話說明：不用先請人寫好「正確答案」，就能大致評估 RAG 系統，適合開發時快速反覆測試。

### S5-c5｜跟人類判斷比，忠實度最準，資料相關性最難評 {#s5-c5}

> 證據（§5 Experiments）：「For faithfulness, the Ragas prediction are in general highly accurate.」

> 證據（§5 Experiments）：「We found context relevance to be the hardest quality dimension to evaluate.」

白話說明：自動評估也會錯，尤其是判斷「哪些資料是必要的」這一項。

## 這篇沒有強調的部分

WikiEval 資料集的建法與兩種比較基準的細節，入門簡報不使用。

## 用到這篇的頁面

[怎麼評估 RAG](../concepts/rag-evaluation.md)
