# A. 簡報文字（不含答案）

## 第 1 頁：RAG 是什麼？

## 第 2 頁：今天的目標
- 目標 O1：說出只靠模型記憶會有哪些問題，以及 RAG 怎麼補
- 目標 O2：依序說明 RAG 的三個步驟各在做什麼
- 目標 O3：分辨關鍵字檢索與語意檢索，知道為什麼要混合
- 目標 O4：指出 RAG 會出錯的地方，以及怎麼檢查答案
- 路線：問題：模型只靠記憶→做法：RAG 三步驟→細節：怎麼找資料→會出錯的地方與檢查→延伸：LLM Wiki

## 第 3 頁：先想一個問題
- 〔例子〕問聊天機器人：「這學期的退選截止日是哪天？」
- 〔例子〕它可能回答得很有自信，日期卻是錯的
- 〔例子〕它也說不出這個日期是從哪裡看來的
- 〔圖：chat〕這學期的退選截止日是哪天？；退選截止日是 11 月 30 日。；示意對話，日期為虛構

## 第 4 頁：為什麼會這樣：模型只靠「記憶」
- 大型語言模型（LLM）把訓練時讀到的知識存在參數裡，稱為參數記憶
- 缺點一：不容易更新，世界變了，模型不會知道
- 缺點二：很難說清楚答案是怎麼來的
- 缺點三：可能幻覺，寫出聽起來合理、其實錯誤的內容
- 〔圖：table〕名詞；白話意思；參數；模型內部的大量數字；訓練；讀大量文字，反覆調整參數；參數記憶；用參數存下來的知識

## 第 5 頁：解法：把閉卷考試變成開卷考試
- 〔比喻〕閉卷考試只能靠記憶；開卷考試可以先翻書再作答
- RAG（檢索增強生成）：回答前，先從外部資料庫找相關資料
- 再把資料和問題一起交給模型，根據資料寫答案
- 資料庫可以直接修改，用了哪些資料也能攤開檢查
- 〔圖：books〕

## 第 6 頁：RAG 的三個步驟
- 建索引：事前把文件整理成可以搜尋的資料庫
- 檢索：由檢索器找出最相關的前 K 塊資料（K 由自己設定）
- 生成：把問題和找到的資料放進提示詞，交給模型回答
- 〔圖：pipeline〕建索引；事前做一次；把文件整理成資料庫；檢索；每次提問；找出最相關的前 K 塊資料；生成；每次提問；問題＋資料 → 模型寫答案

## 第 7 頁：步驟一：建索引（1）切塊
- 切塊：把長文件切成一段段短文字，方便逐段比對
- 提出 RAG 的論文把維基百科每 100 個英文詞切一塊，共 2,100 萬塊
- 實務上每塊通常不超過數百個 token（模型讀文字的單位）
- 切太大雜訊多；切太小可能看不懂前後文
- 〔圖：chunks〕

## 第 8 頁：步驟一：建索引（2）轉成向量
- 向量嵌入：由嵌入模型把一段文字轉成一串代表意思的數字
- 〔比喻〕像地圖上的點：意思越近，點離得越近
- 「bad guy」和「villain」用字不同，轉成向量後卻可能很接近
- 提問時，問題也轉成向量，再跟每一塊比遠近
- 〔圖：vector-map〕

## 第 9 頁：步驟二：檢索有兩種找法
- BM25：傳統的關鍵字檢索，看字面有沒有出現
- 語意檢索：比較向量的遠近，換句話說也比較找得到
- 向量可能漏掉「TS-999」這種精確代碼，BM25 比對字面就找得到
- 混合檢索：兩種各找一批，再合併、去掉重複
- 〔圖：table〕；關鍵字檢索 BM25；語意檢索；比什麼；字面有沒有出現；意思近不近；擅長；代碼、專有名詞；換句話說、同義詞；例子；「TS-999」；bad guy → villain

## 第 10 頁：跟著一個問題走一遍
- 〔例子〕以「校園問答機器人」為例，從建索引一路走到回答
- 〔圖：walkthrough〕示意例子：手冊、章節與時間都是虛構的；建索引；把《學生手冊》切塊，每塊轉成向量，存進資料庫；提問；「期末考週圖書館開到幾點？」也轉成向量；檢索；找出最接近的 3 塊，其中一塊寫著「考試週延長開放至 24:00」；生成；提示詞：「根據以下資料回答問題：〔3 塊資料〕問題：……」；回答；「考試週開到 24:00（出自《學生手冊》第 4 章）」

