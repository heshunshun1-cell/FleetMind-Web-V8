import csv
import os
# 负责写入csv，os负责检查文件是否存在
# 是我们以后保存新增车辆数据的文件名
CSV_FILE = "fleet_data.csv"



class Truck:
    def __init__(self, truck_id, driver, route, revenue, fuel_cost, 
                 toll_cost, repair_cost, salary_cost, insurance_cost, other_cost):
        self.truck_id = truck_id
        self.driver = driver
        self.route = route
        self.revenue = revenue
        self.fuel_cost = fuel_cost
        self.toll_cost = toll_cost
        self.repair_cost = repair_cost
        self.salary_cost = salary_cost
        self.insurance_cost = insurance_cost
        self.other_cost = other_cost

    def calculate_total_cost(self):
        return (
            self.fuel_cost +
            self.toll_cost +
            self.repair_cost +
            self.salary_cost +
            self.insurance_cost +
            self.other_cost
        )
    
    # self.calculate_total_cost 是一个方法，不是普通变量。
    # 所以调用它时要加 ()，表示执行这个方法并返回总成本。）
    def calculate_profit(self):
        return self.revenue - self.calculate_total_cost()
    
    def calculate_profit_margin(self):
        if self.revenue == 0:
            return 0
        return self.calculate_profit() / self.revenue * 100
    
    def get_risk_level(self):
        profit_margin = self.calculate_profit_margin()

        if profit_margin >= 25:
            return 'Excellent'
        elif profit_margin >= 15:
            return 'Normal'
        elif profit_margin >= 5:
            return 'Warning'
        else:
            return 'High Risk'
        

    def get_risk_class(self):
        # 根据风险等级返回对应的 CSS class 名称。
        # 这个方法不负责计算风险，只负责告诉网页应该用什么颜色。
        risk_level = self.get_risk_level()

        if risk_level == 'Excellent':
            return 'risk-excellent'
        elif risk_level == 'Normal':
            return 'risk-normal'
        elif risk_level == 'Warning':
            return 'risk-warning'
        else:
            return 'risk-high'
        
    def get_profit_class(self):
        # 根据利润是正数还是负数，返回对应的 CSS class 名称
        # 这方法不负责计算利润，只负责告诉网页应该用什么颜色显示利润
        if self.calculate_profit() >= 0:
            return 'profit-positive'
        else:
            return 'profit-negative'

     
    def get_highest_cost_category(self):
        costs = {'Fuel Cost': self.fuel_cost,
                 'Toll Cost': self.toll_cost,
                 'Repair Cost': self.repair_cost,
                 'Salary Cost': self.salary_cost,
                 'Insurance Cost': self.insurance_cost,
                 'Other Cost': self.other_cost
                 }

        # 找出金额最高的成本类别。
        # costs 是一个字典，key 是成本名称，value 是对应金额。
        # key=costs.get 的意思是：让 Python 比较每个成本类别对应的金额，而不是比较成本名称本身。
        highest_category = max(costs, key=costs.get)
        return highest_category, costs[highest_category]
    
    def generate_suggestion(self):
        risk_level = self.get_risk_level()
        highest_category, highest_value = self.get_highest_cost_category()

        if risk_level == 'Excellent':
            suggestion = "This truck has a strong profit margin. The company should keep monitoring its cost structure."
        elif risk_level == 'Normal':
            suggestion = "This truck is performing at an acceptable level, but there is still room to improve cost efficiency."
        elif risk_level == 'Warning':
            suggestion = "This truck has a low profit margin. The company should review its revenue, route planning, and major cost items."
        else:
            suggestion = "This truck is at high risk. The company should carefully review pricing, operating costs, and vehicle usage."

        if highest_category == 'Fuel Cost':
            suggestion += " Fuel cost is the biggest pressure, so route efficiency and fuel usage should be checked."
        elif highest_category == 'Toll Cost':
            suggestion += " Toll cost is the biggest pressure, so alternative routes may need to be considered."
        elif highest_category == "Repair Cost":
            suggestion += " Repair cost is the biggest pressure, so vehicle maintenance should be reviewed."
        elif highest_category == "Salary Cost":
            suggestion += " Salary cost is the biggest pressure, so staff allocation and workload should be reviewed."
        elif highest_category == "Insurance Cost":
            suggestion += " Insurance cost is the biggest pressure, so insurance and parking arrangements should be reviewed."
        else:
            suggestion += " Other cost is the biggest pressure, so the company should check detailed expense records."

        return suggestion
    
    def get_summary_text(self):
        highest_category, highest_value = self.get_highest_cost_category()

        summary = (
            f"Truck ID: {self.truck_id} | "
            f"Driver: {self.driver} | "
            f"Route: {self.route} | "
            f"Revenue: ${self.revenue:,.2f} | "
            f"Total Cost: ${self.calculate_total_cost():,.2f} | "
            f"Profit: ${self.calculate_profit():,.2f} | "
            f"Profit Margin: {self.calculate_profit_margin():.2f}% | "
            f"Risk Level: {self.get_risk_level()} | "
            f"Main Cost Pressure: {highest_category} (${highest_value:,.2f})"
        )

        return summary
    

