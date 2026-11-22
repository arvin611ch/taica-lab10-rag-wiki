# Wiki 主張審查材料

每條主張：中文標題、白話說明、英文證據（逐字出自原文）。

## S1｜Lewis et al. 2020：RAG 原始論文

### S1-c1｜語言模型把知識存在參數裡；只靠這種記憶有三個缺點：不易更新、難說明預測依據、可能產生幻覺
- 證據：Large pre-trained language models have been shown to store factual knowledge in their parameters
- 證據：They cannot easily expand or revise their memory, can’t straightforwardly provide insight into their predictions, and may produce “hallucinations”
- 說明：白話說明：語言模型把訓練時讀到的知識「壓」進模型的參數裡。這種記憶不容易直接改、很難看出模型為什麼這樣回答，還可能一本正經地編造內容。見 [參數記憶與幻覺](../concepts/parametric-memory.md)。

### S1-c2｜加上可檢索的外部記憶後，知識可以直接修改，也能拿出來檢查
- 證據：knowledge can be directly revised and expanded, and accessed knowledge can be inspected and interpreted
- 說明：白話說明：外部記憶就是一個可以查的文件庫。要更新知識，改文件庫就好；模型用了哪幾段資料，也可以直接攤開來看。

### S1-c3｜RAG 由兩個元件組成：檢索器找文件，生成器根據文件與問題產生答案
- 證據：a retriever pη (z|x) with parameters η that returns (top-K truncated) distributions over text passages given a query x
- 證據：the seq2seq model (BART [32]) then conditions on these latent documents together with the input to generate the output
- 說明：白話說明：論文中的檢索器是 [DPR](s2-karpukhin-2020-dpr.md)，生成器是 BART 模型。檢索器回傳前 K 份最相關的段落，生成器把問題和這些段落一起讀進去再寫答案。見 [檢索器](../concepts/retriever.md)。

### S1-c4｜論文的外部資料庫是維基百科，每 100 個英文詞（word）切成一段，共 2,100 萬段
- 證據：Each Wikipedia article is split into disjoint 100-word chunks, to make a total of 21M documents.
- 說明：白話說明：這就是「切塊」：把長文章切成固定長度的小段，才能一段一段比對。見 [切塊](../concepts/chunking.md)。

### S1-c5｜換掉文件庫，答案就跟著新資料改變；只靠參數的模型則需要再訓練（2016／2018 年版實驗）
- 證據：Parametric-only models like T5 or BART need further training to update their behavior as the world changes.
- 證據：We prepare a list of 82 world leaders who had changed
- 證據：RAG answers 70% correctly using the 2016 index for 2016 world leaders and 68% using the 2018 index for 2018 world leaders.
- 證據：Accuracy with mismatched indices is low (12% with the 2018 index and 2016 leaders, 4% with the 2016 index and 2018 leaders).
- 證據：This shows we can update RAG’s world knowledge by simply replacing its non-parametric memory.
- 說明：白話說明：作者準備了 82 位在 2016 到 2018 年間換人的各國領袖，問「某職位現在是誰？」。用 2016 年的維基百科當文件庫，就答對 2016 年的領袖 70%；換成 2018 年的文件庫，就答對 2018 年的領袖 68%。文件庫和題目年份對不上時，正確率掉到 12% 和 4%。模型本身從頭到尾沒有重新訓練。

### S1-c6｜人工評比時，RAG 產生的題目比純生成模型更符合事實
- 證據：human evaluation results, over 452 pairs of generations from BART and RAG-Token
- 證據：Evaluators indicated that BART was more factual than RAG in only 7.1% of cases, while RAG was more factual in 42.7% of cases
- 說明：白話說明：評審比較 452 組由 BART（沒有檢索）和 RAG 產生的益智題目。認為 RAG 比較符合事實的有 42.7%，認為 BART 比較符合事實的只有 7.1%。這是單一任務的結果，不代表 RAG 永遠不會出錯。

## S2｜Karpukhin et al. 2020：DPR 稠密段落檢索

### S2-c1｜傳統的關鍵字檢索（TF-IDF、BM25）是比對字詞，像查索引
- 證據：Retrieval in open-domain QA is usually implemented using TF-IDF or BM25 (Robertson and Zaragoza, 2009), which matches keywords efficiently with an inverted index
- 說明：白話說明：關鍵字檢索看的是問題裡的詞有沒有出現在文件裡。見 [關鍵字檢索 BM25](../concepts/bm25.md)。

