````markdown
# FleetMind Web V7 - Database-Augmented Logistics RAG Assistant

FleetMind Web V7 是我在 FleetMind V1-V6 基础上继续升级的物流数据分析与 RAG 问答系统。

这个版本的目标不是简单做一个网页问答工具，而是学习一个真实 AI 应用系统应该如何组织：

- knowledge base 检索
- SQLite 数据库查询
- RAG pipeline
- evidence 展示
- 数据库上下文组织
- prompt engineering 前置准备
- hallucination control 思路

FleetMind V7 目前仍然是本地 lightweight RAG，不依赖外部 LLM API。后续版本会继续接入 LLM，让系统从 rule-based answer generator 升级成 LLM-powered logistics assistant。

---

## Project Background

FleetMind 最早来自我的 COMP9001 final project。最开始它只是一个 Python terminal program，用来分析单辆卡车的收入、成本、利润率和风险等级。

随着版本升级，FleetMind 逐渐从一个小型 Python 项目，扩展成一个 Flask + SQLite + analytics + RAG 的物流管理系统。

我希望这个项目能结合我的物流行业背景和计算机学习路径，模拟一个真实企业可能会使用的车队运营分析平台。

---

## Version History

### V1 - Terminal Fleet Analysis

最初版本是一个 terminal-based Python program。

主要功能：

- 输入 truck revenue 和 cost
- 计算 total cost
- 计算 profit
- 计算 profit margin
- 判断 risk level
- 使用 OOP `Truck` class 封装分析逻辑

这个阶段主要练习了 Python 基础、函数、类和简单业务规则。

---

### V2 - Flask Web Version

V2 把 terminal program 升级成 Flask web app。

新增内容：

- Flask routes
- HTML templates
- 表单输入
- 样本车辆展示
- 单车分析页面
- 历史记录保存

这个阶段让我第一次理解了 web app 的基本结构：

```text
app.py
templates/
static/
business logic
````

---

### V3 - Dashboard Version

V3 加入 dashboard 页面，把多辆车的数据做汇总分析。

新增内容：

* truck count
* total revenue
* total cost
* total profit
* average margin
* high risk count
* best/worst truck
* matplotlib charts

这个阶段开始从单条记录分析，转向整体运营数据分析。

---

### V4 - Visualization and UI Improvement

V4 主要增强可视化和页面展示。

新增内容：

* revenue/cost/profit/risk charts
* dashboard table styling
* profit/loss color highlighting
* compare page sorting
* risk warning display

这个阶段让我意识到，数据分析项目不仅要算得对，也要让用户看得懂。

---

### V5 - SQLite Database Version

V5 是一次重要升级：从 CSV/file-based storage 升级到 SQLite database。

新增内容：

* `fleetmind.db`
* `trucks` table
* `trips` table
* `routes` analysis
* trip-level records
* CRUD operations
* analytics page
* insights page
* route analytics
* high delay detection
* loss-making truck detection

这个阶段让我开始真正接触 database-driven web app。

我学习到：

* SQLite connection
* SQL SELECT
* WHERE filtering
* ORDER BY sorting
* GROUP BY aggregation
* Flask + database integration
* structured data storage

---

### V6 - Local RAG Experiment

V6 第一次加入 RAG assistant。

新增内容：

* `knowledge_base/`
* route notes
* fleet policy
* risk rules
* cost notes
* keyword-based document retrieval
* source display
* simple answer generation

这个阶段的 RAG 还是比较简单，主要是：

```text
用户问题
↓
关键词匹配 knowledge_base
↓
返回相关文本
↓
生成简单管理建议
```

虽然还不是 LLM-powered RAG，但它让我理解了 RAG 的基本思想：

```text
retrieval first, answer second
```

---

## V7 - Modular Database-Augmented RAG Assistant

V7 是目前最重要的一次升级。

V7 的核心目标是把原来比较集中的 RAG 代码拆成更专业的模块，并让 RAG 同时利用：

```text
knowledge_base evidence
SQLite database context
```

也就是说，V7 不只是从文档里找答案，还能从真实数据库里查运营数据。

---

## V7 Current Architecture

当前 V7 的核心文件结构：

```text
document_retriever.py      # knowledge_base 检索
database_retriever.py      # SQLite 数据库检索
answer_generator.py        # rule-based 管理建议生成
rag_engine.py              # RAG 主流程控制
app.py                     # Flask web routes
templates/rag.html         # RAG assistant 页面
knowledge_base/            # 本地知识库
fleetmind.db               # SQLite 数据库
```

RAG pipeline：

```text
User Question
↓
document_retriever.py
检索 knowledge_base
↓
database_retriever.py
检索 SQLite database
↓
rag_engine.py
整合 document evidence 和 database context
↓
answer_generator.py
生成管理建议
↓
rag.html
展示 answer、sources、retrieved evidence
```

---

## V7.1 - RAG Modular Refactor

V7.1 的目标是把 V6 中比较集中的 `rag_engine.py` 拆成多个模块。

完成内容：

* 新建 `document_retriever.py`
* 新建 `database_retriever.py`
* 新建 `answer_generator.py`
* 清理 `rag_engine.py`
* 让 `rag_engine.py` 只负责主流程调度

重构后：

```text
document_retriever.py
负责 knowledge_base 读取、切分、检索

