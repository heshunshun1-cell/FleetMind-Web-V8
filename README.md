# FleetMind Web V5

## 项目简介

FleetMind Web V5 是一个基于 Flask 和 SQLite 的物流车队运营分析系统。

这个项目最早来自我之前的 Python 车辆成本分析程序，后来一步步升级成 Flask 网页版、CSV Dashboard，再到现在的数据库驱动版本。V5 的目标是把 FleetMind 从一个简单的数据展示网页，升级成一个可以保存、管理、分析 truck 和 trip 数据的小型物流运营系统。

V5 的核心变化是：

```text
CSV Dashboard
→ SQLite Database
→ Truck / Trip / Route Analytics
→ CRUD Data Management
````

简单来说，FleetMind V5 不只是看数据，还可以新增、修改、删除数据，并且让 dashboard、analytics 和 insights 自动更新。

---

## 项目背景

我想做这个项目，是因为我对物流业务和数据分析都比较感兴趣。真实的物流公司不只关心一辆车赚不赚钱，还会关心每一趟运输任务的利润、延误、路线表现和风险。

所以 V5 主要围绕三个层级展开：

```text
Truck-level analysis：车辆层面
Trip-level analysis：运输任务层面
Route-level analysis：路线层面
```

这样项目会更接近真实物流运营场景。

---

## 从 V5.1 到最终版 V5

### V5.1：SQLite 数据库基础

V5.1 的重点是把项目从 CSV 文件升级到 SQLite 数据库。

我创建了 `fleetmind.db` 和 `trucks` 表，让 truck records 可以真正保存到数据库中。Dashboard、Records、Analytics 和 Insights 也开始从 SQLite 读取数据。

这一步让我理解到：
一个项目想更像真实系统，不能只靠 CSV 文件，数据库结构非常重要。

---

### V5.2：Trip Records

V5.2 加入了 `trips` 表，用来保存每一趟运输任务。

每条 trip 包括 route、distance、revenue、cost、profit、delay、risk level 等信息。系统也新增了 `/trips` 页面、Trip Summary Cards 和 Trip-Level Insights。

这一步让项目从只分析车辆，升级到可以分析具体运输任务。

---

### V5.3：Route Analytics

V5.3 在 trip 数据基础上，加入了路线分析页面 `/route-analytics`。

系统会按 route 汇总 trip 数据，计算每条路线的 revenue、profit、average delay、average cost per KM 和 risk level。

这一步让我感觉项目更接近真实物流管理，因为公司经常需要知道哪条路线赚钱、哪条路线延误高、哪条路线风险大。

---

### V5.4：Add New Trip

V5.4 加入了 `/add-trip` 页面，用户可以手动新增运输任务。

新增 trip 后，系统会自动计算：

* Profit
* Profit Margin
* Cost per KM
* Risk Level

新增的数据会自动影响：

```text
/trips
/route-analytics
Trip Insights
Route Insights
```

这一步让系统从“展示 sample data”变成了“可以录入新业务数据并自动分析”。

---

### 最终版 V5：CRUD 数据管理

后来我发现一个重要问题：
如果 truck 或 trip 数据输入错了，系统不能修改，也不能删除。

所以最终版 V5 补上了基础 CRUD 功能：

| 数据类型     | Create | Read | Update | Delete |
| -------- | ------ | ---- | ------ | ------ |
| Truck 数据 | 支持     | 支持   | 支持     | 支持     |
| Trip 数据  | 支持     | 支持   | 支持     | 支持     |

现在 V5 已经可以完成：

```text
新增数据
查看数据
修改数据
删除数据
自动重新计算分析结果
```

这样它才真正像一个 database-driven fleet analytics system。

---

## 主要功能

FleetMind V5 目前支持：

* Truck 数据管理：新增、查看、修改、删除 truck records
* Trip 数据管理：新增、查看、修改、删除 trip records
* Fleet Dashboard：展示车队整体收入、成本、利润、风险等指标
* Fleet Analytics：用 matplotlib 生成收入、利润、风险、成本压力图表
* Operational Insights：根据 truck 数据生成运营建议
* Trip Records：展示每趟运输任务的数据
* Trip Summary Cards：统计 trip 总数、总收入、总利润、高延误任务等
* Trip-Level Insights：分析高延误、高成本、低利润率等运输任务
* Route Analytics：按路线汇总收入、利润、延误、成本和风险
* Route-Level Insights：找出高风险路线、最高延误路线、最赚钱路线等

---

## 遇到的问题和解决方法

### 1. CSV 不适合继续扩展

早期版本主要依赖 `fleet_data.csv`。CSV 对简单展示够用，但当系统有 records、dashboard、analytics、insights 后，就不够灵活。

解决方法：
我把数据存储升级为 SQLite，并把主要页面的数据来源改成数据库。

---

### 2. 修改 sample data 后页面没有变化

我一开始修改了 `init_trips.py`，但网页显示的数据没有变化。

后来发现原因是：
Python 文件变了，不代表 SQLite 数据库里的旧数据会自动变。

解决方法：

```bash
python3 init_trips.py
```

重新初始化 trips 表后，页面才会读取到新数据。

---

### 3. 旧 trip 的 risk level 和新规则不一致

有些旧 trip 的 delay_hours 已经超过 24 小时，但 risk level 还是 Normal 或 Excellent。

原因是旧数据是在旧规则下写入数据库的。

解决方法：
我写了 `fix_trip_risk_levels.py`，重新计算旧 trip 的风险等级。

```bash
python3 fix_trip_risk_levels.py
```

---

### 4. 新增 trip 后路线分析要自动更新

新增 trip 后，不应该只出现在 `/trips`，也应该影响 `/route-analytics`。

解决方法：
Route Analytics 不写死数据，而是从 `trips` 表按 route 分组计算。所以新增、修改、删除 trip 后，路线分析会自动更新。

---

### 5. 数据输入错了不能修改

一开始系统只能新增和查看数据，不能修改和删除。

解决方法：
我给 truck 和 trip 都加入了基础 CRUD 功能。现在用户可以在网页里直接 edit 和 delete 数据。

---

## Risk Level 规则

Trip risk level 的主要规则是：

```text
High Risk:
profit < 0 或 delay_hours >= 24

