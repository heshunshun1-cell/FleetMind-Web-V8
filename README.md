# FleetMind Web V6

## 项目简介

FleetMind 是我从 Python 基础项目一步步升级出来的物流车队运营分析系统。

前几个版本主要完成了车辆成本分析、Flask 网页、CSV 记录、Dashboard 可视化、SQLite 数据库、Trip records 和 Route analytics。到了 V6，我开始尝试加入 RAG 思想，让 FleetMind 不只是展示数据，也可以根据自己的知识库回答一些车队运营问题。

V6 的核心定位是：

> FleetMind V6 - RAG-based Fleet Operations Assistant  
> 基于 RAG 的车队运营问答助手

目前这个版本还没有接入真正的大模型 API，而是一个我自己手写的 simple rule-based RAG prototype。重点是理解 RAG 的底层流程。

---

## 从 V1 到 V6 的升级

| 版本 | 主要内容 |
|---|---|
| V1 | Python 命令行车辆成本分析 |
| V2 | Flask 网页版，可以输入车辆数据 |
| V3 | 加入 CSV records，保存和查看历史车辆记录 |
| V4 | 加入 Dashboard 和图表分析 |
| V5 | 升级 SQLite 数据库，加入 trucks、trips、route analytics 和 insights |
| V6 | 加入 knowledge base 和 simple RAG assistant，支持运营问答 |

---

## 为什么做 V6

V5 已经可以分析车辆和运输任务数据，也能生成一些 rule-based insights。

但是 V5 的建议是固定规则生成的，用户不能自由提问。

例如，V5 可以显示：

```text
This trip is High Risk.
````

但它不能很好回答：

```text
为什么 high delay trip 需要复查？
fuel cost 太高时应该检查什么？
Chongqing-Kunming route 有什么特点？
cost per kilometre 为什么重要？
```

所以 V6 的目标是：

> 让 FleetMind 可以根据自己的知识库，回答一些物流运营相关问题。

---

## 什么是 RAG

RAG 全称是 Retrieval-Augmented Generation。

我对它的理解是：

```text
先查资料，再组织回答。
```

它主要包括三步：

| 部分         | 中文理解 | 在 FleetMind V6 中的作用 |
| ---------- | ---- | ------------------- |
| Retrieval  | 检索   | 从知识库中找出和问题相关的内容     |
| Augmented  | 增强   | 把检索到的内容作为回答依据       |
| Generation | 生成   | 根据找到的内容组织回答         |

在 FleetMind V6 中，流程是：

```text
用户问题
→ 读取 knowledge_base
→ 切分成 chunks
→ 检索相关 chunks
→ 生成回答
→ 显示 sources
```

---

## V6 新增内容

### 1. knowledge_base 知识库

V6 新增了：

```text
knowledge_base/
```

里面包括：

```text
risk_rules.txt
route_notes.txt
fleet_policy.txt
cost_notes.txt
```

| 文件                 | 作用                                               |
| ------------------ | ------------------------------------------------ |
| `risk_rules.txt`   | 风险判断规则，例如 High Risk、Warning、delay 规则             |
| `route_notes.txt`  | 路线运营知识，例如重庆到广州、深圳、昆明等路线特点                        |
| `fleet_policy.txt` | 车队管理政策，例如高风险记录优先复查                               |
| `cost_notes.txt`   | 成本分析知识，例如 fuel cost、toll cost、cost per kilometre |

这些知识文件采用中英双语形式，方便学习和展示。

---

### 2. rag_engine.py

V6 新增了：

```text
rag_engine.py
```

它实现了一个简单 RAG engine。

主要函数：

| 函数                              | 作用                |
| ------------------------------- | ----------------- |
| `load_documents()`              | 读取知识库 txt 文件      |
| `split_documents_into_chunks()` | 把文档切成 chunks      |
| `normalize_word()`              | 简单处理单复数和标点        |
| `search_chunks()`               | 检索相关 chunks       |
| `clean_text()`                  | 清理输出文本            |
| `generate_answer()`             | 生成回答              |
| `get_sources()`                 | 提取 sources        |
| `ask_rag()`                     | 封装完整 RAG pipeline |

---

## 当前 RAG 流程

```text
question
    ↓