## 第 11 頁：好處：換掉資料庫，就能更新知識
- 換用 2016 或 2018 年的維基百科當資料庫，問 82 位各國領袖是誰
- 年份對得上：答對 70%、68%；對不上：只剩 12%、4%
- 只換資料庫，模型沒有重新訓練
- 出題任務的人工評比：42.7% 認為 RAG 較符合事實，7.1% 相反
- 〔圖：bars〕%；答對比例；2016 資料庫問 2016 年領袖；70；2018 資料庫問 2018 年領袖；68；2018 資料庫問 2016 年領袖；12；2016 資料庫問 2018 年領袖；4

## 第 12 頁：RAG 和微調有什麼不同？
- 微調：用新資料再訓練模型，改變模型參數
- 綜述論文的比喻：RAG 像給模型一本專用課本，微調像學生把知識內化
- RAG 換資料就能更新；微調適合學固定的格式與風格
- 兩者不互斥，可以一起用
- 〔圖：table〕；RAG；微調；改了什麼；外部資料庫；模型參數；更新知識；換資料就好；要重新訓練；指出依據；可以；不容易

## 第 13 頁：出錯①：找不到對的資料
- 切塊會丟掉前後文：「營收成長 3%」單看不知道是哪家公司
- 改法：由 AI 替每塊前面補一段 50–100 token 的說明
- 重排：先粗找一大批（原文 150 塊），再由重排模型打分，留 20 塊
- 三招合用後，前 20 塊找不到資料的比例 5.7% → 1.9%
- 〔圖：bars〕%；找不到資料的比例（越低越好）；原本；5.7；＋補說明（只用向量檢索）；3.7；＋補說明（向量＋BM25）；2.9；＋重排；1.9

## 第 14 頁：出錯②：找到了，卻沒用好
- 上下文：模型一次讀進去的全部文字（問題＋資料）
- 含答案的那塊資料放開頭或結尾，通常答得最好；放長文中間明顯變差
- 以 GPT-3.5-Turbo 為例：放中間時，正確率低於不給資料的 56.1%
- 從 20 塊加到 50 塊，兩個模型的正確率只多約 1%–1.5%
- 〔圖：u-curve〕56.1；不給資料（閉卷）56.1%；示意曲線，形狀依原論文圖 1

## 第 15 頁：出錯③：沒照資料寫，怎麼檢查？
- RAG 不保證不幻覺：模型仍可能寫出資料裡沒有的內容
- 忠實度：答案要建立在找回來的資料上，每句都要有依據
- 算法：讓 LLM 把答案拆成短句，逐句判斷有沒有依據，算比例
- 另外兩個分數：找回的資料相不相關、答案有沒有切題
- 〔圖：faithfulness〕示意例子｜答案：考試週圖書館開到 24:00，週末也照常開放，而且免費借筆電。｜拆句：考試週開到 24:00（有依據 ✓）；週末照常開放（有依據 ✓）；免費借筆電（沒依據 ✗）｜忠實度 2/3

## 第 16 頁：延伸：RAG 的演進，與這份簡報的來源
- RAG 持續演進：基本型 → 進階型（檢索前後加處理）→ 模組型
- 一般 RAG 每次提問都重新從原文找片段，整理過的結果不會留下
- LLM Wiki：AI 事先把資料整理成有出處的筆記，查詢結果也能存回去
- 〔本專案說明〕這份簡報就是查詢這個 Wiki 的結果，每頁都附出處
- 〔圖：timeline〕基本型（Naive）；建索引 → 檢索 → 生成；進階型（Advanced）；檢索前改寫問題、檢索後重排；模組型（Modular）；模組可替換、可多次檢索；LLM Wiki；事先整理、持續累積的知識

## 第 17 頁：小測驗（上）
- 題目：下列哪一項「不是」只靠參數記憶的缺點？　選項：A. 難以更新／B. 說不出依據／C. 可能幻覺／D. 一定要連網才能回答
- 題目：RAG 的三個步驟，正確順序是？　選項：A. 檢索 → 建索引 → 生成／B. 建索引 → 檢索 → 生成／C. 生成 → 檢索 → 建索引／D. 建索引 → 生成 → 檢索