### S2-c2｜用向量表示意思，換句話說也比較容易找到：「bad guy」比較能對到「villain」
- 證據：synonyms or paraphrases that consist of completely different tokens may still be mapped to vectors close to each other
- 證據：a dense retrieval system would be able to better match “bad guy” with “villain” and fetch the correct context
- 說明：白話說明：問「魔戒裡的壞人是誰？」，答案段落寫的是「反派索倫」。兩句沒有共同的關鍵字，關鍵字檢索很難找到；向量檢索看的是意思，比較有機會找到。見 [向量嵌入](../concepts/embedding.md)。

### S2-c3｜DPR 用兩個編碼器，分別把問題和段落轉成向量，再用內積找最接近的段落
- 證據：the embedding is optimized for maximizing inner products of the question and relevant passage vectors
- 說明：白話說明：「雙編碼器」就是兩個轉換器：一個專門轉問題、一個專門轉段落。訓練目標是讓「問題」和「能回答它的段落」的向量越接近越好。見 [檢索器](../concepts/retriever.md)。

### S2-c4｜在前 20 筆的檢索準確率上，DPR 比 BM25 高 9 到 19 個百分點
- 證據：our dense retriever outperforms a strong LuceneBM25 system greatly by 9%-19% absolute in terms of top-20 passage retrieval accuracy
- 說明：白話說明：「前 20 筆準確率」是指檢索器找回的前 20 段裡，至少有一段含有答案的比例。差距隨資料集不同，在 9 到 19 個百分點之間。

### S2-c5｜兩種方法各有所長：BM25 擅長罕見關鍵字，DPR 擅長同義改寫
- 證據：Term-matching methods like BM25 are sensitive to highly selective keywords and phrases, while DPR captures lexical variations or semantic relationships better.
- 證據：Results can be improved further in some cases by combining DPR with BM25 in both single- and multi-dataset settings.
- 說明：白話說明：遇到專有名詞、編號、少見人名，字面比對反而準；遇到換句話說，向量比對比較好。論文也發現把兩者分數合併，有些情況下結果更好。
- 說明：這是 [混合檢索](../concepts/hybrid-search.md) 的理由。

## S3｜Gao et al. 2023：大型語言模型的 RAG 綜述

### S3-c1｜大型語言模型會幻覺、知識會過時、推理過程無法追溯；RAG 用外部資料庫來補
- 證據：Large Language Models (LLMs) showcase impressive capabilities but encounter challenges like hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes.
- 說明：白話說明：跟 [S1-c1](s1-lewis-2020-rag.md#s1-c1) 說的是同一組問題，只是對象換成 ChatGPT 這類大型語言模型。見 [參數記憶與幻覺](../concepts/parametric-memory.md)。

### S3-c2｜基本 RAG 有三步：建索引、檢索、生成
- 證據：It mainly consists of 3 steps. 1) Indexing. Documents are split into chunks, encoded into vectors, and stored in a vector database.
- 證據：2) Retrieval. Retrieve the Top k chunks most relevant to the question based on semantic similarity. 3) Generation. Input the original question and the retrieved chunks together into LLM to generate the final answer.
- 說明：白話說明：建索引是事前準備（切塊、轉向量、存起來）；使用者發問時才做檢索與生成。見 [檢索增強生成](../concepts/rag.md)。

### S3-c3｜檢索時，問題要用跟建索引時同一個模型轉成向量
- 證據：the RAG system employs the same encoding model utilized during the indexing phase to transform the query into a vector representation
- 說明：白話說明：問題和文件要放在同一個「向量空間」裡才能比遠近，所以必須用同一個嵌入模型。見 [向量嵌入](../concepts/embedding.md)。

### S3-c4｜基本 RAG 常見的毛病：找錯或漏找資料，以及寫出資料裡沒有的內容
- 證據：The retrieval phase often struggles with precision and recall, leading to the selection of misaligned or irrelevant chunks, and the missing of crucial information.
- 證據：the model may face the issue of hallucination, where it produces content not supported by the retrieved context
- 說明：白話說明：RAG 不會讓幻覺消失。檢索可能找錯，模型也可能沒照著資料寫。見 [RAG 的常見失敗](../concepts/rag-failures.md)。