load_documents()
    ↓
documents
    ↓
split_documents_into_chunks()
    ↓
chunks
    ↓
search_chunks()
    ↓
top_k relevant chunks
    ↓
generate_answer()
    ↓
answer + sources
```

示例：

```python
response = ask_rag("what should we do with high delay trips", top_k=3)
```

返回内容包括：

```python
{
    "answer": "...",
    "sources": [...],
    "results": [...]
}
```

---

## 检索逻辑

目前 V6 使用 keyword-based retrieval，还没有使用 embedding。

检索时会做：

* 统一大小写
* 去掉 stop words
* 简单 normalization
* 计算 score
* 使用 min_score 过滤弱相关结果
* 使用 required_words 强制匹配核心词
* 使用 top_k 返回最相关结果

---

## 测试问题

我用以下问题测试了 RAG engine：

```text
what should we do with high delay trips
what should we check if fuel cost is high
what should we know about Chongqing-Kunming route
why is cost per kilometre important
what should managers do with high risk trucks
```

测试结果基本可以正确匹配到对应知识文件。

| 问题类型               | 主要来源                                 |
| ------------------ | ------------------------------------ |
| high delay         | `fleet_policy.txt`, `risk_rules.txt` |
| fuel cost          | `fleet_policy.txt`, `cost_notes.txt` |
| specific route     | `route_notes.txt`                    |
| cost per kilometre | `cost_notes.txt`                     |
| high risk trucks   | `fleet_policy.txt`, `risk_rules.txt` |

---

## 项目结构

```text
FleetMind-Web-V6/
    app.py
    database.py
    fleetmind_core.py
    rag_engine.py
    requirements.txt
    README.md
    .gitignore

    knowledge_base/
        risk_rules.txt
        route_notes.txt
        fleet_policy.txt
        cost_notes.txt

    templates/
    static/
```

---

## 如何运行

在项目目录下运行：

```bash
python3 rag_engine.py
```

程序会自动测试一组问题，并输出回答和 sources。

---

## 遇到的问题

### 1. `.endswith()` 写错

一开始把：

```python
filename.endswith(".txt")
```

写成了：

```python
filename.endwith(".txt")
```

导致报错。后来改成正确的：

```python
endswith()
```

---

### 2. chunk 切分问题

一开始文档没有很好切分。后来使用：

```python
content.split("\n\n")
```

按空行切分文档。

这让我理解到：RAG 里 chunk 的质量和文档格式有关。

---

### 3. 检索结果太杂

一开始只用简单关键词匹配，结果会比较杂。后来逐步加入：

```text
stop words
normalization
min_score
required_words
top_k
```

检索结果变得更稳定。

---

## 我学到了什么

通过 V6，我第一次比较完整地理解了 RAG 的基础流程：

* RAG 不是一开始就调用 AI
* 知识库质量很重要
* documents 需要切成 chunks
* retrieval 是 RAG 的核心
* score 和 top_k 会影响结果质量
* sources 可以让回答更可信
* RAG 需要不断测试和调试

这个版本虽然还没有使用 embedding 或真正的大模型 API，但它让我理解了 RAG 的底层逻辑。

---

## 下一步计划

后续可以继续升级：

* 把 RAG assistant 接入 Flask 页面
* 新增 `/rag-assistant` 页面
* 支持中文问题检索
* 接入 SQLite 数据库，让 assistant 同时读取 fleet data
* 使用 embedding 做语义检索
* 接入 OpenAI API 生成更自然的回答
* 在网页中显示 retrieved chunks 和 sources

---

## 总结

FleetMind V6 是我从传统数据分析项目走向 AI application 的一个重要版本。

它把：

```text
物流业务知识 + 数据分析 + RAG assistant
```

结合在了一起。

这个版本最大的意义是：我没有直接复制复杂框架，而是先用基础 Python 逻辑理解 RAG 是怎么工作的。

```

保存后我们再继续检查 remote，确保后面上传到 `FleetMind-Web-V6`，不是 V5。
```