## 第 18 頁：小測驗（下）
- 題目：使用者搜尋錯誤代碼「TS-999」，哪一種檢索最不容易漏掉？　選項：A. 關鍵字檢索 BM25／B. 只用語意檢索／C. 兩者完全一樣／D. 都找不到
- 題目：答案拆成 4 句，其中 3 句能在找回的資料裡找到依據，忠實度是多少？　選項：A. 1/4／B. 3/4／C. 4/3／D. 無法計算

## 第 19 頁：重點回顧
- 只靠參數記憶：不易更新、難說清依據、可能幻覺
- RAG＝建索引 → 檢索 → 生成，回答前先查資料
- 關鍵字檢索看字面、語意檢索看意思，兩者互補
- 可能找不到、沒用好、沒照資料寫；用忠實度檢查答案


# B. 每個重點與它引用的 Wiki 主張

- 第 4 頁「大型語言模型（LLM）把訓練時讀到的知識存在參數裡，稱為參數記憶」
  - S1-c1｜語言模型把知識存在參數裡；只靠這種記憶有三個缺點：不易更新、難說明預測依據、可能產生幻覺｜證據：Large pre-trained language models have been shown to store factual knowledge in their parameters / They cannot easily expand or revise their memory, can’t straightforwardly provide insight into their predictions, and may produce “hallucinations”
- 第 4 頁「缺點一：不容易更新，世界變了，模型不會知道」
  - S1-c1｜語言模型把知識存在參數裡；只靠這種記憶有三個缺點：不易更新、難說明預測依據、可能產生幻覺｜證據：Large pre-trained language models have been shown to store factual knowledge in their parameters / They cannot easily expand or revise their memory, can’t straightforwardly provide insight into their predictions, and may produce “hallucinations”
  - S3-c1｜大型語言模型有幻覺、知識過時、推理無法追溯的問題；引入外部資料庫知識的 RAG 被視為有希望的解法｜證據：Large Language Models (LLMs) showcase impressive capabilities but encounter challenges like hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes. / Retrieval-Augmented Generation (RAG) has emerged as a promising solution by incorporating knowledge from external databases.
- 第 4 頁「缺點二：很難說清楚答案是怎麼來的」
  - S1-c1｜語言模型把知識存在參數裡；只靠這種記憶有三個缺點：不易更新、難說明預測依據、可能產生幻覺｜證據：Large pre-trained language models have been shown to store factual knowledge in their parameters / They cannot easily expand or revise their memory, can’t straightforwardly provide insight into their predictions, and may produce “hallucinations”
  - S3-c1｜大型語言模型有幻覺、知識過時、推理無法追溯的問題；引入外部資料庫知識的 RAG 被視為有希望的解法｜證據：Large Language Models (LLMs) showcase impressive capabilities but encounter challenges like hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes. / Retrieval-Augmented Generation (RAG) has emerged as a promising solution by incorporating knowledge from external databases.
- 第 4 頁「缺點三：可能幻覺，寫出聽起來合理、其實錯誤的內容」
  - S1-c1｜語言模型把知識存在參數裡；只靠這種記憶有三個缺點：不易更新、難說明預測依據、可能產生幻覺｜證據：Large pre-trained language models have been shown to store factual knowledge in their parameters / They cannot easily expand or revise their memory, can’t straightforwardly provide insight into their predictions, and may produce “hallucinations”
  - S3-c1｜大型語言模型有幻覺、知識過時、推理無法追溯的問題；引入外部資料庫知識的 RAG 被視為有希望的解法｜證據：Large Language Models (LLMs) showcase impressive capabilities but encounter challenges like hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes. / Retrieval-Augmented Generation (RAG) has emerged as a promising solution by incorporating knowledge from external databases.
- 第 5 頁「RAG（檢索增強生成）：回答前，先從外部資料庫找相關資料」
  - S1-c3｜RAG 由兩個元件組成：檢索器找文件，生成器根據文件與問題產生答案｜證據：a retriever pη (z|x) with parameters η that returns (top-K truncated) distributions over text passages given a query x / retriever (Dense Passage Retriever [26], henceforth DPR) provides latent documents conditioned on the input, and the seq2seq model (BART [32]) then conditions on these latent documents together with the input to generate the output
  - S3-c2｜基本 RAG 有三步：建索引、檢索、生成｜證據：It mainly consists of 3 steps. 1) Indexing. Documents are split into chunks, encoded into vectors, and stored in a vector database. / 2) Retrieval. Retrieve the Top k chunks most relevant to the question based on semantic similarity. 3) Generation. Input the original question and the retrieved chunks together into LLM to generate the final answer.
