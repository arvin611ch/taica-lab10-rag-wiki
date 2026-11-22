---
title: 長上下文的位置效應
type: concept
updated: 2026-11-23
---
# 長上下文的位置效應

**一句話定義：** 把很多份資料一起放進提示詞時，模型比較會用放在開頭和結尾的資料，放在中間的容易被忽略。研究稱為「Lost in the Middle」。

## 白話解釋

上下文（context）是模型一次能讀進去的全部文字，包括問題和找回來的資料。RAG 找回的資料越多，上下文越長。

比喻：像一次讀 20 份講義，第一份和最後一份印象最深，中間那幾份最容易漏看。

這代表「找到資料」還不夠，資料**放在哪裡、放多少**也會影響答案。

## 來源怎麼說

- 正確率常呈 U 型：相關資料在開頭或結尾通常最好，在長篇內容的中間明顯變差。[S4-c1](../sources/s4-liu-2023-lost-in-the-middle.md#s4-c1)
- 答案在中間時，GPT-3.5-Turbo 甚至比不給文件時（56.1%）還差。[S4-c2](../sources/s4-liu-2023-lost-in-the-middle.md#s4-c2)
- 能讀更長內容的模型，不一定比較會用這些內容。[S4-c3](../sources/s4-liu-2023-lost-in-the-middle.md#s4-c3)
- 從 20 篇加到 50 篇，GPT-3.5-Turbo 只多約 1.5%、Claude-1.3 只多約 1%，提示詞卻長很多。[S4-c4](../sources/s4-liu-2023-lost-in-the-middle.md#s4-c4)
- 建議重排或少放幾篇。[S4-c5](../sources/s4-liu-2023-lost-in-the-middle.md#s4-c5)

## 相關頁面

[RAG 的常見失敗](rag-failures.md)、[混合檢索與重排](hybrid-search.md)
