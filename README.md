# FleetMind Web V6

FleetMind Web V6 是一个基于 Flask 的物流车队运营分析与 RAG 问答助手项目。

这个项目是从我之前的 FleetMind V1 到 V5 一步一步升级来的。最开始它只是一个 Python 终端程序，用来分析单辆货车的收入、成本、利润和风险。后来我把它升级成 Flask 网页应用，再加入 dashboard、SQLite 数据库、trip records、route analytics。到了 V6，我开始尝试把 RAG（Retrieval-Augmented Generation，检索增强生成）接入项目，让系统不只是展示数据，还能根据知识库和数据库内容回答一些简单的物流管理问题。

项目灵感来自我之前接触过的物流运输场景，但项目里的数据都经过匿名化和修改，不包含真实公司、司机、车牌、客户或敏感路线信息。

---

## 1. Project Overview 项目简介

FleetMind Web V6 的目标是探索一个物流分析系统如何从传统 dashboard 升级为一个简单的 AI-assisted decision support tool。

在 V6 中，系统不仅可以分析车辆和运输任务数据，还可以通过本地知识库和 SQLite 数据库回答运营相关问题。

目前系统可以完成：

* 车辆收入、成本、利润、利润率分析
* 风险等级判断，例如 Excellent、Normal、Warning、High Risk
* SQLite 数据库存储 trucks、trips、routes 相关数据
* Dashboard 数据汇总
* Analytics 图表展示
* Trip records 增删改查
* Route analytics 路线层面分析
* Rule-based operational insights
* 本地 knowledge base 文档检索
* RAG Assistant 网页问答
* 结合知识库结果和数据库结果生成管理建议

---

## 2. Tech Stack 技术栈

这个项目主要使用：

* Python
* Flask
* SQLite
* HTML
* CSS
* Jinja2
* Matplotlib
* Local text-based RAG
* Keyword-based retrieval
* Rule-based decision support

V6 暂时没有接入 OpenAI API 或其他大模型 API。现在的 RAG 是一个本地实验版本，主要目的是帮助我理解 RAG 的基本结构，包括知识库、检索、上下文组织、数据库检索和回答生成。

---

## 3. Main Features 主要功能

### 3.1 Fleet Dashboard

Dashboard 页面可以展示车队整体运营情况，包括：

* Truck count
* Total revenue
* Total cost
* Total profit
* Average profit margin
* High risk trucks count
* Best truck
* Worst truck
* Most common cost pressure

这个页面主要用来快速了解整个车队的经营表现。

---

### 3.2 Fleet Analytics

Analytics 页面会基于 SQLite 数据库生成图表和汇总信息，包括：

* Revenue by truck
* Profit by truck
* Risk level distribution
* Cost pressure distribution
* Loss-making trucks

这个功能从之前的 CSV 版本升级而来。V6 里主要数据来源已经变成 SQLite 数据库，因此数据更加结构化，也更方便后续继续扩展。

---

### 3.3 Truck Records

Truck records 页面可以查看保存到数据库里的车辆数据。

每辆车包含：

* Truck ID
* Driver
* Route
* Revenue
* Fuel cost
* Toll cost
* Repair cost
* Salary cost
* Insurance cost
* Other cost
* Total cost
* Profit
* Profit margin
* Risk level
* Main cost pressure

系统会根据输入的收入和成本自动计算利润、利润率、风险等级和主要成本压力。

---

### 3.4 Trip Records

V5 开始我加入了 trip-level records，V6 中继续保留并完善。

每条 trip record 包括：

* Trip ID
* Truck ID
* Driver
* Route
* Distance
* Revenue
* Total cost
* Profit
* Profit margin
* Cost per km
* Delay hours
* Risk level
* Trip date

这个设计让项目不再只是分析“单辆车”，而是可以分析具体运输任务。

---

### 3.5 Route Analytics

Route analytics 页面会基于 trips 表，按照路线进行分组分析。

系统可以计算每条路线的：

* Total trips
* Total revenue
* Total cost
* Total profit
* Average profit margin
* Average delay hours
* Average cost per km
* Route risk level

这个功能让项目更接近真实物流管理，因为公司在实际运营中经常需要判断哪条路线利润高、哪条路线延误严重、哪条路线成本压力最大。

---

### 3.6 Operational Insights

Insights 页面会根据数据库记录生成 rule-based 建议。

例如：

* 如果车辆亏损，提示检查定价、路线规划和运营成本
* 如果车辆是 High Risk，提示管理层优先 review
* 如果 profit margin 很低，提示需要成本控制或路线调整
* 如果某类成本压力最常见，提示公司优先关注该成本项
* 如果某条路线延误最高，提示需要检查路线安排和调度计划