- 第 5 頁「再把資料和問題一起交給模型，根據資料寫答案」
  - S3-c2｜基本 RAG 有三步：建索引、檢索、生成｜證據：It mainly consists of 3 steps. 1) Indexing. Documents are split into chunks, encoded into vectors, and stored in a vector database. / 2) Retrieval. Retrieve the Top k chunks most relevant to the question based on semantic similarity. 3) Generation. Input the original question and the retrieved chunks together into LLM to generate the final answer.
- 第 5 頁「資料庫可以直接修改，用了哪些資料也能攤開檢查」
  - S1-c2｜結合可檢索的外部記憶，可以解決其中部分問題：知識可以直接修改，也能拿出來檢查｜證據：Hybrid models that combine parametric memory with non-parametric (i.e., retrieval-based) memories [20, 26, 48] can address some of these issues because knowledge can be directly revised and expanded, and accessed knowledge can be inspected and interpreted
- 第 6 頁「建索引：事前把文件整理成可以搜尋的資料庫」
  - S3-c2｜基本 RAG 有三步：建索引、檢索、生成｜證據：It mainly consists of 3 steps. 1) Indexing. Documents are split into chunks, encoded into vectors, and stored in a vector database. / 2) Retrieval. Retrieve the Top k chunks most relevant to the question based on semantic similarity. 3) Generation. Input the original question and the retrieved chunks together into LLM to generate the final answer.
- 第 6 頁「檢索：由檢索器找出最相關的前 K 塊資料（K 由自己設定）」
  - S3-c2｜基本 RAG 有三步：建索引、檢索、生成｜證據：It mainly consists of 3 steps. 1) Indexing. Documents are split into chunks, encoded into vectors, and stored in a vector database. / 2) Retrieval. Retrieve the Top k chunks most relevant to the question based on semantic similarity. 3) Generation. Input the original question and the retrieved chunks together into LLM to generate the final answer.
  - S1-c3｜RAG 由兩個元件組成：檢索器找文件，生成器根據文件與問題產生答案｜證據：a retriever pη (z|x) with parameters η that returns (top-K truncated) distributions over text passages given a query x / retriever (Dense Passage Retriever [26], henceforth DPR) provides latent documents conditioned on the input, and the seq2seq model (BART [32]) then conditions on these latent documents together with the input to generate the output
- 第 6 頁「生成：把問題和找到的資料放進提示詞，交給模型回答」
  - S3-c2｜基本 RAG 有三步：建索引、檢索、生成｜證據：It mainly consists of 3 steps. 1) Indexing. Documents are split into chunks, encoded into vectors, and stored in a vector database. / 2) Retrieval. Retrieve the Top k chunks most relevant to the question based on semantic similarity. 3) Generation. Input the original question and the retrieved chunks together into LLM to generate the final answer.
- 第 7 頁「切塊：把長文件切成一段段短文字，方便逐段比對」
  - S3-c2｜基本 RAG 有三步：建索引、檢索、生成｜證據：It mainly consists of 3 steps. 1) Indexing. Documents are split into chunks, encoded into vectors, and stored in a vector database. / 2) Retrieval. Retrieve the Top k chunks most relevant to the question based on semantic similarity. 3) Generation. Input the original question and the retrieved chunks together into LLM to generate the final answer.
  - S6-c1｜RAG 的前處理：把文件切成通常不超過數百 token 的小塊、轉成向量、存進向量資料庫｜證據：Break down the knowledge base (the “corpus” of documents) into smaller chunks of text, usually no more than a few hundred tokens; / Use an embedding model to convert these chunks into vector embeddings that encode meaning; / Store these embeddings in a vector database that allows for searching by semantic similarity.
- 第 7 頁「提出 RAG 的論文把維基百科每 100 個英文詞切一塊，共 2,100 萬塊」
  - S1-c4｜論文的外部資料庫是維基百科，每 100 個英文詞（word）切成一段，共 2,100 萬段｜證據：Each Wikipedia article is split into disjoint 100-word chunks, to make a total of 21M documents.
- 第 7 頁「實務上每塊通常不超過數百個 token（模型讀文字的單位）」
  - S6-c1｜RAG 的前處理：把文件切成通常不超過數百 token 的小塊、轉成向量、存進向量資料庫｜證據：Break down the knowledge base (the “corpus” of documents) into smaller chunks of text, usually no more than a few hundred tokens; / Use an embedding model to convert these chunks into vector embeddings that encode meaning; / Store these embeddings in a vector database that allows for searching by semantic similarity.