def create_sample_trucks():
    # 创建匿名化样本车辆数据。
    # 路线只展示到城市级别，不包含真实客户、车牌、仓库或具体地址。
    trucks = [
        Truck(
            'Truck 001',
            'Driver A',
            'Chongqing to Chengdu',
            68000,
            23000,
            8000,
            12000,
            11000,
            3000,
            2000
        ),
        Truck(
            'Truck 002',
            'Driver B',
            'Chongqing to Guiyang',
            52000,
            21000,
            7500,
            6500,
            10500,
            2800,
            1800
        ),
        Truck(
            'Truck 003',
            'Driver C',
            "Chongqing to Xi'an",
            75000,
            26000,
            9000,
            1800,
            11500,
            3200,
            2500
        ),
        Truck(
            'Truck 004',
            'Driver D',
            'Chongqing to Kunming',
            46000,
            18000,
            6800,
            7500,
            10000,
            2600,
            2200
        ),
        Truck(
            'Truck 005',
            'Driver E',
            'Chongqing to Wuhan',
            72000,
            24000,
            8500,
            5000,
            11200,
            3100,
            2300
        ),
        Truck(
            'Truck 006',
            'Driver F',
            'Chongqing to Guangzhou',
            88000,
            33000,
            12000,
            9000,
            12500,
            3600,
            3000
        ),
        Truck(
            'Truck 007',
            'Driver G',
            'Chongqing to Lanzhou',
            39000,
            17500,
            7200,
            6800,
            9800,
            2400,
            1800
        ),
        Truck(
            'Truck 008',
            'Driver H',
            'Chongqing to Shanghai',
            96000,
            35000,
            14500,
            7500,
            13000,
            4000,
            3500
        ),
        Truck(
            'Truck 009',
            'Driver I',
            'Chongqing to Nanning',
            61000,
            22500,
            7800,
            4200,
            10800,
            2900,
            2100
        ),
        Truck(
            'Truck 010',
            'Driver J',
            'Chongqing to Xiangyang',
            58000,
            20500,
            7600,
            9800,
            10600,
            2700,
            1900
        ),
        Truck(
            'Truck 011',
            'Driver K',
            'Chongqing to Changsha',
            69000,
            23800,
            8200,
            4300,
            11100,
            3000,
            2200
        ),
        Truck(
            'Truck 012',
            'Driver L',
            'Chongqing to Fuzhou',
            84000,
            31000,
            11800,
            6200,
            12200,
            3500,
            2800
        )
    ]

    return trucks


def save_analysis_history(truck):
    # 把分析结果保存到 fleet_history.txt 文件中。
    # "a" 代表 append，也就是追加内容，不会删除之前的记录。
    try:
        with open("fleet_history.txt", "a", encoding = "utf-8") as file:
            file.write(truck.get_summary_text() + "\n")
        return True
    
    except:
        return False
    

def save_truck_to_csv(truck):
    # 把新增truck的结构化数据保存到fleet_data.csv
    # 这个函数不会影响原来的file_history.txt功能
    try:
        file_exists = os.path.exists(CSV_FILE)

        with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # 如果csv文件不存在，就先写入表头
            if not file_exists:
                writer.writerow([
                    'truck_id',
                    'driver',
                    'route',
                    'revenue',
                    'fuel_cost',
                    'toll_cost',
                    'repair_cost',
                    'salary_cost',
                    'insurance_cost',
                    'other_cost',
                    'total_cost',
                    'profit',
                    'profit_margin',
                    'risk_level',
                    'highest_cost_category',
                    'highest_cost_value'
                ])

            highest_category, highest_value = truck.get_highest_cost_category()

            # 写入当前truck的一行数据
            writer.writerow([
                truck.truck_id,
                truck.driver,
                truck.route,
                truck.revenue,
                truck.fuel_cost,
                truck.toll_cost,
                truck.repair_cost,
                truck.salary_cost,
                truck.insurance_cost,
                truck.other_cost,
                truck.calculate_total_cost(),
                truck.calculate_profit(),
                truck.calculate_profit_margin(),
                truck.get_risk_level(),
                highest_category,
                highest_value
            ])

        return True
    
    except Exception as e:
        print("CSV save error:", e)
        return False