这部分不是机器学习模型，而是基于规则的 decision support system。

---

## 4. V6 RAG Assistant

V6 最大的升级是加入了一个简单的 RAG Assistant。

RAG 的全称是 Retrieval-Augmented Generation，中文可以理解为“检索增强生成”。

在这个项目里，我实现的是一个本地简化版 RAG。它不会调用大模型 API，而是通过读取本地 txt 文档、关键词检索、数据库查询和规则化回答生成，来模拟一个物流管理问答助手。

---

## 5. V6 Development Progress 开发过程

### V6.1 Knowledge Base

第一步是建立 `knowledge_base/` 文件夹。

里面放了一些和物流运营相关的 txt 文件，例如：

* `fleet_policy.txt`
* `risk_rules.txt`
* `route_notes.txt`
* `cost_notes.txt`

这些文件用来模拟公司的内部知识库，包括路线说明、风险规则、成本说明和管理政策。

我在这一步主要学习了 knowledge base 的概念。以前项目里的数据主要是结构化数据，例如 SQLite 表格；而 knowledge base 更像是非结构化文本资料，用自然语言记录规则和经验。

---

### V6.2 Simple Retrieval

第二步是写 `rag_engine.py`。

这一版实现了几个基础功能：

* 读取 `knowledge_base/` 里的 txt 文件
* 把文档内容按照空行切成 chunks
* 把用户问题拆成关键词
* 去掉一些无意义的停用词
* 对问题和 chunk 进行简单匹配
* 根据 score 排序
* 返回最相关的知识片段和 sources

这一阶段我主要理解了 retrieval 的基本流程：

```text
用户问题
→ 拆分关键词
→ 搜索知识库 chunks
→ 计算匹配分数
→ 返回相关内容
```

虽然这个检索方式还比较简单，不是 embedding-based search，但它帮助我理解了 RAG 里 retrieval 的核心思想。

---

### V6.3 RAG Assistant Page

第三步是把 RAG assistant 接入 Flask 页面。

我新增了 `/rag` 页面，用户可以在网页输入问题。Flask 接收到问题后，会调用：

```python
ask_rag(question)
```

然后 `rag_engine.py` 会检索知识库，并把回答和 sources 返回给网页。

这一步完成后，用户可以在网页上问：

```text
what should we do with high delay trips
```

页面会返回相关知识库内容，并显示来源文件。

这一阶段我主要学习了 Flask 表单和 RAG 函数之间的连接方式：

```text
HTML form
→ Flask request.form
→ ask_rag(question)
→ return answer and sources
→ render_template 显示结果
```

---

### V6.4 Database Retrieval

第四步是让 RAG assistant 不只检索 txt 文件，还能查询 SQLite 数据库。

我在 `database.py` 里新增了：

```python
get_high_risk_trucks_from_db()
```

这个函数可以从 `trucks` 表里查出 `risk_level = High Risk` 的车辆。

然后在 `rag_engine.py` 里新增了：

```python
get_database_context(question)
```

这个函数会判断用户问题是否和 high risk trucks 有关。如果问题里包含 `high risk` 和 `truck`，系统就会查询 SQLite 数据库，并把高风险车辆整理成文字结果。

例如用户问：

```text
which trucks are high risk
```

系统可以返回：

```text
Database Result - High Risk Trucks

Truck ID: Truck 017
Driver: Dong dong
Route: Chongqing to Singapore
Revenue: 120000.0
Total Cost: 128200.0
Profit: -8200.0
Profit Margin: -6.83%
Risk Level: High Risk
Main Cost Pressure: Fuel Cost
```

这一阶段让我理解了 structured data 和 unstructured data 的区别：

* `knowledge_base/*.txt` 是非结构化文本
* `fleetmind.db` 是结构化数据库
* RAG assistant 可以同时使用这两类信息作为回答上下文

---

### V6.5 Better Answer Logic

第五步是优化回答结构。

在 V6.4 中，系统只是把知识库结果和数据库结果简单拼接在一起。功能可以用，但回答看起来还不够像管理建议。

所以 V6.5 中我新增了：

```python
generate_management_answer(question, doc_results, db_results)
```

这个函数会把回答整理成更清楚的结构：

```text
Question

Management Answer

Database Findings

Knowledge Base Findings

Suggested Action
```

这样系统不只是把资料列出来，而是更像一个基础的 decision support assistant。

例如用户问：

```text
what should managers do with high risk trucks
```

系统会先展示数据库中的高风险车辆，再展示知识库中相关的风险规则，最后给出 suggested action，例如优先 review 高风险车辆、检查利润率、主要成本压力、路线表现，以及是否需要调整路线、控制成本或安排维修检查。

这一阶段的重点是从 retrieval system 升级到 management recommendation system。

---