- 第 7 頁「切太大雜訊多；切太小可能看不懂前後文」
  - S3-c6｜切塊大小是取捨：大塊上下文多但雜訊多，小塊雜訊少但可能資訊不完整｜證據：Larger chunks can capture more context, but they also generate more noise, requiring longer processing time and higher costs. While smaller chunks may not fully convey the necessary context, they do have less noise.
- 第 8 頁「「bad guy」和「villain」用字不同，轉成向量後卻可能很接近」
  - S2-c2｜用向量表示意思，換句話說也比較容易找到：「bad guy」比較能對到「villain」｜證據：synonyms or paraphrases that consist of completely different tokens may still be mapped to vectors close to each other / a dense retrieval system would be able to better match “bad guy” with “villain” and fetch the correct context / “Who is the bad guy in lord of the rings?”, which can be answered from the context “Sala Baker is best known for portraying the villain Sauron in the Lord of the Rings trilogy.”
- 第 8 頁「提問時，問題也轉成向量，再跟每一塊比遠近」
  - S3-c3｜基本 RAG 檢索時，用建索引時的同一個編碼模型把問題轉成向量｜證據：the RAG system employs the same encoding model utilized during the indexing phase to transform the query into a vector representation
- 第 9 頁「BM25：傳統的關鍵字檢索，看字面有沒有出現」
  - S2-c1｜傳統的關鍵字檢索（TF-IDF、BM25）是比對字詞，像查索引｜證據：Retrieval in open-domain QA is usually implemented using TF-IDF or BM25 (Robertson and Zaragoza, 2009), which matches keywords efficiently with an inverted index
- 第 9 頁「語意檢索：比較向量的遠近，換句話說也比較找得到」
  - S2-c2｜用向量表示意思，換句話說也比較容易找到：「bad guy」比較能對到「villain」｜證據：synonyms or paraphrases that consist of completely different tokens may still be mapped to vectors close to each other / a dense retrieval system would be able to better match “bad guy” with “villain” and fetch the correct context / “Who is the bad guy in lord of the rings?”, which can be answered from the context “Sala Baker is best known for portraying the villain Sauron in the Lord of the Rings trilogy.”
- 第 9 頁「向量可能漏掉「TS-999」這種精確代碼，BM25 比對字面就找得到」
  - S6-c2｜向量檢索可能漏掉精確比對，例如錯誤代碼「TS-999」；BM25 能補上｜證據：While embedding models excel at capturing semantic relationships, they can miss crucial exact matches. / An embedding model might find content about error codes in general, but could miss the exact "TS-999" match. BM25 looks for this specific text string to identify the relevant documentation.
- 第 9 頁「混合檢索：兩種各找一批，再合併、去掉重複」
  - S6-c8｜混合檢索：BM25 與向量檢索各找一批，再合併、去掉重複｜證據：Use BM25 to find top chunks based on exact matches; / Use embeddings to find top chunks based on semantic similarity; / Combine and deduplicate results from (3) and (4) using rank fusion techniques; / Add the top-K chunks to the prompt to generate the response. / By leveraging both BM25 and embedding models, traditional RAG systems can provide more comprehensive and accurate results
  - S2-c5｜兩種方法各有所長：BM25 擅長罕見關鍵字，DPR 擅長同義改寫｜證據：Term-matching methods like BM25 are sensitive to highly selective keywords and phrases, while DPR captures lexical variations or semantic relationships better. / Results can be improved further in some cases by combining DPR with BM25 in both single- and multi-dataset settings.
- 第 11 頁「換用 2016 或 2018 年的維基百科當資料庫，問 82 位各國領袖是誰」
  - S1-c5｜換掉文件庫就能更新 RAG 的知識；只靠參數的模型則需要再訓練（2016／2018 年版實驗）｜證據：Parametric-only models like T5 or BART need further training to update their behavior as the world changes. / We prepare a list of 82 world leaders who had changed / between these dates and use a template “Who is {position}?” / RAG answers 70% correctly using the 2016 index for 2016 world leaders and 68% using the 2018 index for 2018 world leaders. / Accuracy with mismatched indices is low (12% with the 2018 index and 2016 leaders, 4% with the 2016 index and 2018 leaders). / This shows we can update RAG’s world knowledge by simply replacing its non-parametric memory.