### S3-c5｜RAG 的演進分成 Naive、Advanced、Modular 三個階段
- 證據：we categorize it into three stages: Naive RAG, Advanced RAG, and Modular RAG
- 證據：Focusing on enhancing retrieval quality, it employs pre-retrieval and post-retrieval strategies.
- 證據：Modular RAG offers remarkable adaptability by allowing module substitution or reconfiguration to address specific challenges.
- 說明：白話說明：Advanced RAG 在檢索前改寫問題、檢索後重排與精簡資料；Modular RAG 把流程拆成可以替換、重組的模組，例如多次檢索、視情況決定要不要檢索。見 [RAG 的三個階段](../concepts/rag-paradigms.md)。

### S3-c6｜切塊大小是取捨：大塊上下文多但雜訊多，小塊雜訊少但可能資訊不完整
- 證據：Larger chunks can capture more context, but they also generate more noise, requiring longer processing time and higher costs. While smaller chunks may not fully convey the necessary context, they do have less noise.
- 說明：白話說明：見 [切塊](../concepts/chunking.md)。

### S3-c7｜RAG 像給模型一本專用課本；微調像學生把知識內化，適合學格式與風格
- 證據：RAG can be likened to providing a model with a tailored textbook for information retrieval, ideal for precise information retrieval tasks. In contrast, FT is comparable to a student internalizing knowledge over time, suitable for scenarios requiring replication of specific structures, styles, or formats.
- 證據：RAG and FT are not mutually exclusive and can complement each other
- 說明：白話說明：「微調」（fine-tuning）是拿新資料再訓練模型、改變模型參數。RAG 不改模型，只在回答時給資料。兩者可以並用。見 [RAG 與微調](../concepts/rag-vs-finetuning.md)。

### S3-c8｜評估 RAG 有三個品質分數：資料相關性、答案忠實度、答案切題度
- 證據：Quality scores include context relevance, answer faithfulness, and answer relevance.
- 說明：白話說明：見 [怎麼評估 RAG](../concepts/rag-evaluation.md)。

## S4｜Liu et al. 2023：Lost in the Middle

### S4-c1｜模型的表現常呈 U 型：相關資料在開頭或結尾時通常最好，在長篇內容的中間時明顯變差
- 證據：performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts
- 證據：k documents (e.g., passages from Wikipedia), where exactly one of the documents contains the answer
- 說明：白話說明：實驗一次給模型好幾篇文件，其中只有一篇含有答案，再移動那篇的位置。正確率畫出來像字母 U。見 [長上下文的位置效應](../concepts/lost-in-the-middle.md)。

### S4-c2｜答案放在中間時，GPT-3.5-Turbo 甚至比完全不給文件時還差
- 證據：when relevant information is placed in the middle of its input context, GPT-3.5-Turbo’s performance on the multi-document question task is lower than its performance when predicting without any documents (i.e., the closed-book setting; 56.1%)
- 證據：in 20- and 30-document settings is lower than performance without any input documents (i.e., closedbook performance; 56.1%)
- 說明：白話說明：不給文件、只靠模型自己記得的內容（閉卷）時正確率是 56.1%。給了 20 或 30 篇文件、但答案剛好在中間時，正確率反而更低。

### S4-c3｜號稱能讀更長內容的模型，不一定比較會用這些內容
- 證據：extended-context models are not necessarily better at using their input context
- 說明：白話說明：模型「放得下」很多文件，不代表它「用得好」。

### S4-c4｜多給文件的效益很快飽和：從 20 篇加到 50 篇只多約 1% 到 1.5%
- 證據：using 50 documents instead of 20 retrieved documents only marginally improves performance
- 證據：Using more than 20 retrieved documents only marginally improves reader performance (∼1.5% for GPT-3.5Turbo and ∼1% for Claude-1.3), while significantly increasing the input context length (and thus latency and cost).
- 說明：白話說明：文件越多，提示詞越長、越慢、越貴，正確率卻幾乎沒變。

### S4-c5｜建議的對策：重排，把相關資料移到前面；或在適當時候少放幾篇
- 證據：effective reranking of retrieved documents (pushing relevant information closer to the start of the input context) or ranked list truncation (retrieving fewer documents when appropriate; Arampatzis et al., 2009) may be promising directions
- 說明：白話說明：這是作者提出的方向，不是已驗證的保證。見 [混合檢索與重排](../concepts/hybrid-search.md)。