database_retriever.py
负责 SQLite 数据库查询

answer_generator.py
负责生成回答

rag_engine.py
负责调用各模块并返回结果
```

学习到的新知识：

* modular programming
* separation of concerns
* RAG pipeline structure
* backend responsibility splitting

遇到的挑战：

一开始 `rag_engine.py` 里什么都放在一起，包括文档读取、chunk 切分、关键词搜索、数据库查询和回答生成。代码能跑，但是结构不清晰，后续很难接 LLM。

解决方式：

把不同职责拆成独立文件，让每个模块只做一件事。

---

## V7.2 - Retrieval Quality Improvement

V7.2 的目标是提升 knowledge_base 检索质量。

原来的检索方式比较简单：

```text
用户问题关键词
↓
chunk 文本匹配
↓
匹配一个词加一分
```

问题是：

* `trips` 和 `trip` 不一定能匹配好
* `delayed` 和 `delay` 不一定能匹配好
* `expensive` 和 `cost` 没有直接关系
* `unprofitable` 和 `loss` 没有直接关系

因此 V7.2 增加了轻量级语义增强。

完成内容：

### 1. Keyword Normalization

把不同形式的词统一。

例子：

```text
trips → trip
trucks → truck
routes → route
delayed → delay
```

### 2. Stop Words Filtering

过滤无意义常见词。

例如：

```text
what, which, is, the, should, with, about
```

这样系统更关注真正重要的业务词：

```text
delay
risk
fuel
cost
profit
route
truck
trip
```

### 3. Synonym Expansion

加入简单同义词扩展。

例子：

```text
late → delay
expensive → cost / fuel / maintenance
unprofitable → loss / profit / negative
dangerous → risk
```

### 4. Business Keyword Weighting

业务关键词权重更高。

例如：

```text
delay
risk
fuel
cost
profit
loss
route
truck
trip
```

这些词比普通词更重要，所以匹配到时加更高分数。

### 5. Phrase Matching

加入短语匹配。

例如：

```text
high delay
delay risk
high risk
fuel cost
cost per kilometre
profit margin
negative profit
```

如果用户问题和 knowledge_base chunk 同时出现完整短语，就额外加分。

### 6. Evidence Tracking

每条检索结果现在会显示：

```text
Source
Score
Matched Keywords
Matched Phrases
Content
```

这让系统不只是给答案，还能解释：

```text
为什么这条 evidence 被检索出来？
```

学习到的新知识：

* keyword normalization
* stop words
* synonym expansion
* scoring mechanism
* phrase matching
* evidence tracking
* retrieval transparency

遇到的挑战：

一开始检索结果虽然能出来，但分数经常都是 1，排序不明显。用户问 `Which routes have high delay risk?` 时，系统不能很好地区分最相关的 chunk。

解决方式：

加入业务关键词权重和短语匹配，让更相关的 evidence 排在前面。

---

## V7.3 - Database Retrieval Expansion

V7.3 的目标是让 RAG 不只会查文档，还能根据用户问题查询 SQLite 数据库。

### V7.3.1 High Delay Trips

支持问题：

```text
Which trips have high delay?
Which trucks are late?
What should managers do with delayed trips?
```

数据库逻辑：

```sql
WHERE delay_hours >= 24
ORDER BY delay_hours DESC
```

系统能返回高延误运输任务。

---

### V7.3.2 Loss-Making Trips

支持问题：

```text
Which trips are unprofitable?
Which trips are losing money?
Which trips have negative profit?
Which trips are loss-making?
```

数据库逻辑：

```sql
WHERE profit < 0
ORDER BY profit ASC
```

系统能查出亏损运输任务。

例如：

```text
Route: Chongqing to Shenzhen
Profit: -4,999.98
Risk Level: High Risk
```

---

### V7.3.3 High Cost Per Km Trips

支持问题：

```text
Which trips have high cost per km?
Which trips are costly?
Which routes are expensive?
```

数据库逻辑：

```sql
ORDER BY cost_per_km DESC
LIMIT 5
```

系统能找出每公里成本最高的运输任务。

---

### V7.3.4 Route Performance Summary

支持 route-level 汇总分析。

支持问题：

```text
Which routes are expensive?
Which routes have high average delay?
Route performance summary
Which routes have low profit margin?
```

数据库逻辑：

```sql
GROUP BY route
```

统计内容：

```text
Total Trips
Total Distance
Total Revenue
Total Cost
Total Profit
Average Profit Margin
Average Cost Per Km
Average Delay Hours
```

这一步让系统从 trip-level analysis 升级到 route-level analysis。

---

### V7.3.5 Intent Priority

一开始系统有一个问题：

用户问：

```text
Which routes are expensive?
```

可能同时触发：

```text
High Cost Per Km Trips
Route Performance Summary
```

所以 V7.3.5 加入了 intent priority。

规则：

```text
truck / trucks → truck-level 查询
trip / trips → trip-level 查询
route / routes → route-level 查询
```

这样：

```text
Which routes are expensive?
→ Route Performance Summary

