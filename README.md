# FleetMind Web V4.5 - Enhanced Fleet Analytics Dashboard

## 项目简介

FleetMind 是一个我自己一步步开发出来的物流车队数据分析 Web App。这个项目最开始只是一个简单的 Truck 单车分析工具，后来逐渐升级成了一个可以保存车辆数据、查看历史记录、生成 Fleet Dashboard，并进一步进行数据可视化分析的小型物流数据系统。

这个项目的灵感来自我对物流运输业务的理解。真实的物流管理并不只是看一辆车收入有多少，还要综合分析成本、利润、利润率、风险等级和主要成本压力。因此，我希望用 Python 和 Flask 做一个简单但有实际业务意义的工具，把车辆运营数据变得更清楚、更直观。

V4 的重点是加入 **Data Visualization 数据可视化功能**。
V4.5 则是在 V4 的基础上进一步打磨页面展示和业务分析体验，让 `/analytics` 页面更像一个完整的数据分析 dashboard。

---

## 项目版本进化

### V1 - Basic Truck Analysis

最初版本主要实现单车分析功能。用户输入一辆 Truck 的运营数据后，系统可以计算：

* Revenue
* Total Cost
* Profit
* Profit Margin
* Risk Level
* Main Cost Pressure
* Suggestion

这一版主要解决的问题是：
**能不能用 Python 和 Flask 把一辆车的运营表现分析出来。**

---

### V2 - CSV Data Storage

V2 加入了 CSV 数据保存功能。

新增：

* `fleet_data.csv`
* `records.html`
* `save_truck_to_csv()`
* `read_trucks_from_csv()`

用户新增车辆后，系统可以把车辆数据保存到 CSV 文件中，并在 Records 页面查看历史保存记录。

这一版让 FleetMind 从“一次性计算工具”变成了一个可以保存数据的 Web App。

---

### V3 - Fleet Dashboard

V3 新增 Fleet Dashboard 页面：

```text
/dashboard
```

Dashboard 可以展示整个车队的汇总数据，例如：

* Truck Count
* Total Revenue
* Total Cost
* Total Profit
* Average Profit Margin
* High Risk Trucks
* Best Performing Truck
* Lowest Margin Truck
* Most Common Cost Pressure

这一版让项目从“单车分析”升级到了“车队整体分析”。

---

### V4 - Data Visualization Analytics

V4 新增 Analytics 页面：

```text
/analytics
```

并使用 `matplotlib` 从 `fleet_data.csv` 自动生成图表。

新增图表包括：

* Revenue by Truck
* Profit by Truck
* Risk Level Distribution
* Cost Pressure Distribution

图表会保存到：

```text
static/charts/
```

这一版让 FleetMind 从“数字 summary dashboard”升级成了“可视化 analytics dashboard”。

---

### V4.5 - Enhanced Analytics Dashboard

V4.5 是在进入 SQLite V5 前的一次精修版本。
目标不是大改结构，而是把 V4 的展示效果、业务分析能力和 GitHub 可读性进一步提升。

V4.5 新增：

* `requirements.txt`
* Analytics Summary Cards
* Loss-making Trucks Section
* Total Profit 条件上色
* Average Profit Margin 条件上色
* Loss-making Trucks 数字上色
* Loss-making Trucks warning 样式
* 更清晰的 README 和运行说明

现在 `/analytics` 页面不只是四张图，而是形成了更完整的分析结构：

```text
关键指标总览
↓
亏损车辆风险提示
↓
Revenue / Profit / Risk / Cost Pressure 图表
```

---

## 当前核心功能

### 1. Truck Analysis

用户可以输入单辆 Truck 的运营数据，系统会自动计算：

* 总成本
* 利润
* 利润率
* 风险等级
* 最大成本压力
* 运营建议

---

### 2. CSV Data Storage

项目使用 `fleet_data.csv` 保存车辆数据。

这让用户可以持续添加车辆记录，而不是每次运行都重新输入。

---

### 3. Records Page

Records 页面可以展示历史保存的车辆数据。

这一步让项目具备了基本的数据管理能力。

---

### 4. Fleet Dashboard

Dashboard 页面展示车队整体表现，包括收入、成本、利润、风险和主要成本压力。

它的作用是帮助用户快速理解整个车队当前的运营状态。

---

### 5. Analytics Page

Analytics 页面是 V4 和 V4.5 的核心升级。

目前包含：

* Summary Cards
* Loss-making Trucks Section
* Revenue Chart
* Profit Chart
* Risk Distribution Chart
* Cost Pressure Distribution Chart

