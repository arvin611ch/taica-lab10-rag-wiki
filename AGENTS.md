# RAG 入門 LLM Wiki：規則檔（schema）

這份檔案告訴 AI（本專案用 Claude Code）這個 Wiki 怎麼組織、頁面長什麼樣子、每種操作要照什麼步驟做。做法依照 Karpathy 的〈LLM Wiki〉構想：原始資料、Wiki、規則檔三層，操作分成 ingest、query、lint。

## 主題與讀者

- 主題：檢索增強生成（Retrieval-Augmented Generation, RAG）。
- 讀者：沒學過機器學習、但用過 ChatGPT 的大學生。
- 用途：當作教學簡報〈RAG 是什麼？讓 AI 先查資料再回答〉的唯一知識來源。

## 三層結構

| 層 | 位置 | 誰寫 | 規則 |
| --- | --- | --- | --- |
| 原始資料 | `raw/` | 只由 `pipeline/fetch_sources.py` 下載 | 不修改。全文只留本機（`.gitignore`），公開 repo 只放 `raw/manifest.json` 的網址與 SHA-256 |
| Wiki | `wiki/` | AI | 所有事實都要能追到某篇原始資料的原文 |
| 規則檔 | `AGENTS.md` | 使用者與 AI 共同修訂 | 流程改了就更新這份檔案並在 `wiki/log.md` 記一筆 |

## 頁面種類與格式

每頁開頭都有 YAML frontmatter：`title`、`type`（`source`／`concept`／`overview`／`query`／`discussion`／`meta`）、`updated`。

### 來源頁 `wiki/sources/<slug>.md`

一篇原始資料一頁。frontmatter 另有 `id`（`S1`…）與 `url`。每個重點寫成一個「主張」區塊：

```markdown
### S1-c1｜一句中文主張 {#s1-c1}

> 證據（§章節）：「從原文逐字複製的英文句子」

白話說明：……
```

- 主張編號 `S<來源>-c<序號>`，錨點一律小寫（`#s1-c1`）。
- 「證據」必須逐字出自 `raw/text/<id>.txt`，放在全形引號「」中；只能刪去頭尾，不能改字、不能拼接兩段不相連的句子。
- 數字（百分比、年份、篇數）只能出現在有證據支撐的主張裡。

### 概念頁 `wiki/concepts/<slug>.md`

一個概念一頁，結構固定：`**一句話定義：**`、`## 白話解釋`、`## 來源怎麼說`（引用主張）、`## 常見誤解`（可省略）、`## 相關頁面`。

- 引用主張的寫法：`[S1-c1](../sources/s1-lewis-2020-rag.md#s1-c1)`。
- 比喻要標成「比喻：」開頭，表示這不是來源裡的事實。

### 其他頁

- `wiki/index.md`：全部頁面的目錄，每頁一行連結加一句摘要。每次 ingest 都要更新。
- `wiki/log.md`：只往後加的時間紀錄，每筆以 `## [YYYY-MM-DD] 操作 | 標題` 開頭。
- `wiki/glossary.md`：名詞表。簡報的「名詞先定義後使用」檢查會讀這份表。
- `wiki/overview.md`：把所有來源串起來的綜合整理。
- `wiki/discussions/`：「先討論、後生成」的討論紀錄，照實記錄 AI 提出的重點與使用者的回覆。
- `wiki/queries/`：值得留下的查詢結果（例如簡報大綱），存回 Wiki。

## 操作

### Ingest（加入一篇資料）

1. `pipeline/fetch_sources.py` 下載資料、轉成文字、記錄 SHA-256。
2. AI 讀資料，列出 3–4 個候選重點，先跟使用者討論要強調哪些，再動筆。
3. 寫來源頁，**寫完立刻跑單頁檢查**：`lint_wiki.py --page wiki/sources/<slug>.md`。通過了才去更新概念頁。
4. 更新相關概念頁、`glossary.md`、`index.md`；每改一頁也跑一次單頁檢查。最後在 `log.md` 加一筆。
5. 一篇做完再做下一篇；全部做完跑一次完整的 `lint_wiki.py`，檢查孤兒頁、目錄與覆蓋這類整體結構。

