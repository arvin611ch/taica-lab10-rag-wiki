---
title: 首頁
---
# RAG 入門：LLM Wiki × 教學 HTML 簡報

TAICA Lab 10｜陽明交大 113611097 百川 江晟維

這個作業先照 Karpathy 的〈LLM Wiki〉構想，讓 AI（Claude Code）把 7 篇關於「檢索增強生成（RAG）」的資料整理成一個互相連結、每句話都能追到原文的 Wiki；再只用這個 Wiki 當知識來源，產生一份給沒學過機器學習的大學生看的教學簡報。

## 入口

| 成果 | 連結 | 說明 |
| --- | --- | --- |
| 教學 HTML 簡報 | [slides/](slides/index.html) | 19 頁。方向鍵換頁，第 17–18 頁的測驗可以點選作答 |
| LLM Wiki | [wiki/](wiki/index.html) | 7 個來源頁、42 條主張、13 個概念頁、名詞表、總覽、討論紀錄 |
| 流程設計與反思 | [workflow.html](workflow.html) | 流程圖、哪些步驟會重複、哪裡檢查、哪個節點最常出錯、改了什麼 |
| 執行與檢查紀錄 | [runs/](runs/index.html) | 每次檢查的原始報告與 AI 審查結果 |
| 原始碼 | [GitHub](https://github.com/arvin611ch/taica-lab10-rag-wiki) | 規則檔 `AGENTS.md`、Wiki 原始 Markdown、檢查程式 |

## LLM Wiki 主題與簡介

- **主題：** 檢索增強生成（Retrieval-Augmented Generation, RAG）——讓語言模型回答前先查資料。
- **讀者：** 用過 ChatGPT、但沒學過機器學習的大學生。
- **三層結構：** 原始資料（`raw/`，只讀不改）→ Wiki（`wiki/`，AI 撰寫）→ 規則檔（`AGENTS.md`，規定格式與流程）。
- **可追溯：** 每條主張都附一段從原文逐字複製的英文證據，檢查程式會逐字比對原文；簡報的每個重點旁邊都有主張編號，點下去會跳到 Wiki 的那一條。

| 編號 | 資料 | 在簡報中的角色 |
| --- | --- | --- |
| S1 | [Lewis et al. 2020，RAG 原始論文](wiki/sources/s1-lewis-2020-rag.html) | 問題、定義、換資料庫就能更新知識 |
| S2 | [Karpukhin et al. 2020，DPR](wiki/sources/s2-karpukhin-2020-dpr.html) | 關鍵字 vs 語意檢索 |
| S3 | [Gao et al. 2023，RAG 綜述](wiki/sources/s3-gao-2023-rag-survey.html) | 三步驟、與微調的差別、演進 |
| S4 | [Liu et al. 2023，Lost in the Middle](wiki/sources/s4-liu-2023-lost-in-the-middle.html) | 資料放中間容易被忽略 |
| S5 | [Es et al. 2023，RAGAS](wiki/sources/s5-es-2023-ragas.html) | 怎麼評估答案是否忠實 |
| S6 | [Anthropic 2024，Contextual Retrieval](wiki/sources/s6-anthropic-2024-contextual-retrieval.html) | 切塊、混合檢索、重排的實務數字 |
| S7 | [Karpathy 2026，LLM Wiki](wiki/sources/s7-karpathy-2026-llm-wiki.html) | RAG 與 LLM Wiki 的差別 |

簡報每一頁引用了哪些主張，整理在 [查詢紀錄：教學簡報大綱](wiki/queries/deck-outline.html)。