---

## Analytics Summary Cards

V4.5 在 Analytics 页面顶部加入了四个关键指标卡片：

* Total Revenue
* Total Profit
* Average Profit Margin
* Loss-making Trucks

其中：

* Total Profit 会根据正负自动上色
* Average Profit Margin 会根据表现自动上色
* Loss-making Trucks 如果数量大于 0，会显示为红色提醒

这个设计让用户进入页面后，可以先看到最重要的车队表现，再往下看详细图表。

---

## Loss-making Trucks Section

V4.5 新增了专门的亏损车辆区域。

如果有车辆利润为负，系统会显示：

* Truck ID
* Revenue
* Total Cost
* Profit
* Risk Level
* Main Cost Pressure

亏损车辆区域使用了 warning 样式：

* 淡红色背景
* 红色左边框
* 红色亏损数字

这个功能非常实用，因为真实业务中，发现亏损车辆比只看高收入车辆更重要。

例如，一辆车收入高并不代表它赚钱。如果成本过高，利润仍然可能是负数。
所以 FleetMind 不只是看 revenue，而是更关注 profit 和 risk。

---

## 数据可视化图表

### 1. Revenue by Truck

每辆车收入柱状图。

这个图可以帮助用户快速比较不同 Truck 的收入表现。

生成文件：

```text
static/charts/revenue_chart.png
```

---

### 2. Profit by Truck

每辆车利润柱状图。

这张图可以显示盈利车辆和亏损车辆。
如果某辆车利润为负，柱子会向下，并且会直接显示负数数值。

生成文件：

```text
static/charts/profit_chart.png
```

---

### 3. Risk Level Distribution

风险等级分布图。

风险等级固定为四类：

```text
Excellent
Normal
Warning
High Risk
```

即使某一类当前车辆数量为 0，也会保留这个分类逻辑。

生成文件：

```text
static/charts/risk_chart.png
```

---

### 4. Cost Pressure Distribution

主要成本压力分布图。

系统会统计每辆车的最大成本压力来源，例如：

```text
Fuel Cost
Repair Cost
Toll Cost
Salary Cost
Insurance Cost
```

这张图可以帮助用户理解车队当前最集中的成本问题。

生成文件：

```text
static/charts/cost_pressure_chart.png
```

---

## 技术实现思路

V4.5 仍然保持 V4 的基本技术路线：

```text
读取 fleet_data.csv
↓
Python 处理车辆数据
↓
matplotlib 生成 PNG 图表
↓
保存到 static/charts/
↓
Flask + Jinja2 在 analytics.html 页面中展示
```

这样做的好处是结构清楚，适合当前阶段逐步学习和展示。

虽然还没有使用 SQLite、PostgreSQL、React 或 Docker，但项目已经完整体现了一个基础数据分析 Web App 的核心流程：

```text
数据输入
↓
数据存储
↓
数据计算
↓
数据汇总
↓
数据可视化
↓
业务解释
```

---

## 主要技术栈

本项目目前使用：

* Python
* Flask
* HTML
* CSS
* CSV
* Jinja2
* matplotlib
* Git
* GitHub

---

## 当前项目结构

```text
FleetMind-Web-V4-DS/

app.py
fleetmind_core.py
fleet_data.csv
fleet_history.txt
README.md
requirements.txt

templates/
├── index.html
├── result.html
├── records.html
├── samples.html
├── compare.html
├── assistant.html
├── history.html
├── new_truck.html
├── dashboard.html
└── analytics.html

static/
├── style.css
└── charts/
    ├── revenue_chart.png
    ├── profit_chart.png
    ├── risk_chart.png
    └── cost_pressure_chart.png
```

---

## How to Run This Project

### 1. Clone this repository

```bash
git clone https://github.com/heshunshun1-cell/FleetMind-Web-V4-DS.git
```

### 2. Enter the project folder