### Query（向 Wiki 提問）

先讀 `index.md` 找相關頁面，再讀概念頁與來源頁，回答時附主張編號。有保存價值的答案存到 `wiki/queries/`。

### Lint（健康檢查）

`pipeline/lint_wiki.py` 檢查：frontmatter、證據是否逐字出自原文、引用的主張是否存在、站內連結與錨點、孤兒頁、目錄是否完整、log 格式、每篇來源是否被概念頁用到、名詞表連結。

### 製作簡報（Query 的一種）

1. 依學習目標查 Wiki，把大綱寫成 `deck/outline.json`：每個重點都附主張編號，或標成比喻／示意例子。
2. **大綱檢查（先於產生簡報）**：`check_deck.py --content-only` 檢查出處、數字、名詞順序、目標覆蓋、份量。不通過就改大綱；如果是 Wiki 缺內容，回到 Ingest 補 Wiki。
3. `pipeline/render_deck.py` 依大綱產生 `docs/slides/index.html`，並把對應表存回 `wiki/queries/deck-outline.md`。
4. **畫面檢查**：`check_deck.py` 用無頭瀏覽器檢查溢出（含 SVG 文字）、連結、換頁，並存每頁截圖；AI 也要看截圖。
5. **AI 審查**：把 `review_packet.md` 分成兩份，交給兩個沒看過製作過程的 AI：新手只拿簡報文字（不含答案），事實查核只拿「重點↔主張」對照。
6. 有錯就回到對應節點修正，再從那個節點之後的檢查重跑。
7. **停止條件**：事實查核沒有「不支持」，而且新手測驗全對，就不再送下一輪 AI 審查；最後一輪修正只重跑程式檢查。

## 流程圖

### v2（目前使用，2026-11-23 第一次完整執行後修改）

```text
階段一（每篇資料一次）
取得資料 → 討論重點 → 寫入一頁 → 單頁檢查 ─(不通過)→ 寫入一頁
                                   │通過，下一頁／下一篇
                                   ▼
                              Wiki 檢查（整體結構）
階段二
查詢 Wiki → 整理大綱 → 大綱檢查 ─(不通過)→ 整理大綱（Wiki 缺內容 → 回階段一）
                          │通過
                          ▼
              產生簡報 → 畫面檢查 ─(不通過)→ 改版型／改大綱
                          │通過
                          ▼
                       AI 審查 ─(不通過)→ 改大綱或改 Wiki
                          │通過
                          ▼
                         發布
```

v1 → v2 改了什麼、為什麼，見 `report/workflow.md`。

### v1（第一次執行時使用）

```text
取得資料 → 討論重點 → 寫入 Wiki → Wiki 檢查 ─(不通過)→ 寫入 Wiki
                                     │通過
                                     ▼
          查詢 Wiki → 整理大綱 → 產生簡報 → 簡報檢查 ─(不通過)→ 整理大綱
                                                 │通過
                                                 ▼
                                               發布
```

## 指令

```bash
.venv/bin/python -I pipeline/fetch_sources.py      # 節點 1
.venv/bin/python -I pipeline/lint_wiki.py --page wiki/sources/<slug>.md   # 單頁檢查（寫完一頁就跑）
.venv/bin/python -I pipeline/lint_wiki.py          # Wiki 檢查（整體）
.venv/bin/python -I pipeline/check_deck.py --content-only   # 大綱檢查（產生簡報前）
.venv/bin/python -I pipeline/render_deck.py        # 產生簡報
.venv/bin/python -I pipeline/check_deck.py --out runs/<run>/   # 簡報檢查（大綱＋畫面）＋審查材料
.venv/bin/python -I pipeline/build_site.py         # 產生 docs/ 網站
```

## 文字規則

- 繁體中文、臺灣用語。名詞第一次出現時附英文原文。
- 不誇大：來源怎麼說就怎麼寫，不把單一實驗的數字寫成普遍定律。
- 不虛構來源、數字或引文。查不到就寫「來源沒有提到」。