Warning:
profit_margin < 10 或 delay_hours >= 12

Excellent:
profit_margin >= 25 且 delay_hours < 6

Normal:
其他情况
```

这个规则让系统可以根据业务数据自动判断风险，而不是只展示数字。

---

## 技术栈

这个项目使用了：

* Python
* Flask
* SQLite
* SQL
* HTML
* CSS
* Jinja2
* matplotlib

我在这个项目中练习了：

* Flask routing
* HTML form
* SQLite database connection
* SQL query
* CRUD operations
* Dashboard metrics
* Rule-based insights
* Data visualization
* Logistics business analysis

---

## 项目结构

```text
FleetMind-Web-V5/
│
├── app.py
├── database.py
├── fleetmind_core.py
├── init_db.py
├── init_trips.py
├── fix_trip_risk_levels.py
├── fleetmind.db
├── README.md
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── analytics.html
│   ├── insights.html
│   ├── records.html
│   ├── trips.html
│   ├── route_analytics.html
│   ├── add_trip.html
│   ├── edit_trip.html
│   ├── edit_truck.html
│   └── ...
│
├── static/
│   ├── style.css
│   └── charts/
```

---

## 如何运行

安装依赖：

```bash
pip install flask matplotlib
```

初始化 truck 数据：

```bash
python3 init_db.py
```

初始化 trip 数据：

```bash
python3 init_trips.py
```

如需修复旧 trip 风险等级：

```bash
python3 fix_trip_risk_levels.py
```

运行项目：

```bash
python3 app.py
```

浏览器打开：

```text
http://127.0.0.1:5001
```

---

## 当前版本总结

FleetMind Web V5 已经从一个 CSV dashboard 升级成了一个 SQLite database-driven fleet analytics platform。

现在系统支持：

```text
Truck CRUD
Trip CRUD
Fleet Dashboard
Fleet Analytics
Operational Insights
Trip Records
Trip-Level Insights
Route Analytics
Route-Level Insights
```

对我来说，V5 最大的进步是：
它不再只是一个展示数据的网页，而是一个有数据库、有增删改查、有分析结果、有业务建议的小型物流数据系统。

---

## 下一步计划：FleetMind V6

V6 我计划做成：

```text
RAG-based Intelligent Logistics Assistant
```

也就是让 AI assistant 不只是固定回答，而是可以根据数据库里的 truck、trip 和 route 数据回答问题。

未来可以加入：

* RAG-based assistant
* 自然语言查询数据库
* 按 route、truck、risk level、date 筛选
* Chart.js 或 Plotly 交互式图表
* 更专业的表单验证和删除确认
* 简单的利润或延误预测

---

## Final Reflection

FleetMind V5 对我来说是一次比较完整的项目升级。

我从一个简单 Python 项目开始，一步步加入网页、数据库、dashboard、analytics、insights、trip records、route analytics 和 CRUD。过程中也遇到了很多问题，比如数据库没有更新、旧规则和新规则不一致、页面文字没有同步修改、数据不能编辑删除等。

这些问题让我更理解真实项目开发的过程：
不是把功能写出来就结束，还要不断测试、发现问题、修复问题，并让系统结构变得更合理。