```bash
cd FleetMind-Web-V4-DS
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

### 4. Run the Flask app

```bash
python3 app.py
```

### 5. Open the browser

Visit:

```text
http://127.0.0.1:5001
```

If your Flask app runs on a different port, use the port shown in the terminal.

---

## 遇到的问题和解决过程

### 1. CSV 字段名不匹配

一开始写 Revenue Chart 时，我本来想用 `truck_name` 作为横坐标，但后来检查 `fleet_data.csv` 后发现真实字段是：

```text
truck_id
```

如果继续使用 `truck_name`，程序会出现 `KeyError`。

后来我改成：

```python
row["truck_id"]
```

这个问题让我意识到，做数据项目时不能凭感觉写字段名，必须先确认真实数据结构。

---

### 2. matplotlib 在 Flask 中导致程序崩溃

开发 V4 时，matplotlib 在 Flask 中运行时出现过 Mac 相关报错：

```text
NSWindow should only be instantiated on the main thread
```

原因是 matplotlib 默认可能尝试打开图形窗口，但 Flask Web App 后台运行时不应该弹出 GUI 窗口。

解决方法是在图表函数中加入：

```python
import matplotlib
matplotlib.use("Agg")
```

这样 matplotlib 就只在后台生成 PNG 图片，不会打开窗口。

这个问题让我学到：
在 Web 项目里使用 matplotlib，需要注意后端渲染模式。

---

### 3. 亏损车辆不够明显

Profit Chart 一开始虽然能显示负利润，但亏损车辆只是柱子向下，不够直观。

后来我加入了数值标签，让亏损车辆可以直接显示负数。
V4.5 又进一步加入了 Loss-making Trucks Section 和红色 warning 样式，让亏损车辆变得更醒目。

这个改动让我意识到：
数据分析不是只把图画出来，还要让用户快速看懂重点问题。

---

### 4. Risk Chart 应该固定四个等级

一开始 Risk Chart 是根据 CSV 中实际出现的风险等级生成。
如果某个等级没有出现，比如 `Warning`，图表中就不会显示。

后来我改成固定四类：

```python
risk_counts = {
    "Excellent": 0,
    "Normal": 0,
    "Warning": 0,
    "High Risk": 0
}
```

这样即使某个等级数量为 0，也能保持分析标准完整。

这让我意识到，数据分析不仅要读取数据，还要设计合理的分析框架。

---

## 我从 V4 到 V4.5 学到了什么

从 V4 到 V4.5，我感觉这个项目不只是多加了几个页面或样式，而是更接近一个真正的数据 dashboard。

V4 让我学会了：

* 用 matplotlib 生成图表
* 把图表保存到 static 文件夹
* 在 Flask 页面中显示图表
* 从 CSV 中读取并分析数据

V4.5 让我进一步理解：

* 如何设计 Summary Cards
* 如何突出关键业务指标
* 如何识别亏损车辆
* 如何用颜色和样式表达风险
* 如何让 GitHub 项目更容易运行和展示

现在的 FleetMind 已经不是一个简单的 Flask 小网页，而是一个具备基础数据分析、业务解释和可视化展示能力的学生项目。

---

## 当前项目评价

我认为 FleetMind V4.5 已经具备了一个完整数据分析项目的基本结构：

```text
数据输入
数据保存
历史记录
汇总分析
图表可视化
亏损识别
风险提示
项目文档
```

相比普通的课程小作业，它更完整，也更有业务背景。
尤其是它围绕物流车队运营展开，而不是随机做一个没有场景的 demo。

当然，它目前仍然有一些限制：

* 数据仍然存储在 CSV 中
* 图表还是 matplotlib 静态 PNG
* 还没有数据库
* 还没有 SQL 查询筛选
* 还没有交互式图表
* 还没有 machine learning

这些限制也正好引出了下一步 V5 的方向。

---

## Future Improvements

下一步我计划把 FleetMind 升级到 V5：

```text
FleetMind V5 – Database-driven Fleet Analytics Platform
```

V5 的目标是从 CSV 可视化 dashboard 升级为 SQLite 数据库驱动的车队运营分析系统。

计划加入：

* SQLite 数据库
* trucks / trips / routes 表
* trip-level records
* SQL 查询和筛选
* trucks 页面
* trips 页面
* 更强的 analytics 页面
* Chart.js 或 Plotly 交互式图表
* rule-based insights 页面

V5 的核心目标不是马上加入大模型，而是先把系统底层做扎实：

```text
CSV-based analytics dashboard
↓
SQLite database-driven fleet analytics platform
```

---

## 总结

FleetMind V4.5 是我从基础 Flask Web App 走向数据分析 dashboard 的重要一步。

它让我把 Python、Flask、CSV、Jinja2、CSS、matplotlib 和 GitHub 项目管理真正连接到了一起。

对我来说，这个项目不只是一次代码练习，而是一次从“会写功能”到“会做数据产品”的进步。

FleetMind 未来还可以继续升级，但 V4.5 已经证明了一个完整的数据分析 Web 项目可以如何从零开始，一步步成长起来。