- 第 11 頁「年份對得上：答對 70%、68%；對不上：只剩 12%、4%」
  - S1-c5｜換掉文件庫就能更新 RAG 的知識；只靠參數的模型則需要再訓練（2016／2018 年版實驗）｜證據：Parametric-only models like T5 or BART need further training to update their behavior as the world changes. / We prepare a list of 82 world leaders who had changed / between these dates and use a template “Who is {position}?” / RAG answers 70% correctly using the 2016 index for 2016 world leaders and 68% using the 2018 index for 2018 world leaders. / Accuracy with mismatched indices is low (12% with the 2018 index and 2016 leaders, 4% with the 2016 index and 2018 leaders). / This shows we can update RAG’s world knowledge by simply replacing its non-parametric memory.
- 第 11 頁「只換資料庫，模型沒有重新訓練」
  - S1-c5｜換掉文件庫就能更新 RAG 的知識；只靠參數的模型則需要再訓練（2016／2018 年版實驗）｜證據：Parametric-only models like T5 or BART need further training to update their behavior as the world changes. / We prepare a list of 82 world leaders who had changed / between these dates and use a template “Who is {position}?” / RAG answers 70% correctly using the 2016 index for 2016 world leaders and 68% using the 2018 index for 2018 world leaders. / Accuracy with mismatched indices is low (12% with the 2018 index and 2016 leaders, 4% with the 2016 index and 2018 leaders). / This shows we can update RAG’s world knowledge by simply replacing its non-parametric memory.
- 第 11 頁「出題任務的人工評比：42.7% 認為 RAG 較符合事實，7.1% 相反」
  - S1-c6｜在出題任務的人工評比中，評審較常認為 RAG（RAG-Token）比純生成模型 BART 更符合事實｜證據：human evaluation results, over 452 pairs of generations from BART and RAG-Token / Evaluators indicated that BART was more factual than RAG in only 7.1% of cases, while RAG was more factual in 42.7% of cases
- 第 12 頁「綜述論文的比喻：RAG 像給模型一本專用課本，微調像學生把知識內化」
  - S3-c7｜RAG 像給模型一本專用課本；微調像學生把知識內化，適合學格式與風格｜證據：RAG can be likened to providing a model with a tailored textbook for information retrieval, ideal for precise information retrieval tasks. In contrast, FT is comparable to a student internalizing knowledge over time, suitable for scenarios requiring replication of specific structures, styles, or formats. / RAG and FT are not mutually exclusive and can complement each other
- 第 12 頁「RAG 換資料就能更新；微調適合學固定的格式與風格」
  - S3-c7｜RAG 像給模型一本專用課本；微調像學生把知識內化，適合學格式與風格｜證據：RAG can be likened to providing a model with a tailored textbook for information retrieval, ideal for precise information retrieval tasks. In contrast, FT is comparable to a student internalizing knowledge over time, suitable for scenarios requiring replication of specific structures, styles, or formats. / RAG and FT are not mutually exclusive and can complement each other
  - S1-c5｜換掉文件庫就能更新 RAG 的知識；只靠參數的模型則需要再訓練（2016／2018 年版實驗）｜證據：Parametric-only models like T5 or BART need further training to update their behavior as the world changes. / We prepare a list of 82 world leaders who had changed / between these dates and use a template “Who is {position}?” / RAG answers 70% correctly using the 2016 index for 2016 world leaders and 68% using the 2018 index for 2018 world leaders. / Accuracy with mismatched indices is low (12% with the 2018 index and 2016 leaders, 4% with the 2016 index and 2018 leaders). / This shows we can update RAG’s world knowledge by simply replacing its non-parametric memory.
- 第 12 頁「兩者不互斥，可以一起用」
  - S3-c7｜RAG 像給模型一本專用課本；微調像學生把知識內化，適合學格式與風格｜證據：RAG can be likened to providing a model with a tailored textbook for information retrieval, ideal for precise information retrieval tasks. In contrast, FT is comparable to a student internalizing knowledge over time, suitable for scenarios requiring replication of specific structures, styles, or formats. / RAG and FT are not mutually exclusive and can complement each other
- 第 13 頁「切塊會丟掉前後文：「營收成長 3%」單看不知道是哪家公司」
  - S6-c3｜切塊會丟掉上下文：「營收成長 3%」這一塊本身沒寫是哪家公司、哪一季｜證據：A relevant chunk might contain the text: "The company's revenue grew by 3% over the previous quarter." However, this chunk on its own doesn't specify which company it's referring to or the relevant time period, making it difficult to retrieve the right information or use the information effectively