## S5｜Es et al. 2023：RAGAS 自動評估

### S5-c1｜忠實度：答案應該建立在找回來的資料上
- 證據：Faithfulness refers to the idea that the answer should be grounded in the given context.
- 說明：白話說明：答案裡的每一句話，都應該能從找回來的資料推得出來。見 [怎麼評估 RAG](../concepts/rag-evaluation.md)。

### S5-c2｜答案切題度與資料相關性：答案要回應問題，找回的資料要精簡
- 證據：Answer Relevance refers to the idea that the generated answer should address the actual question that was provided.
- 證據：Context Relevance refers to the idea that the retrieved context should be focused, containing as little irrelevant information as possible.
- 說明：白話說明：答案可能句句屬實卻答非所問（切題度低）；找回來的資料也可能一大堆、真正有用的只有一句（相關性低）。

### S5-c3｜忠實度的算法：把答案拆成短句，逐條檢查能否從資料推出，算出支持的比例
- 證據：we first use an LLM to extract a set of statements
- 證據：the LLM determines if si can be inferred from c(q) using a verification function
- 證據：is the number of statements that were supported according to the LLM and |S| is the total number of statements
- 說明：例子：答案拆成 4 句，其中 3 句能在資料裡找到依據，忠實度就是 3/4。
- 說明：白話說明：本專案檢查簡報的方式也借用這個想法：每個重點都要對到 Wiki 裡的一條主張。

### S5-c4｜這些指標不需要人工標的標準答案
- 證據：we put forward a suite of metrics which can be used to evaluate these different dimensions without having to rely on ground truth human annotations
- 說明：白話說明：不用先請人寫好「正確答案」，就能大致評估 RAG 系統，適合開發時快速反覆測試。

### S5-c5｜跟人類判斷比，忠實度最準，資料相關性最難評
- 證據：For faithfulness, the Ragas prediction are in general highly accurate.
- 證據：We found context relevance to be the hardest quality dimension to evaluate.
- 說明：白話說明：自動評估也會錯，尤其是判斷「哪些資料是必要的」這一項。

## S6｜Anthropic 2024：Contextual Retrieval

### S6-c1｜RAG 的前處理：把文件切成通常不超過數百 token 的小塊、轉成向量、存進向量資料庫
- 證據：Break down the knowledge base (the “corpus” of documents) into smaller chunks of text, usually no more than a few hundred tokens;
- 證據：Use an embedding model to convert these chunks into vector embeddings that encode meaning;
- 證據：Store these embeddings in a vector database that allows for searching by semantic similarity.
- 說明：白話說明：token 是模型讀文字的基本單位，大約是一個英文單字的一部分或一兩個中文字。見 [切塊](../concepts/chunking.md)、[向量嵌入](../concepts/embedding.md)。