## 6. Challenges and Solutions 遇到的问题与解决方法

### 6.1 不清楚 RAG 的整体结构

刚开始做 V6 时，我对 RAG 的理解还比较模糊，只知道它和知识库问答有关，但不清楚代码里应该怎么组织。

后来我把它拆成几个部分：

```text
Knowledge Base
→ Retrieval
→ Context
→ Answer Generation
→ Sources
```

这样之后，整个结构就清楚很多。V6.1 到 V6.5 其实就是按照这个顺序一步一步做出来的。

---

### 6.2 文档检索结果不够准确

一开始关键词搜索比较粗糙，用户问 delay 的时候，有时候会检索到不太相关的内容。

为了解决这个问题，我加入了：

* stop words
* normalize_word()
* 简单复数处理，例如 trips → trip
* required_words 判断，例如 delay 问题必须包含 delay
* score 排序
* top_k 控制返回数量

虽然这还不是专业搜索引擎，但比最初版本稳定很多。

---

### 6.3 Flask 页面找不到 base.html

在接入 `/rag` 页面时，我一开始用了：

```html
{% extends "base.html" %}
```

但是项目里并没有 `base.html`，所以 Flask 报错：

```text
TemplateNotFound: base.html
```

解决方法是把 `rag.html` 改成一个完整 HTML 页面，不再依赖 `base.html`。

这个问题让我理解到：Jinja2 的模板继承虽然很方便，但前提是项目里真的有对应的 base template。

---

### 6.4 app.py 和 rag_engine.py 的连接问题

RAG 接入 Flask 时，需要在 `app.py` 里导入：

```python
from rag_engine import ask_rag
```

然后 `/rag` route 里调用：

```python
response = ask_rag(question)
```

一开始我对这个流程还不熟悉。后来理解为：

```text
app.py 负责网页请求
rag_engine.py 负责检索和回答
```

这样分工之后，代码结构就更清楚了。

---

### 6.5 字典取值写错

在 Flask route 中，我一开始把：

```python
sources = response["sources"]
```

写成了类似：

```python
sources = response("sources")
```

这个错误的原因是我把 dictionary 当成函数调用了。

后来我理解了：

```text
函数调用用 ()
字典取值用 []
```

所以应该写：

```python
response["answer"]
response["sources"]
```

这个问题虽然小，但对我理解 Python dictionary 很有帮助。

---

### 6.6 数据库字段和查询函数要对应

V6.4 加 database retrieval 时，需要确保 SQL 里的字段名和 SQLite 表里的字段一致。

例如：

```sql
SELECT truck_id, driver, route, revenue, total_cost, profit, profit_margin, risk_level
FROM trucks
WHERE risk_level = 'High Risk'
```

如果字段名写错，系统就会报错。

所以我先检查了 `database.py` 和 trucks 表的字段，再写查询函数。这个过程让我更加理解数据库结构设计和代码调用之间的关系。

---

### 6.7 函数名不一致导致 NameError

V6.5 时，我一开始有两个类似的函数：

```python
generate_management_recommendation()
generate_management_answer()
```

后来 `ask_rag()` 里调用的是 `generate_management_answer()`，但文件里没有正确放这个函数，就可能导致：

```text
NameError: name 'generate_management_answer' is not defined
```

解决方法是统一函数职责：

* `generate_answer()`：基础知识库回答
* `generate_management_answer()`：V6.5 管理建议回答
* `generate_management_recommendation()`：旧版函数，可以不用或后续删除

这让我意识到函数命名和函数职责要保持清楚，否则项目越大越容易混乱。

---

### 6.8 忘记给 lower() 加括号

测试 V6.5 时，页面报错：

```text
TypeError: argument of type 'builtin_function_or_method' is not iterable
```

原因是我写成了：

```python
question_lower = question.lower
```

正确写法应该是：

```python
question_lower = question.lower()
```

`question.lower` 只是拿到方法本身，`question.lower()` 才是真的执行转小写。

这个问题让我更加注意 Python 方法调用时括号的重要性。

---

### 6.9 页面显示格式不够好

V6.5 初版里，Database Findings 每一行前面都有 `-`，看起来像散乱列表，不太像管理报告。

后来我优化了显示逻辑：

* 数据库标题不加横线
* Truck ID 前面加空行
* 其他字段正常显示
* Suggested Action 单独分区

这样最终输出更像一份运营管理建议报告。

---

## 7. Project Structure 项目结构

当前项目大致结构如下：

```text
FleetMind-Web-V6/
├── app.py
├── database.py
├── fleetmind_core.py
├── rag_engine.py
├── fleetmind.db
├── knowledge_base/
│   ├── cost_notes.txt
│   ├── fleet_policy.txt
│   ├── risk_rules.txt
│   └── route_notes.txt
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── analytics.html
│   ├── records.html
│   ├── trips.html
│   ├── route_analytics.html
│   ├── insights.html
│   ├── rag.html
│   └── ...
├── static/
│   ├── style.css
│   └── charts/
└── README.md
```

