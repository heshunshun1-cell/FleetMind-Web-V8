# FleetMind-Web-V3

## 项目简介

FleetMind-Web-V3 是我在 FleetMind-Web-V2 基础上继续升级出来的物流数据分析 Web 项目。

V2 版本已经实现了：

* 用户新增 Truck 数据
* 自动计算收入、成本、利润、利润率和风险等级
* 将新增车辆保存到 `fleet_data.csv`
* 在 Records 页面查看历史保存记录

但是 V2 主要还是偏向“单条记录保存”和“历史记录查看”。

所以在 V3 中，我想进一步升级成一个更像真实物流管理系统的版本：

> 不只是看一辆车，而是从整个车队角度看运营情况。

因此，V3 的核心目标是新增一个 Fleet Dashboard。

---

## 从 V2 到 V3 的升级目标

V2 的功能重点是：

```text
Add Truck
↓
Analyse Truck
↓
Save to CSV
↓
View Records
```

V3 的升级重点是：

```text
Read CSV
↓
Calculate Fleet Statistics
↓
Show Dashboard
```

也就是说，V3 不再只是保存数据，而是开始利用已有数据做统计分析。

---

## V3 新增功能

### 1. Fleet Dashboard 页面

V3 新增了一个页面：

```text
/dashboard
```

对应文件：

```text
templates/dashboard.html
```

这个页面会读取 `fleet_data.csv` 中已经保存的车辆记录，并显示整体运营统计结果。

---

### 2. Dashboard 统计指标

目前 Dashboard 显示以下指标：

* Truck Count
* Total Revenue
* Total Cost
* Total Profit
* Average Profit Margin
* High Risk Trucks
* Best Performing Truck
* Lowest Margin Truck
* Most Common Cost Pressure

这些指标让系统从“单车分析工具”开始变成一个“小型车队运营看板”。

---

### 3. 新增 `get_dashboard_data()`

在 `fleetmind_core.py` 中，我新增了：

```python
def get_dashboard_data():
```

这个函数负责：

```text
读取 CSV 文件
↓
遍历所有车辆记录
↓
累加收入、成本、利润和利润率
↓
统计高风险车辆数量
↓
找出表现最好和利润率最低的车辆
↓
统计最常见的成本压力
↓
把结果返回给 Flask 页面
```

这个函数是 V3 的核心。

它让 Dashboard 页面不只是静态网页，而是可以根据 CSV 数据动态生成统计结果。

---

## V3 的开发过程

### 第一步：先写数据逻辑，而不是先写页面

一开始我没有直接写 `dashboard.html`，而是先在 `fleetmind_core.py` 里写：

```python
get_dashboard_data()
```

我觉得这是这次升级里比较重要的一点。

因为 Dashboard 本质上不是先有网页，而是先有数据统计逻辑。

所以开发顺序是：

```text
fleetmind_core.py
先处理数据

↓

app.py
再添加 Flask route

↓

dashboard.html
最后显示到网页上
```

这样比直接写 HTML 更清楚，也更容易 Debug。

---

### 第二步：在 Flask 中新增 `/dashboard`

在 `app.py` 中，我新增了：

```python
@app.route("/dashboard")
def dashboard():
    data = get_dashboard_data()
    return render_template("dashboard.html", data=data)
```

一开始我没有直接连接 HTML，而是先用：

```python
return str(data)
```

测试数据能不能正常显示。

确认数据正常后，才改成：

```python
return render_template("dashboard.html", data=data)
```

这个过程让我意识到：

> 写 Web 项目时，不要一上来就美化页面，应该先确认数据是对的。

---

### 第三步：创建 Dashboard 页面

之后我新建了：

```text
templates/dashboard.html
```

最开始只是简单显示：

```html
<p>Truck Count: {{ data.truck_count }}</p>
```

后来再慢慢改成卡片式布局。

现在 Dashboard 使用了卡片结构来显示不同指标，看起来更像一个真实系统的运营面板。

---

## V3 中遇到的问题和解决方法

### 1. records 和 record 混淆

在写高风险车辆统计时，我一开始写错了：

```python
records["risk_level"]
```

结果报错：

```text
TypeError: list indices must be integers or slices, not str
```

后来发现原因是：

```python
records
```

是整个列表。

而：

```python
record
```

才是循环里的单条数据。

正确写法应该是：

```python
for record in records:
    if record["risk_level"] == "High Risk":
        high_risk_count += 1
```

这个错误让我更清楚地理解了：

```text
records = list
record = dict
record["risk_level"] = 当前车辆的风险等级
```

这个点虽然基础，但对理解 CSV 数据读取非常重要。

---

### 2. CSV 读取出来的数字都是字符串

`read_trucks_from_csv()` 读取出来的数据虽然看起来像数字，但其实都是字符串。

比如：

```python
record["revenue"]
```

读出来是：

```python
"68000"
```

不是：

```python
68000
```

所以在 Dashboard 统计时，必须写：

```python
float(record["revenue"])
```

同样地，利润、成本、利润率都要转换成 `float` 后才能计算。

---

### 3. Dashboard 一开始只显示字典

最开始访问 `/dashboard` 时，页面只是显示：

```python
{'truck_count': 2, 'total_revenue': 500000.0}
```

虽然很丑，但这个步骤很有用，因为它证明后端数据已经算出来了。

后来我才把它接入：

```html
dashboard.html
```