- 第 13 頁「改法：由 AI 替每塊前面補一段 50–100 token 的說明」
  - S6-c4｜情境化檢索：在每塊前面補一段說明（通常 50 到 100 token），再建向量與 BM25 索引｜證據：To implement Contextual Retrieval, we turn to Claude. / The resulting contextual text, usually 50-100 tokens, is prepended to the chunk before embedding it and before creating the BM25 index. / This chunk is from an SEC filing on ACME corp's performance in Q2 2023 / Here is the chunk we want to situate within the whole document
- 第 13 頁「重排：先粗找一大批（原文 150 塊），再由重排模型打分，留 20 塊」
  - S6-c6｜重排：先粗找一大批（文中 150 塊），再用重排模型逐塊打分，只留最好的（文中 20 塊）｜證據：Perform initial retrieval to get the top potentially relevant chunks (we used the top 150); / Using a reranking model, give each chunk a score based on its relevance and importance to the prompt, then select the top-K chunks (we used the top 20);
- 第 13 頁「三招合用後，前 20 塊找不到資料的比例 5.7% → 1.9%」
  - S6-c5｜效果：找不到資料的比例下降 35%、49%，加上重排後下降 67%｜證據：Contextual Embeddings reduced the top-20-chunk retrieval failure rate by 35% (5.7% → 3.7%). / Combining Contextual Embeddings and Contextual BM25 reduced the top-20-chunk retrieval failure rate by 49% (5.7% → 2.9%). / Reranked Contextual Embedding and Contextual BM25 reduced the top-20-chunk retrieval failure rate by 67% (5.7% → 1.9%).
- 第 14 頁「含答案的那塊資料放開頭或結尾，通常答得最好；放長文中間明顯變差」
  - S4-c1｜模型的表現常呈 U 型：相關資料在開頭或結尾時通常最好，在長篇內容的中間時明顯變差｜證據：performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts / k documents (e.g., passages from Wikipedia), where exactly one of the documents contains the answer
- 第 14 頁「以 GPT-3.5-Turbo 為例：放中間時，正確率低於不給資料的 56.1%」
  - S4-c2｜答案放在中間時，GPT-3.5-Turbo 甚至比完全不給文件時還差｜證據：when relevant information is placed in the middle of its input context, GPT-3.5-Turbo’s performance on the multi-document question task is lower than its performance when predicting without any documents (i.e., the closed-book setting; 56.1%) / in 20- and 30-document settings is lower than performance without any input documents (i.e., closedbook performance; 56.1%)
- 第 14 頁「從 20 塊加到 50 塊，兩個模型的正確率只多約 1%–1.5%」
  - S4-c4｜多給文件的效益很快飽和：從 20 篇加到 50 篇，GPT-3.5-Turbo 只多約 1.5%、Claude-1.3 只多約 1%｜證據：using 50 documents instead of 20 retrieved documents only marginally improves performance (∼1.5% for GPT-3.5-Turbo and ∼1% for claude-1.3) / Using more than 20 retrieved documents only marginally improves reader performance (∼1.5% for GPT-3.5Turbo and ∼1% for Claude-1.3), while significantly increasing the input context length (and thus latency and cost).
- 第 15 頁「RAG 不保證不幻覺：模型仍可能寫出資料裡沒有的內容」
  - S3-c4｜基本 RAG 的毛病：檢索常找錯或漏找資料，生成時也可能寫出資料裡沒有的內容｜證據：The retrieval phase often struggles with precision and recall, leading to the selection of misaligned or irrelevant chunks, and the missing of crucial information. / the model may face the issue of hallucination, where it produces content not supported by the retrieved context
- 第 15 頁「忠實度：答案要建立在找回來的資料上，每句都要有依據」
  - S5-c1｜忠實度：答案應該建立在找回來的資料上｜證據：Faithfulness refers to the idea that the answer should be grounded in the given context.
  - S5-c3｜忠實度的算法：把答案拆成短句，逐條檢查能否從資料推出，算出支持的比例｜證據：we first use an LLM to extract a set of statements / the LLM determines if si can be inferred from c(q) using a verification function / is the number of statements that were supported according to the LLM and |S| is the total number of statements
