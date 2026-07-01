## V7.6 - Embedding-based Semantic RAG Upgrade

V7.6 是 FleetMind V7 中非常重要的一次升级。这个版本把原来的 keyword-based RAG 进一步升级为 embedding-based semantic RAG，并且成功接入 LLM API，让系统从“规则型问答工具”进化成更接近真实 AI 应用的 logistics RAG assistant。

这次升级的目标不是单纯调用大模型，而是学习一个真实 AI 系统背后的完整流程：

```text
用户问题
↓
Embedding-based semantic search
↓
检索 knowledge_base 证据
↓
SQLite 数据库查询真实运营数据
↓
构建带防幻觉规则的 prompt
↓
调用 LLM 生成管理建议
↓
如果 LLM 不可用，使用 rule-based fallback
````

---

### 1. Embedding-based Semantic Search

在 V6 和 V7 前期版本中，系统主要依赖 keyword matching。也就是说，用户问题和知识库片段必须有相同或相近的关键词，系统才能匹配到相关内容。

例如：

```text
delay
delayed
late
serious delay
route delay
```

这些表达意思接近，但 keyword search 不一定都能稳定匹配。

V7.6 引入了 `sentence-transformers`，使用：

```python
SentenceTransformer("all-MiniLM-L6-v2")
```

把用户问题和知识库文本都转换成 embedding 向量。

这个模型会把一句话转换成一个 384 维向量：

```text
Sentence
↓
Embedding Model
↓
384-dimensional vector
```

系统再用 cosine similarity 比较两个向量的语义相似度。

例如：

```text
"Route B has serious delay problems."
```

和：

```text
"Which route often arrives late?"
```

虽然关键词不完全一样，但 embedding 可以判断它们语义相关。

这让我理解到：

```text
keyword search 看的是“词是否一样”
semantic search 看的是“意思是否接近”
```

---

### 2. New Semantic Retriever Module

V7.6 新增了：

```text
semantic_retriever.py
```

这个模块负责：

```text
1. 读取 knowledge_base 里的 txt 文件
2. 按空行切分知识片段
3. 用 SentenceTransformer 生成 embeddings
4. 用 cosine similarity 计算用户问题和知识片段的相似度
5. 返回 top_k 个最相关 evidence
```

核心流程：

```text
Question
↓
query embedding
↓
document embeddings
↓
cosine similarity
↓
top-k evidence
```

这样 `rag_engine.py` 不再依赖旧的 keyword retriever，而是调用：

```python
semantic_search(question, top_k=top_k)
```

这一步让 RAG 的 retrieval quality 明显提升。

---

### 3. LLM-powered RAG Integration

V7.6 还接入了 LLM API。

新增或增强的模块包括：

```text
prompt_builder.py      # 构建 LLM prompt
llm_client.py          # 调用 OpenAI API
rag_engine.py          # 统一调度 semantic search、database retrieval 和 LLM answer
```

新的 RAG 主流程是：

```text
User Question
↓
semantic_retriever.py
检索 knowledge_base evidence
↓
database_retriever.py
查询 SQLite database context
↓
prompt_builder.py
构建带规则的 prompt
↓
llm_client.py
调用 LLM
↓
answer_generator.py
作为 fallback
```

这个版本保留了 rule-based fallback：

```text
如果没有 API key
如果 LLM 调用失败
如果网络或配置有问题
```

系统仍然可以返回基本管理建议，而不是直接崩溃。

---

### 4. Hallucination Control

V7.6 的一个重点是 hallucination control。

在 prompt 中，我加入了明确规则：

```text
不要编造 truck ID
不要编造 trip ID
不要编造 route name
不要编造 driver
不要编造 revenue / cost / profit / delay
如果数据库没有记录，要明确说明 no records were retrieved
数据库事实优先于知识库解释
```

这让系统在回答时更加可靠。

例如用户问：

```text
which routes have serious delay problems
```

如果数据库没有返回记录，LLM 不能自己编路线。
如果数据库返回了 route summary，LLM 才能基于真实 `Average Delay Hours` 判断严重路线。

这让我理解到：真实 AI 应用不能只追求“回答流畅”，更重要的是回答必须被 evidence 和 database context 支撑。

---

### 5. Database Retrieval Enhancement

在测试中发现一个问题：

```text
which routes have serious delay problems
```

一开始没有返回数据库记录。

原因是 `database_retriever.py` 原本能识别：

```text
high delay trips
```

但不能很好识别：

```text
route + delay
```

所以 V7.6 增强了 intent detection：

```text
is_route_question
is_delay_question
is_route_delay_question
```

这样系统现在可以识别路线层面的延误问题，并返回：

```text
Database Result - Route Performance Summary
```

其中包括：

```text
Route
Total Trips
Total Distance
Total Revenue
Total Cost
Total Profit
Average Profit Margin
Average Cost Per Km
Average Delay Hours
```

同时，`database.py` 中的 route performance query 也从按 cost 排序，优化为按 delay 排序：

```sql
ORDER BY average_delay_hours DESC
```

这样当用户问 delay routes 时，系统会优先返回延误最严重的路线。

---

## Difficulties and Solutions in V7.6

### Challenge 1: Python and package compatibility

一开始尝试安装 `sentence-transformers` 和 PyTorch 时，遇到了 Python 版本和依赖兼容问题。

特别是：

```text
numpy
scipy
scikit-learn
torch
sentence-transformers
```

之间有版本依赖。

解决方式：

最终使用一套稳定组合：

```text
Python 3.12.6
sentence-transformers==3.0.1
torch==2.2.2
numpy==1.26.4
scipy==1.13.1
scikit-learn==1.5.2
```

并用：

```bash
pip check
```

确认环境没有 broken requirements。

---

### Challenge 2: Understanding embeddings and tensors

刚开始不理解为什么 embedding shape 是：

```text
(3, 384)
```

后来理解到：

```text
3 = 输入了 3 个句子
384 = all-MiniLM-L6-v2 输出的向量维度
```

也学习到 PyTorch tensor 是深度学习中保存数值数据的格式。

例如：

```text
tensor([[0.5614]])
```

表示两个句子的语义相似度。

---

### Challenge 3: Semantic search indexing bug

在 `semantic_retriever.py` 中，曾经错误写成：

```python
document_embeddings[0]
```

这会导致系统只拿第一个文档向量做相似度计算，后面 `topk` 取多个结果时出现：

```text
RuntimeError: selected index k out of range
```

解决方式：

改成：

```python
similarities = util.cos_sim(query_embedding, document_embeddings)[0]
```

这样系统会比较用户问题和所有知识片段，而不是只比较第一个。

---

### Challenge 4: Missing LLM dependencies

运行 `rag_engine.py` 时，遇到：

```text
No module named 'dotenv'
No module named 'openai'
```

解决方式：

安装并加入 `requirements.txt`：

```text
python-dotenv
openai
```

这让我理解到：

```text
python-dotenv 负责读取 .env
openai 负责调用 LLM API
.env 用来安全保存 API key
```

---

### Challenge 5: Route delay question could not retrieve database context

系统一开始能回答：

```text
what should we do with high delay trips
```

但不能很好回答：

```text
which routes have serious delay problems
```

原因是数据库检索器没有识别 route-level delay intent。

解决方式：

增强 `database_retriever.py` 的问题判断逻辑，并让 route performance summary 支持 delay 类问题。

最终系统可以基于真实数据库返回：

```text
Chongqing to Berlin: 30.00 average delay hours
Chongqing to Davis: 25.00 average delay hours
Chongqing to Shenzhen: 8.00 average delay hours
```

---

## Updated V7.6 Architecture

当前 V7.6 的整体框架：

```text
app.py
Flask web routes
↓
rag_engine.py
RAG 主流程控制
↓
semantic_retriever.py
Embedding-based knowledge base retrieval
↓
database_retriever.py
SQLite database context retrieval
↓
prompt_builder.py
Prompt construction + hallucination control rules
↓
llm_client.py
LLM API call
↓
answer_generator.py
Rule-based fallback
↓
templates/rag.html
展示 answer、sources、database context、retrieved evidence
```

核心文件：

```text
semantic_retriever.py      # 语义检索
embedding_test.py          # embedding 学习测试文件
rag_engine.py              # RAG 总调度
database_retriever.py      # 数据库检索
database.py                # SQL 查询函数
prompt_builder.py          # prompt 构建
llm_client.py              # LLM API 调用
answer_generator.py        # fallback 回答生成
knowledge_base/            # 本地知识库
fleetmind.db               # SQLite 数据库
```

---

## What I Learned in V7.6

通过 V7.6，我学习了：

```text
SentenceTransformer 如何生成 embeddings
384-dimensional sentence embedding 的含义
cosine similarity 如何衡量语义相似度
PyTorch tensor 的基本概念
semantic search 和 keyword search 的区别
如何把 semantic retriever 接入 RAG pipeline
如何用 SQLite database context 增强 LLM 回答
如何构建带 hallucination control 的 prompt
如何使用 .env 管理 API key
如何保留 rule-based fallback 提高系统稳定性
如何处理 Python AI package dependency conflicts
```

这次升级让我更清楚地理解了：
一个真实的 AI assistant 不只是调用大模型，而是由检索、数据库、prompt、模型调用、fallback 和证据控制共同组成的系统。

---

## V7.6 Project Value

V7.6 让 FleetMind 从普通 Flask + SQLite 项目，升级成了一个更完整的 AI application prototype。

它现在具备：

```text
Embedding-based semantic retrieval
Database-augmented RAG
LLM-powered answer generation
Hallucination control
Rule-based fallback
Logistics domain knowledge base
SQLite operational analytics
Route-level and trip-level business reasoning
```
