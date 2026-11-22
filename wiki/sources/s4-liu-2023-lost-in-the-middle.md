---
id: S4
title: S4｜Liu et al. 2023：Lost in the Middle
type: source
url: https://arxiv.org/abs/2307.03172
updated: 2026-11-23
---
# S4｜Liu et al. 2023：Lost in the Middle

**原文：** Nelson F. Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, TACL 2024. <https://arxiv.org/abs/2307.03172>

**一句話摘要：** 把找回來的文件放進提示詞時，「答案在第幾篇」會大幅影響模型表現：放開頭或結尾最好，放中間最差。

## 重點

### S4-c1｜模型的表現呈 U 型：相關資料在開頭或結尾時最好，在中間時明顯變差 {#s4-c1}

> 證據（Abstract）：「performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts」

白話說明：實驗給模型 20 篇文件，只有一篇含有答案，再移動那篇的位置。正確率畫出來像字母 U。見 [長上下文的位置效應](../concepts/lost-in-the-middle.md)。

### S4-c2｜答案放在中間時，GPT-3.5-Turbo 甚至比完全不給文件時還差 {#s4-c2}

> 證據（§1 Introduction）：「when relevant information is placed in the middle of its input context, GPT-3.5-Turbo’s performance on the multi-document question task is lower than its performance when predicting without any documents (i.e., the closed-book setting; 56.1%)」

白話說明：不給文件、只靠模型自己記得的內容（閉卷）時正確率是 56.1%。給了 20 篇文件、但答案剛好在中間時，正確率反而更低。

### S4-c3｜號稱能讀更長內容的模型，不一定比較會用這些內容 {#s4-c3}

> 證據（§1 Introduction）：「extended-context models are not necessarily better at using their input context」

白話說明：模型「放得下」很多文件，不代表它「用得好」。

### S4-c4｜多給文件的效益很快飽和：從 20 篇加到 50 篇只多約 1% 到 1.5% {#s4-c4}

> 證據（§5 Open-domain QA case study）：「Using more than 20 retrieved documents only marginally improves reader performance (∼1.5% for GPT-3.5Turbo and ∼1% for Claude-1.3), while significantly increasing the input context length (and thus latency and cost).」

白話說明：文件越多，提示詞越長、越慢、越貴，正確率卻幾乎沒變。

### S4-c5｜建議的對策：重排，把相關資料移到前面；或在適當時候少放幾篇 {#s4-c5}

> 證據（§5 Open-domain QA case study）：「effective reranking of retrieved documents (pushing relevant information closer to the start of the input context) or ranked list truncation (retrieving fewer documents when appropriate; Arampatzis et al., 2009) may be promising directions」

白話說明：這是作者提出的方向，不是已驗證的保證。見 [混合檢索與重排](../concepts/hybrid-search.md)。

## 這篇沒有強調的部分

合成的「鍵值查找」實驗、模型架構（encoder-decoder 與 decoder-only）的比較，入門簡報不使用。

## 用到這篇的頁面

[長上下文的位置效應](../concepts/lost-in-the-middle.md)、[RAG 的常見失敗](../concepts/rag-failures.md)、[混合檢索與重排](../concepts/hybrid-search.md)
