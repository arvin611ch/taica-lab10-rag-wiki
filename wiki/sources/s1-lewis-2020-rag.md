---
id: S1
title: S1｜Lewis et al. 2020：RAG 原始論文
type: source
url: https://arxiv.org/abs/2005.11401
updated: 2026-11-23
---
# S1｜Lewis et al. 2020：RAG 原始論文

**原文：** Patrick Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020. <https://arxiv.org/abs/2005.11401>

**一句話摘要：** 第一篇把「檢索器＋生成模型」命名為 RAG 的論文：讓語言模型回答前先到維基百科找相關段落，再根據段落產生答案。

## 重點

### S1-c1｜語言模型把知識存在參數裡；只靠這種記憶有三個缺點：不易更新、難說明預測依據、可能產生幻覺 {#s1-c1}

> 證據（Abstract）：「Large pre-trained language models have been shown to store factual knowledge in their parameters」

> 證據（§1 Introduction）：「They cannot easily expand or revise their memory, can’t straightforwardly provide insight into their predictions, and may produce “hallucinations”」

白話說明：語言模型把訓練時讀到的知識「壓」進模型的參數裡。這種記憶不容易直接改、很難看出模型為什麼這樣回答，還可能一本正經地編造內容。見 [參數記憶與幻覺](../concepts/parametric-memory.md)。

### S1-c2｜加上可檢索的外部記憶後，知識可以直接修改，也能拿出來檢查 {#s1-c2}

> 證據（§1 Introduction）：「knowledge can be directly revised and expanded, and accessed knowledge can be inspected and interpreted」

白話說明：外部記憶就是一個可以查的文件庫。要更新知識，改文件庫就好；模型用了哪幾段資料，也可以直接攤開來看。

### S1-c3｜RAG 由兩個元件組成：檢索器找文件，生成器根據文件與問題產生答案 {#s1-c3}

> 證據（§2 Methods）：「a retriever pη (z|x) with parameters η that returns (top-K truncated) distributions over text passages given a query x」

> 證據（§1 Introduction）：「the seq2seq model (BART [32]) then conditions on these latent documents together with the input to generate the output」

白話說明：論文中的檢索器是 [DPR](s2-karpukhin-2020-dpr.md)，生成器是 BART 模型。檢索器回傳前 K 份最相關的段落，生成器把問題和這些段落一起讀進去再寫答案。見 [檢索器](../concepts/retriever.md)。

### S1-c4｜論文的外部資料庫是維基百科，每 100 個英文詞（word）切成一段，共 2,100 萬段 {#s1-c4}

> 證據（§3 Experiments）：「Each Wikipedia article is split into disjoint 100-word chunks, to make a total of 21M documents.」

白話說明：這就是「切塊」：把長文章切成固定長度的小段，才能一段一段比對。見 [切塊](../concepts/chunking.md)。

### S1-c5｜換掉文件庫，答案就跟著新資料改變；只靠參數的模型則需要再訓練（2016／2018 年版實驗） {#s1-c5}

> 證據（§4.5 Index hot-swapping）：「Parametric-only models like T5 or BART need further training to update their behavior as the world changes.」

> 證據（§4.5 Index hot-swapping）：「We prepare a list of 82 world leaders who had changed」

> 證據（§4.5 Index hot-swapping）：「RAG answers 70% correctly using the 2016 index for 2016 world leaders and 68% using the 2018 index for 2018 world leaders.」

> 證據（§4.5 Index hot-swapping）：「Accuracy with mismatched indices is low (12% with the 2018 index and 2016 leaders, 4% with the 2016 index and 2018 leaders).」

白話說明：作者準備了 82 位在 2016 到 2018 年間換人的各國領袖，問「某職位現在是誰？」。用 2016 年的維基百科當文件庫，就答對 2016 年的領袖 70%；換成 2018 年的文件庫，就答對 2018 年的領袖 68%。文件庫和題目年份對不上時，正確率掉到 12% 和 4%。模型本身從頭到尾沒有重新訓練。

> 證據（§4.5 Index hot-swapping）：「This shows we can update RAG’s world knowledge by simply replacing its non-parametric memory.」

### S1-c6｜人工評比時，RAG 產生的題目比純生成模型更符合事實 {#s1-c6}

> 證據（§4.3）：「human evaluation results, over 452 pairs of generations from BART and RAG-Token」

> 證據（§4.3）：「Evaluators indicated that BART was more factual than RAG in only 7.1% of cases, while RAG was more factual in 42.7% of cases」

白話說明：評審比較 452 組由 BART（沒有檢索）和 RAG 產生的益智題目。認為 RAG 比較符合事實的有 42.7%，認為 BART 比較符合事實的只有 7.1%。這是單一任務的結果，不代表 RAG 永遠不會出錯。

## 這篇沒有強調的部分

論文比較了兩種變體（RAG-Sequence 與 RAG-Token），差在生成每個字時能不能換用不同文件。這屬於技術細節，入門簡報不使用。

## 用到這篇的頁面

[檢索增強生成](../concepts/rag.md)、[參數記憶與幻覺](../concepts/parametric-memory.md)、[檢索器](../concepts/retriever.md)、[切塊](../concepts/chunking.md)