- 第 15 頁「算法：讓 LLM 把答案拆成短句，逐句判斷有沒有依據，算比例」
  - S5-c3｜忠實度的算法：把答案拆成短句，逐條檢查能否從資料推出，算出支持的比例｜證據：we first use an LLM to extract a set of statements / the LLM determines if si can be inferred from c(q) using a verification function / is the number of statements that were supported according to the LLM and |S| is the total number of statements
- 第 15 頁「另外兩個分數：找回的資料相不相關、答案有沒有切題」
  - S5-c2｜答案切題度與資料相關性：答案要回應問題，找回的資料要精簡｜證據：Answer Relevance refers to the idea that the generated answer should address the actual question that was provided. / Context Relevance refers to the idea that the retrieved context should be focused, containing as little irrelevant information as possible.
  - S3-c8｜評估 RAG 有三個品質分數：資料相關性、答案忠實度、答案切題度｜證據：Quality scores include context relevance, answer faithfulness, and answer relevance.
- 第 16 頁「RAG 持續演進：基本型 → 進階型（檢索前後加處理）→ 模組型」
  - S3-c5｜RAG 的演進分成 Naive、Advanced、Modular 三個階段｜證據：we categorize it into three stages: Naive RAG, Advanced RAG, and Modular RAG / Focusing on enhancing retrieval quality, it employs pre-retrieval and post-retrieval strategies. / Modular RAG offers remarkable adaptability by allowing module substitution or reconfiguration to address specific challenges.
- 第 16 頁「一般 RAG 每次提問都重新從原文找片段，整理過的結果不會留下」
  - S7-c1｜一般 RAG 每次提問都從頭找資料，知識沒有累積｜證據：Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. / the LLM is rediscovering knowledge from scratch on every question. There's no accumulation.
- 第 16 頁「LLM Wiki：AI 事先把資料整理成有出處的筆記，查詢結果也能存回去」
  - S7-c2｜LLM Wiki 讓 LLM 逐步建立並維護一個持續存在的 Wiki｜證據：the LLM **incrementally builds and maintains a persistent wiki** / When you add a new source, the LLM doesn't just index it for later retrieval. It reads it, extracts the key information, and integrates it into the existing wiki
  - S7-c5｜好的查詢結果可以存回 Wiki，簡報也是查詢結果的一種｜證據：**good answers can be filed back into the wiki as new pages.** / Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (Marp), a chart (matplotlib), a canvas.
- 第 19 頁「只靠參數記憶：不易更新、難說清依據、可能幻覺」
  - S1-c1｜語言模型把知識存在參數裡；只靠這種記憶有三個缺點：不易更新、難說明預測依據、可能產生幻覺｜證據：Large pre-trained language models have been shown to store factual knowledge in their parameters / They cannot easily expand or revise their memory, can’t straightforwardly provide insight into their predictions, and may produce “hallucinations”
- 第 19 頁「RAG＝建索引 → 檢索 → 生成，回答前先查資料」
  - S3-c2｜基本 RAG 有三步：建索引、檢索、生成｜證據：It mainly consists of 3 steps. 1) Indexing. Documents are split into chunks, encoded into vectors, and stored in a vector database. / 2) Retrieval. Retrieve the Top k chunks most relevant to the question based on semantic similarity. 3) Generation. Input the original question and the retrieved chunks together into LLM to generate the final answer.
- 第 19 頁「關鍵字檢索看字面、語意檢索看意思，兩者互補」
  - S2-c5｜兩種方法各有所長：BM25 擅長罕見關鍵字，DPR 擅長同義改寫｜證據：Term-matching methods like BM25 are sensitive to highly selective keywords and phrases, while DPR captures lexical variations or semantic relationships better. / Results can be improved further in some cases by combining DPR with BM25 in both single- and multi-dataset settings.
- 第 19 頁「可能找不到、沒用好、沒照資料寫；用忠實度檢查答案」
  - S3-c4｜基本 RAG 的毛病：檢索常找錯或漏找資料，生成時也可能寫出資料裡沒有的內容｜證據：The retrieval phase often struggles with precision and recall, leading to the selection of misaligned or irrelevant chunks, and the missing of crucial information. / the model may face the issue of hallucination, where it produces content not supported by the retrieved context
  - S4-c1｜模型的表現常呈 U 型：相關資料在開頭或結尾時通常最好，在長篇內容的中間時明顯變差｜證據：performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts / k documents (e.g., passages from Wikipedia), where exactly one of the documents contains the answer
  - S5-c1｜忠實度：答案應該建立在找回來的資料上｜證據：Faithfulness refers to the idea that the answer should be grounded in the given context.