def read_trucks_from_csv():
    # 读取fleet_data.csv里的结构化车辆数据
    # 返回一个list，每一条记录是一个dictionary
    records = [] 

    try:
        with open(CSV_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                records.append(row)

        return records
    
    except FileNotFoundError:
        return []

    
def read_analysis_history():
    # 读取之前保存的分析记录，并把内容返回给网页。
    # Flask 网页版不能用 print() 显示历史，所以这里用 return。
    try:
        with open("fleet_history.txt", "r", encoding = "utf-8") as file:
            history = file.read()

            if history.strip() == "":
                return 'No analysis history found.'
            else:
                return history
            
    except FileNotFoundError:
        return 'No history file found yet. Please analyse a truck first.'
    

def compare_trucks(trucks):
    # 定义一个小函数，用来返回每辆车的利润率。
    # sorted() 会根据这个利润率来排序车辆。
    def get_margin(truck):
        return truck.calculate_profit_margin()

    sorted_trucks = sorted(
        trucks,
        key=get_margin,
        reverse=True
    )

    best_truck = sorted_trucks[0]
    highest_risk_truck = sorted_trucks[-1]

    return sorted_trucks, best_truck, highest_risk_truck

# ==== Fleet Dashboard ====
# 计算dashboard的统计数据
def get_dashboard_data():
    # 读取csv所有车辆记录
    records = read_trucks_from_csv()
    # 统计车辆数据
    truck_count = len(records)

    # 初始化统计变量
    total_revenue = 0
    total_cost = 0
    total_profit = 0
    total_margin = 0
    high_risk_count = 0
    best_truck = None
    worst_truck = None
    # 统计各类成本压力出现次数
    cost_pressure_count = {}
    
    # 遍历所有车辆记录
    for record in records:
        total_revenue += float(record["revenue"])
        total_cost += float(record["total_cost"])
        total_profit += float(record["profit"])
        total_margin += float(record["profit_margin"])
        
        # 统计高风险车辆数量
        if record["risk_level"] == "High Risk":
            high_risk_count += 1
        # 找出利润最高
        if best_truck is None or float(record["profit_margin"]) > float(best_truck["profit_margin"]):
            best_truck = record
        # 找出利润最低
        if worst_truck is None or float(record["profit_margin"]) < float(worst_truck["profit_margin"]):
            worst_truck = record

        # 统计主要成本压力类别
        category = record["highest_cost_category"]

        if category not in cost_pressure_count:
            cost_pressure_count[category] = 1
        else:
            cost_pressure_count[category] += 1

    # 计算平均利润率，防止为0的情况
    if truck_count == 0:
        average_profit_margin = 0
    else:
        average_profit_margin = total_margin / truck_count
    
    # 找出出现次数最多的成本压力
    if len(cost_pressure_count) == 0:
        most_common_cost_pressure = "No data"
    else:
        most_common_cost_pressure = max(cost_pressure_count, key=cost_pressure_count.get)

    # 返回dashboard需要的数据
    return {
        "truck_count": truck_count,
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "total_profit": total_profit,
        "average_profit_margin": average_profit_margin,
        "high_risk_count": high_risk_count,
        "best_truck": best_truck,
        "worst_truck": worst_truck,
        "most_common_cost_pressure": most_common_cost_pressure
    }


# =========================
# V4 Analytics: Charts
# =========================

# 收入图表
def generate_revenue_chart():
    import csv
    import os
    import matplotlib
    # 不要打开图形窗口，只在后台生成图片文件
    matplotlib.use("Agg")
    
    import matplotlib.pyplot as plt

    truck_ids = []
    revenues = []

    # 读取CSV里的车辆收入数据
    with open("fleet_data.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            truck_ids.append(row["truck_id"])
            revenues.append(float(row["revenue"]))

        #  确保charts文件夹存在
        os.makedirs("static/charts", exist_ok=True)

        # 生成revenue柱状图
        plt.figure(figsize=(8, 5))
        plt.bar(truck_ids, revenues)

        plt.title("Revenue by Truck")
        plt.xlabel("Truck ID")
        plt.ylabel("Revenue")

        # 旋转Truck ID, 避免文字重叠
        plt.xticks(rotation=30)
        plt.tight_layout()

        # 保存图表图片
        plt.savefig("static/charts/revenue_chart.png")
        plt.close()

# 利润图表
def generate_profit_chart():
    import csv
    import os
    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    truck_ids = []
    profits = []

    # 读取csv里的车辆利润数据
    with open("fleet_data.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            truck_ids.append(row["truck_id"])
            profits.append(float(row["profit"]))

        # 确保charts文件存在
        os.makedirs("static/charts", exist_ok=True)

        # 生成利润柱状图表
        plt.figure(figsize=(8, 5))
        bars = plt.bar(truck_ids, profits)

        plt.title("Profit by Truck")
        plt.xlabel("Truck ID")
        plt.xlabel("Profit")

        # 在柱状图上显示利润数值和亏损的
        for bar, profit in zip(bars, profits):
            x_position = bar.get_x() + bar.get_width() / 2

            if profit >= 0:
                y_position = profit
                verticle_align = "bottom"
            else:
                y_position = profit
                verticle_align = "top"

            plt.text(
                x_position,
                y_position,
                f"{profit:.0f}",
                ha="center",
                va=verticle_align
            )

        # 旋转truck ID 避免文字重叠
        plt.xticks(rotation=30)
        plt.tight_layout()

        # 保存图表图片
        plt.savefig("static/charts/profit_chart.png")
        plt.close()


# Risk Distribution Chart
def generate_risk_chart():
    import csv
    import os
    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    # 固定显示四种风险等级
    risk_counts = {
        "Excellent": 0,
        "Normal": 0,
        "Warning": 0,
        "High Risk": 0
    }

    # 读取 CSV 里的风险等级数据
    with open("fleet_data.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            risk_level = row["risk_level"]

            if risk_level in risk_counts:
                risk_counts[risk_level] += 1

    # 确保 charts 文件夹存在
    os.makedirs("static/charts", exist_ok=True)

    # 生成风险等级分布图
    plt.figure(figsize=(8, 5))
    bars = plt.bar(risk_counts.keys(), risk_counts.values())

    plt.title("Risk Level Distribution")
    plt.xlabel("Risk Level")
    plt.ylabel("Number of Trucks")

    # 在柱状图上显示车辆数量
    for bar in bars:
        height = bar.get_height()
        x_position = bar.get_x() + bar.get_width() / 2

        plt.text(
            x_position,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom"
        )

    plt.xticks(rotation=30)
    plt.tight_layout()

    # 保存图表图片
    plt.savefig("static/charts/risk_chart.png")
    plt.close()

# Cost Pressure Distribution Chart

def generate_cost_pressure_chart():
    import csv
    import os
    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    cost_pressure_counts = {}

    # 读取 CSV 里的主要成本压力数据
    with open("fleet_data.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cost_pressure = row["highest_cost_category"]

            if cost_pressure in cost_pressure_counts:
                cost_pressure_counts[cost_pressure] += 1
            else:
                cost_pressure_counts[cost_pressure] = 1

    # 确保 charts 文件夹存在
    os.makedirs("static/charts", exist_ok=True)

    # 生成成本压力分布图
    plt.figure(figsize=(8, 5))
    bars = plt.bar(cost_pressure_counts.keys(), cost_pressure_counts.values())

    plt.title("Cost Pressure Distribution")
    plt.xlabel("Main Cost Pressure")
    plt.ylabel("Number of Trucks")

    # 在柱状图上显示车辆数量
    for bar in bars:
        height = bar.get_height()
        x_position = bar.get_x() + bar.get_width() / 2

        plt.text(
            x_position,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom"
        )

    plt.xticks(rotation=30)
    plt.tight_layout()

    # 保存图表图片
    plt.savefig("static/charts/cost_pressure_chart.png")
    plt.close()


# Analytics Summary Data
def get_analytics_summary():
    import csv

    trucks = []
    total_revenue = 0
    total_profit = 0
    total_margin = 0
    loss_making_count = 0

    # 读取CSV里车辆数据
    with open("fleet_data.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            revenue = float(row["revenue"])
            profit = float(row["profit"])
            profit_margin = float(row["profit_margin"])

            trucks.append(row)
            total_revenue += revenue
            total_profit += profit
            total_margin += profit_margin

            if profit < 0:
                loss_making_count += 1

    truck_count = len(trucks)

    if truck_count > 0:
        average_profit_margin = total_margin / truck_count
    else:
        average_profit_margin = 0

    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "average_profit_margin": average_profit_margin,
        "loss_making_count": loss_making_count
    }


# Loss-making Truck Data

def get_loss_making_trucks():
    import csv
    loss_making_trucks = []
    # 读取CSV 筛选亏损车辆
    with open("fleet_data.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
   
        for row in reader:
            profit = float(row["profit"])
            # 只保留利润为负的车辆
            if profit < 0:
                loss_making_trucks.append({
                    "truck_id": row["truck_id"],
                    "revenue": float(row["revenue"]),
                    "total_cost": float(row["total_cost"]),
                    "profit": profit,
                    "risk_level": row["risk_level"],
                    "highest_cost_category": row["highest_cost_category"]
                })

    return loss_making_trucks



def get_ai_response(question):
    # 这个功能不是真正的大模型 AI。
    # 它是一个 keyword-based assistant，也就是基于关键词的简单问答助手。
    # Flask 网页版中，用户的问题来自网页表单，所以这里用 return 返回回答，而不是 print()。

    question = question.lower().strip()

    if question == "":
        return (
            "Please enter a logistics question first. "
            "FleetMind is smart, but it still needs something to work with."
        )

    if "profit" in question or "margin" in question:
        return (
            "Profit is usually affected by revenue and operating costs. "
            "If a truck has low profit, the company should check whether the route price is too low, "
            "or whether fuel, toll, repair, and salary costs are eating the margin. "
            "In simple words: the truck may be working hard, but the money is running away quietly."
        )

    elif "fuel" in question or "gas" in question or "diesel" in question:
        return (
            "High fuel cost may be caused by long routes, traffic congestion, driving habits, "
            "heavy loads, or low vehicle energy efficiency. "
            "The company can compare route distance, fuel usage, and vehicle type. "
            "Fuel cost is often the loudest passenger in a logistics business — it never sits quietly."
        )

    elif "repair" in question or "maintenance" in question:
        return (
            "High repair cost may indicate vehicle ageing, poor maintenance planning, "
            "or frequent heavy-load trips. "
            "If repair cost keeps increasing, the company should check whether this truck needs preventive maintenance "
            "or whether it is slowly becoming a 'money-eating machine'."
        )

    elif "toll" in question:
        return (
            "High toll cost is usually related to route choice. "
            "The company can compare different routes before dispatching trucks, especially for long-distance trips. "
            "Sometimes the shortest route is not the cheapest route — highways can be very good at collecting money."
        )

    elif "risk" in question:
        return (
            "Vehicle risk level is mainly based on profit margin. "
            "A lower profit margin means the truck has less room to absorb unexpected costs. "
            "If a truck is marked as High Risk, it does not mean the truck is bad, "
            "but it means the company should look at it before it turns into a bigger problem."
        )

    elif "salary" in question or "staff" in question or "driver" in question:
        return (
            "Salary cost is usually more stable than fuel or repair cost, "
            "but the company should still check whether staff allocation matches the truck's actual workload. "
            "If one truck has low revenue but high salary cost, the business may need better dispatch planning. "
            "Hard work is important, but the spreadsheet also wants to be respected."
        )

    elif "route" in question or "distance" in question:
        return (
            "Route performance depends on distance, road conditions, toll fees, delivery time, and vehicle matching. "
            "A good route is not only about getting from A to B, but about getting there with reasonable cost and profit. "
            "In logistics, the road may be straight, but the business logic is usually not."
        )

    elif "insurance" in question:
        return (
            "Insurance cost is usually a fixed or semi-fixed cost, but it still affects total profitability. "
            "If insurance cost becomes a major pressure, the company may need to review vehicle usage, parking arrangements, "
            "risk exposure, and insurance plans. "
            "Insurance is boring until something happens — then suddenly it becomes very important."
        )

    elif "cost" in question:
        return (
            "Cost pressure can come from fuel, tolls, repairs, salary, insurance, or other expenses. "
            "FleetMind checks the biggest cost category to help managers quickly find where the pressure comes from. "
            "The goal is not to blame one cost item, but to find the first place worth investigating."
        )

    else:
        return (
            "Sorry, I can only answer basic logistics questions about profit, margin, fuel, repair, toll, salary, route, insurance, cost, and risk. "
            "Try asking something like: 'Why is fuel cost high?' or 'How can I reduce risk?' "
            "FleetMind is still a student project, not the logistics version of Iron Man's Jarvis — at least not yet."
        )
    
    

    





