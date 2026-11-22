---
title: 執行與檢查紀錄
---
# 執行與檢查紀錄

2026-11-23 從頭到尾跑一次的所有檢查。報告由檢查程式自動產生；AI 審查保留審查者的回覆原文。流程說明與反思見 [流程設計與反思](../workflow.html)。

| 回合 | 流程 | 節點 | 結果 | 報告 |
| --- | --- | --- | --- | --- |
| r1 | v1 | ⑤ Wiki 檢查 | 未通過：26 個問題 | [lint_wiki](r1-wiki-lint/lint_wiki.html) |
| r2 | v1 | ⑤ Wiki 檢查 | 通過 | [lint_wiki](r2-wiki-lint/lint_wiki.html) |
| r3 | v1 | ⑩ 簡報檢查 | 第一次執行時在測驗頁當掉（簡報 bug＋檢查程式 bug，修好後重跑）；未通過：4 個問題 | [check_deck](r3-deck/check_deck.html) |
| r4 | v1 | ⑩ 簡報檢查 | 未通過：1 個問題 | [check_deck](r4-deck/check_deck.html) |
| r5 | v1 | ⑩ 簡報檢查＋⑪ AI 審查 | 程式檢查通過；AI 審查找出新手卡住 10 處、事實查核部分支持 17、不支持 2 | [check_deck](r5-deck/check_deck.html)、[新手審查](r5-deck/ai_review_novice.html)、[事實查核](r5-deck/ai_review_factcheck.html)、[審查材料](r5-deck/review_packet.html) |
| r6 | v1 | ⑤ Wiki 檢查 | 通過（接回簡報大綱頁的連結） | [lint_wiki](r6-wiki-lint/lint_wiki.html) |
| r7 | v2 | ④ 單頁檢查＋⑤ Wiki 檢查 | 通過 | [lint_page](r7-page-lint/lint_page.html)、[lint_wiki](r7-wiki-lint/lint_wiki.html) |
| r8 | v2 | ④ AI 主張審查 | 42 條主張：支持 19、部分支持 23、不支持 0 | [主張審查](r8-claims/ai_claims_audit.html)、[審查材料](r8-claims/claims_packet.html) |
| r9 | v2 | ⑧ 大綱檢查＋⑩ 簡報檢查 | 通過 | [check_outline](r9-deck/check_outline.html)、[check_deck](r9-deck/check_deck.html) |
| r10 | v2 | ④ 單頁＋⑤＋⑧＋⑩＋⑪ 第二輪 AI 審查 | 單頁檢查先攔下 1 個問題，修正後全部通過；第二輪 AI 審查：事實查核支持 35、部分支持 10、不支持 0；新手 4/5、測驗全對 | [lint_page](r10-page-lint/lint_page.html)、[lint_wiki](r10-wiki-lint/lint_wiki.html)、[check_outline](r10-deck/check_outline.html)、[check_deck](r10-deck/check_deck.html)、[新手審查](r10-deck/ai_review_novice.html)、[事實查核](r10-deck/ai_review_factcheck.html) |
| r11 | v2 | ⑧＋⑩ 最後一次修正後的檢查 | 全部通過（大綱檢查先攔下 2 次超字數）；依停止條件不再送 AI 審查 | [check_outline](r11-deck/check_outline.html)、[check_deck](r11-deck/check_deck.html)、[lint_wiki](r11-wiki-lint/lint_wiki.html) |

說明：

- ⑧ 大綱檢查在產生簡報前攔下超字數的 3 次（v2 第一次修大綱時 1 次、r11 之前 2 次），執行時沒有加 `--out`，所以沒有留下報告檔；r9–r11 的 check_outline 是之後通過的那一次。過程記在 [Wiki 時間紀錄](../wiki/log.html)。
- r7 的單頁檢查報告只保留最後一次（每次執行會覆蓋同一個檔案）；當時逐頁執行的結果都是通過。
- 簡報截圖存在本機的 `runs/*/shots/`，因為檔案多，沒有放進 repo。
