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
    
    

    