### S6-c2｜向量檢索可能漏掉精確比對，例如錯誤代碼「TS-999」；BM25 能補上
- 證據：While embedding models excel at capturing semantic relationships, they can miss crucial exact matches.
- 證據：An embedding model might find content about error codes in general, but could miss the exact "TS-999" match. BM25 looks for this specific text string to identify the relevant documentation.
- 說明：白話說明：跟 [S2-c5](s2-karpukhin-2020-dpr.md#s2-c5) 的結論一致。見 [關鍵字檢索 BM25](../concepts/bm25.md)、[混合檢索與重排](../concepts/hybrid-search.md)。

### S6-c3｜切塊會丟掉上下文：「營收成長 3%」這一塊本身沒寫是哪家公司、哪一季
- 證據：A relevant chunk might contain the text: "The company's revenue grew by 3% over the previous quarter." However, this chunk on its own doesn't specify which company it's referring to or the relevant time period
- 說明：白話說明：一段話被切出來之後，原本靠前文才看得懂的「這家公司」就失去指涉對象，檢索時也就對不上問題。

### S6-c4｜情境化檢索：在每塊前面補一段 50 到 100 token 的說明，再建向量與 BM25 索引
- 證據：To implement Contextual Retrieval, we turn to Claude.
- 證據：The resulting contextual text, usually 50-100 tokens, is prepended to the chunk before embedding it and before creating the BM25 index.
- 證據：This chunk is from an SEC filing on ACME corp's performance in Q2 2023
- 說明：白話說明：說明文字由 LLM 讀整份文件後自動寫，例如「這段出自 ACME 公司 2023 年第二季的財報」。

### S6-c5｜效果：找不到資料的比例下降 35%、49%，加上重排後下降 67%
- 證據：Contextual Embeddings reduced the top-20-chunk retrieval failure rate by 35% (5.7% → 3.7%).
- 證據：Combining Contextual Embeddings and Contextual BM25 reduced the top-20-chunk retrieval failure rate by 49% (5.7% → 2.9%).
- 證據：Reranked Contextual Embedding and Contextual BM25 reduced the top-20-chunk retrieval failure rate by 67% (5.7% → 1.9%).
- 說明：白話說明：「失敗率」是相關資料沒有出現在前 20 塊的比例。原本是 5.7%，三種做法依序降到 3.7%、2.9%、1.9%。這是 Anthropic 在自家測試資料上的結果。

### S6-c6｜重排：先粗找一大批（文中 150 塊），再用重排模型逐塊打分，只留最好的（文中 20 塊）
- 證據：Perform initial retrieval to get the top potentially relevant chunks (we used the top 150);
- 證據：Using a reranking model, give each chunk a score based on its relevance and importance to the prompt, then select the top-K chunks (we used the top 20);
- 說明：白話說明：見 [混合檢索與重排](../concepts/hybrid-search.md)。

### S6-c7｜知識庫不到 20 萬 token（約 500 頁）時，可以整份放進提示詞，不一定需要 RAG
- 證據：If your knowledge base is smaller than 200,000 tokens (about 500 pages of material), you can just include the entire knowledge base in the prompt that you give the model, with no need for RAG or similar methods.
- 說明：白話說明：RAG 是為了「資料太多、放不進去」而存在。資料少的時候，最簡單的做法就是全部給模型看。這個門檻取決於模型能讀多長，文中指的是 Claude 當時的上限。

### S6-c8｜混合檢索：BM25 與向量檢索各找一批，再合併、去掉重複
- 證據：Combine and deduplicate results from (3) and (4) using rank fusion techniques;
- 證據：By leveraging both BM25 and embedding models, traditional RAG systems can provide more comprehensive and accurate results
- 說明：白話說明：(3) 是用 BM25 找字面相符的塊，(4) 是用向量找意思相近的塊。兩份名單合併、去掉重複後，取前幾名放進提示詞。見 [混合檢索與重排](../concepts/hybrid-search.md)。

## S7｜Karpathy 2026：LLM Wiki

### S7-c1｜一般 RAG 每次提問都從頭找資料，知識沒有累積
- 證據：the LLM is rediscovering knowledge from scratch on every question. There's no accumulation.
- 說明：白話說明：見 [LLM Wiki 與 RAG 的差別](../concepts/llm-wiki-vs-rag.md)。

### S7-c2｜LLM Wiki 讓 LLM 逐步建立並維護一個持續存在的 Wiki
- 證據：the LLM **incrementally builds and maintains a persistent wiki**
- 說明：白話說明：新增一篇資料時，LLM 不只是存起來等人查，而是讀完、整理、更新相關頁面，並標出新舊資料的矛盾。

### S7-c3｜三層結構：原始資料（不修改）、Wiki（LLM 寫）、規則檔（規定格式與流程）
- 證據：There are three layers:
- 證據：These are immutable — the LLM reads from them but never modifies them.
- 說明：白話說明：本專案的對應是 `raw/`、`wiki/` 與 `AGENTS.md`。

### S7-c4｜三種操作：Ingest（加入資料）、Query（提問）、Lint（健康檢查）
- 證據：Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search.
- 說明：白話說明：上面這段是 Lint 要找的問題清單。本專案的 `pipeline/lint_wiki.py` 實作了其中可以用程式判斷的部分（孤兒頁、壞連結、缺頁），並加上「證據必須逐字出自原文」的檢查。

### S7-c5｜好的查詢結果可以存回 Wiki，簡報也是查詢結果的一種
- 證據：**good answers can be filed back into the wiki as new pages.**
- 證據：Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (Marp), a chart (matplotlib), a canvas.
- 說明：白話說明：本專案的簡報大綱存在 [查詢紀錄：教學簡報大綱](../queries/deck-outline.md)。