---

## 8. How to Run 如何运行

### 1. Clone the repository

```bash
git clone https://github.com/your-username/FleetMind-Web-V6.git
cd FleetMind-Web-V6
```

### 2. Install dependencies

```bash
pip install flask matplotlib
```

### 3. Run the Flask app

```bash
python app.py
```

或者：

```bash
python3 app.py
```

### 4. Open in browser

```text
http://127.0.0.1:5001
```

RAG Assistant 页面：

```text
http://127.0.0.1:5001/rag
```

---

## 9. Example Questions 示例问题

可以在 `/rag` 页面测试：

```text
what should we do with high delay trips
```

```text
what should we check if fuel cost is high
```

```text
which trucks are high risk
```

```text
what should managers do with high risk trucks
```

```text
what should we know about Chongqing-Kunming route
```

---

## 10. What I Learned 学到的内容

通过 V6，我主要学习到了：

* Flask route 和 HTML form 如何连接
* 如何用 SQLite 存储和查询结构化数据
* 如何把 txt 文件作为本地知识库
* 如何把文档切成 chunks
* 如何做简单关键词检索
* 如何计算检索 score
* 如何返回 sources
* 如何把数据库查询结果作为 RAG context
* 如何组织 doc_results 和 db_results
* 如何生成结构化 management recommendation
* 如何 debug Flask 和 Python 报错
* 如何逐步把一个学生项目升级成更完整的 portfolio project

---

## 11. V5 to V6 Improvements

相比 V5，V6 的主要升级是：

| 方面   | V5                                     | V6                                          |
| ---- | -------------------------------------- | ------------------------------------------- |
| 数据来源 | SQLite database                        | SQLite + knowledge_base                     |
| 核心功能 | 数据库驱动的运营分析                             | 数据库分析 + RAG 问答                              |
| 页面   | Dashboard / Analytics / Trips / Routes | 新增 RAG Assistant                            |
| 建议逻辑 | Rule-based insights                    | RAG + database + management answer          |
| 数据类型 | Structured data                        | Structured + unstructured data              |
| 项目定位 | Fleet analytics platform               | AI-assisted logistics decision support tool |

---

## 12. Limitations 当前不足

V6 目前还是一个学习型项目，还有一些不足：

* RAG 检索还是 keyword-based，不是 embedding-based semantic search
* 没有接入真正的大语言模型 API
* 回答生成主要是 rule-based template
* 数据库检索目前主要支持 high risk trucks，问题类型还不够多
* 没有用户登录和权限系统
* 前端页面还比较简单
* 数据量较小，还没有做性能优化
* 缺少自动化测试

这些不足也是后续版本可以继续改进的方向。

---

## 13. Future Improvements 后续改进方向

之后可以继续升级：

* 加入 embedding-based search
* 接入 OpenAI API 或其他 LLM API
* 支持更多数据库问题，例如 high delay trips、loss-making routes、high cost per km routes
* 让 RAG assistant 能同时查询 trucks、trips、routes
* 增加 conversation history
* 优化前端 UI
* 增加登录系统
* 增加测试数据和自动化测试
* 部署到云端
* 加入更完整的 architecture diagram

---

## 14. Project Reflection 项目反思

FleetMind V6 对我来说是一个很重要的版本。

V1 到 V5 更多是在练习 Python、Flask、SQLite 和数据分析。V6 则让我开始接触 AI application 的基本结构，尤其是 RAG 的思想。

这个项目还不是一个真正复杂的 AI 系统，但它让我理解到，一个 AI assistant 不只是“聊天框”，而是需要：

```text
数据来源
检索逻辑
上下文组织
回答结构
业务规则
网页交互
```

这些部分组合在一起，才更接近一个实际可用的应用。

FleetMind V6 让我把自己的物流背景、Python 编程、数据库课程知识和 AI/RAG 学习结合到了一起。它不是一个完美项目，但它记录了我从基础 Web dashboard 一步步升级到 AI-assisted logistics assistant 的过程。

---

## 15. Current Version Status

当前版本：FleetMind Web V6.5 / V6.6 polish stage

当前完成内容：

* Knowledge base completed
* Simple retrieval engine completed
* Flask RAG page completed
* SQLite database retrieval completed
* Better management answer logic completed
* README and portfolio polishing in progress

FleetMind V6 当前可以定义为：

```text
A Flask-based AI logistics assistant that combines local knowledge-base retrieval with SQLite operational data to generate structured fleet management recommendations.
```