这让我学到一个开发习惯：

> 先让功能跑通，再慢慢让它变好看。

---

### 4. CSS class 名字影响了其他页面

Dashboard 一开始使用了：

```css
.card
```

但是项目里其他页面，比如 Sample Trucks 页面，也用了 `.card`。

结果 Dashboard 的样式影响到了 Sample Trucks 页面，导致原来的页面样式变了。

后来我把 Dashboard 的卡片 class 改成：

```css
.dashboard-card
```

这样 Dashboard 的样式就不会影响其他页面。

这个问题让我第一次比较直观地理解了：

> CSS class 命名不能太随意，不然不同页面之间会互相污染。

---

### 5. Dashboard 上色一开始不生效

我想给 Dashboard 里的利润和风险数字上色，比如：

* 正利润显示绿色
* 高风险车辆数量显示红色

但是一开始颜色没有变化。

后来发现是因为我之前写了：

```css
.dashboard-card p {
    color: #1f4e79;
}
```

这条规则把所有 Dashboard 卡片里的 `<p>` 都固定成了蓝色。

后来我用更具体的 CSS 选择器覆盖：

```css
.dashboard-card p.profit-positive {
    color: #1f8f4d;
}

.dashboard-card p.profit-negative {
    color: #c0392b;
}
```

这样颜色才正常显示。

这次问题让我学到了 CSS 优先级。

---

## V3 当前效果

现在 V3 的 Dashboard 可以显示：

```text
Truck Count
Total Revenue
Total Cost
Total Profit
Average Profit Margin
High Risk Trucks
Best Performing Truck
Lowest Margin Truck
Most Common Cost Pressure
```

其中：

* Total Profit 为正时显示绿色
* Average Profit Margin 表现好时显示绿色
* High Risk Trucks 大于 0 时显示红色
* 普通统计数据保持蓝色

整体视觉比 V2 更清楚，也更像一个运营分析页面。

---

## Dashboard 数据来源说明

目前 Dashboard 只统计：

```text
fleet_data.csv
```

里面保存的车辆记录。

它不会统计 Sample Trucks 页面里的样本数据。

这样设计是故意的，因为 Sample Trucks 是演示数据，如果混入 Dashboard，会影响真实保存记录的统计结果。

所以当前逻辑是：

```text
Sample Trucks
= 用于演示和测试

CSV Records
= 用户真实保存的数据

Dashboard
= 基于 CSV Records 的统计分析
```

---

## V2 和 V3 的区别

| 版本 | 主要功能                  | 特点            |
| -- | --------------------- | ------------- |
| V2 | CSV Storage + Records | 可以保存和查看车辆记录   |
| V3 | Fleet Dashboard       | 可以统计和分析整体车队表现 |

简单来说：

```text
V2 让系统能“记住数据”
V3 让系统能“分析数据”
```

这是这次升级最大的变化。

---

## 当前项目结构

```text
FleetMind-Web-V3

app.py
fleetmind_core.py
fleet_data.csv
fleet_history.txt

templates/
│
├── index.html
├── result.html
├── records.html
├── samples.html
├── compare.html
├── assistant.html
├── history.html
├── new_truck.html
└── dashboard.html

static/
│
└── style.css

README.md
```

---

## 当前技术栈

V3 使用到的技术包括：

* Python
* Flask
* HTML
* CSS
* CSV
* Jinja2 Template
* Git
* GitHub

目前还没有使用数据库，数据仍然保存在 CSV 文件中。

---

## 我对 V3 的理解

FleetMind-Web-V3 对我来说不是一次大重写，而是在 V2 基础上的一次自然升级。

V2 解决了：

> 数据怎么保存？

V3 继续解决：

> 保存下来的数据怎么分析？

这让我感觉这个项目开始从一个简单练习，慢慢变成一个有结构的小型业务系统。

在这次升级中，我学到的最重要的东西不是某一行代码，而是整个开发流程：

```text
先确认数据来源
↓
写核心统计函数
↓
用 Flask route 测试
↓
再连接 HTML 页面
↓
最后优化 CSS 和用户体验
```

这个过程让我更像是在做一个真实项目，而不是只完成一道作业题。

---

## 下一步计划

### V4：Data Visualization

下一版计划加入图表功能，例如：

* Revenue Bar Chart
* Profit Bar Chart
* Risk Distribution Chart
* Cost Pressure Distribution Chart

这样 Dashboard 不只是显示数字，也能通过图表展示趋势和结构。

---

### V5：SQLite Database

目前系统使用 CSV 保存数据。

未来希望把 CSV 升级成 SQLite，让数据管理更接近真实系统。

目标包括：

* 查询记录
* 删除记录
* 修改记录
* 按风险等级筛选
* 按路线筛选
* 按司机筛选

---

## 总结

FleetMind-Web-V3 是我从 V2 继续升级出来的版本。

这次升级的核心是：

```text
从 Records 页面
升级到 Dashboard 页面
```

也就是从“保存数据”走向“分析数据”。

这个过程中我遇到了不少问题，比如：

* `records` 和 `record` 混淆
* CSV 数字需要转换成 `float`
* CSS class 影响其他页面
* Dashboard 颜色被 CSS 优先级覆盖

但这些问题最后都被一步步解决了。

所以 V3 不只是功能升级，也是我对 Web 项目结构、数据处理和前端样式理解的一次升级。

FleetMind 还会继续迭代。