Which trips have high cost per km?
→ High Cost Per Km Trips

What should managers do with high risk trucks?
→ High Risk Trucks
```

用到的知识：

* SQL filtering
* SQL sorting
* SQL aggregation
* GROUP BY
* COUNT()
* SUM()
* AVG()
* intent detection
* database context generation
* database-augmented RAG

遇到的挑战：

同一个词可能有不同含义。例如 `expensive` 既可能指单个 trip 成本高，也可能指某条 route 整体成本高。

解决方式：

加入 intent priority，根据用户问题中的 `route / trip / truck` 判断查询对象。

---

## Current Features

当前 V7 支持：

### Knowledge Base Retrieval

* route notes retrieval
* cost notes retrieval
* fleet policy retrieval
* risk rules retrieval
* keyword normalization
* synonym expansion
* business keyword scoring
* phrase matching
* retrieved evidence display

### Database Retrieval

* high risk trucks
* high delay trips
* loss-making trips
* high cost per km trips
* route performance summary
* formatted database context
* intent priority

### Web Display

`/rag` 页面支持显示：

* user question
* generated answer
* database findings
* knowledge base findings
* sources
* retrieved evidence
* relevance score
* matched keywords
* matched phrases

---

## Example Questions

```text
What should managers do with high risk trucks?
```

```text
Which trips have high delay?
```

```text
Which trips are unprofitable?
```

```text
Which trips have high cost per km?
```

```text
Which routes are expensive?
```

```text
What should we check if fuel cost is high?
```

```text
Why is cost per kilometre important?
```

---

## Tech Stack

```text
Python
Flask
SQLite
HTML
CSS
Jinja2
SQL
Local RAG
Rule-based retrieval
Rule-based answer generation
```

---

## Key Learning Outcomes

通过 V7，我学习了：

```text
如何把一个 AI assistant 拆成多个后端模块
如何设计 RAG pipeline
如何做本地 knowledge base retrieval
如何用 SQLite 查询真实业务数据
如何把 database context 加入 RAG
如何显示 retrieved evidence
如何设计 scoring mechanism
如何做 intent detection
如何为后续 LLM prompt engineering 做准备
```

这次升级让我理解到，真实 AI 应用不只是调用 API，而是要先解决：

```text
数据从哪里来
检索是否准确
证据是否可靠
数据库查询是否正确
回答是否基于上下文
用户能不能看到来源
系统是否能避免乱编
```

---

## Challenges and Solutions

### Challenge 1: RAG code was too concentrated

早期 RAG 代码集中在 `rag_engine.py` 里，功能混杂。

Solution:

拆分成：

```text
document_retriever.py
database_retriever.py
answer_generator.py
rag_engine.py
```

---

### Challenge 2: Keyword matching was too simple

原来的检索只会简单匹配关键词。

Solution:

加入：

```text
normalization
stop words
synonym expansion
business keyword weighting
phrase matching
```

---

### Challenge 3: Retrieval results were hard to explain

一开始系统只返回答案和 sources，但看不出为什么这些内容被选中。

Solution:

加入：

```text
matched_keywords
matched_phrases
score
retrieved evidence display
```

---

### Challenge 4: Database retrieval only supported one query type

最开始只支持 high risk trucks。

Solution:

扩展到：

```text
high delay trips
loss-making trips
high cost per km trips
route performance summary
```

---

### Challenge 5: Multiple intents could be triggered at the same time

例如：

```text
Which routes are expensive?
```

可能同时触发 trip-level 和 route-level 查询。

Solution:

加入 intent priority：

```text
truck → truck-level
trip → trip-level
route → route-level
```

---

## Current Project Level

FleetMind V7 目前已经不只是一个普通 Flask CRUD 项目。

它包含：

```text
Web development
Database analytics
Business rule design
Local RAG pipeline
Evidence tracking
Intent detection
Logistics domain modeling
```

这个项目可以作为一个 AI application / data analytics / backend learning project 写进简历，尤其适合展示：

```text
AI + logistics
RAG system design
database-augmented assistant
business-oriented analytics
```

---

## Future Improvements

接下来计划进入 V7.4 和 V7.5。

### V7.4 Prompt Builder

新增：

```text
prompt_builder.py
```

目标是把以下内容组织成 LLM prompt：

```text
user question
knowledge base evidence
database context
answer rules
hallucination control rules
```

---

### V7.5 LLM API Integration

后续会接入 LLM API，让系统从 rule-based answer generator 升级为：

```text
LLM-powered logistics RAG assistant
```

但仍然保留 fallback：

```text
如果 LLM API 不可用，仍然使用 rule-based answer
```

---

### V7.6 UI and README Polish

后续优化：

```text
example questions
better evidence cards
database context display
screenshots
English README
project architecture diagram
```

---

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Initialize database if needed:

```bash
python3 init_db.py
```

Run Flask app:

```bash
python3 app.py
```

Open in browser:

```text
http://127.0.0.1:5001
```

RAG assistant page:

```text
http://127.0.0.1:5001/rag
```

---

## Project Reflection

FleetMind V7 是我从 Python beginner project 逐步升级出来的项目。

它不是一开始就设计得很完整，而是在每个版本里逐步发现问题、修复问题、学习新知识。

从 V1 的单车利润计算，到 V5 的 SQLite 数据库，再到 V7 的 database-augmented RAG，我逐渐理解了一个真实 AI 应用不仅需要模型，还需要：

```text
清晰的数据结构
可靠的数据库查询
合理的检索逻辑
可解释的 evidence
稳定的后端模块
面向业务的回答方式
```

这个过程让我对 AI application engineering 有了更具体的理解，也让我看到自己可以把物流行业经验和计算机技术结合起来，做出更接近真实业务场景的系统。

````

