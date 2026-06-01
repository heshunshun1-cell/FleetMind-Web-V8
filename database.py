import sqlite3

# 数据库文件名
DB_NAME = "fleetmind.db"

def get_db_connection():
    """连接 SQLite 数据库"""
    # 连接数据库；若文件不存在，SQLite会自动创建
    conn = sqlite3.connect(DB_NAME)

    # 让查询结果可以像字典一样读取，例如 row["truck_id"]
    conn.row_factory = sqlite3.Row

    return conn

def read_trucks_from_db():
    """从数据库读取所有车辆记录"""

    # 连接数据库
    conn = get_db_connection()

    # 查询 trucks 表里的所有数据
    trucks = conn.execute("SELECT * FROM trucks").fetchall()

    # 关闭数据库连接
    conn.close()

    return trucks

def get_dashboard_data_from_db():
    """从 SQLite 数据库计算 Dashboard 页面需要的数据"""
    
    # 连接数据库
    conn = get_db_connection()

    # 读取trucks表里的所有车辆记录
    records = conn.execute("SELECT * FROM trucks").fetchall()

    #关闭数据库连接
    conn.close()

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

    # 统计主要成本压力出现次数
    cost_pressure_count = {}

    # 便利数据库里的每一条车辆记录
    for record in records:
        total_revenue += float(record["revenue"])
        total_cost += float(record["total_cost"])
        total_profit += float(record["profit"])
        total_margin += float(record["profit_margin"])
        
        # 统计高风险车辆数量
        if record["risk_level"] == "High Risk":
            high_risk_count += 1
        # 找出利润最高的车辆
        if best_truck is None or float(record["profit_margin"]) > float(best_truck["profit_margin"]):
            best_truck = record
        # 找出利润率最低的车辆
        if worst_truck is None or float(record["profit_margin"]) < float(worst_truck["profit_margin"]):
            worst_truck = record
        # 统计主要成本压力
        category = record["highest_cost_category"]

        if category not in cost_pressure_count:
            cost_pressure_count[category] = 1
        else:
            cost_pressure_count[category] += 1

    # 计算平均利润率
    if truck_count == 0:
        average_profit_margin = 0
    else:
        average_profit_margin = total_margin / truck_count

    # 找出最常见的成本压力
    if len(cost_pressure_count) == 0:
        most_common_cost_pressure = "No data"
    else:
        most_common_cost_pressure = max(cost_pressure_count, key=cost_pressure_count.get)

    # 返回dashboard页面需要的数据
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


def get_analytics_summary_from_db():
    """从 SQLite 数据库计算 Analytics 页面汇总数据"""

    # 连接数据库
    conn = get_db_connection()

    # 读取 trucks 表里的所有车辆记录
    records = conn.execute("SELECT * FROM trucks").fetchall()

    # 关闭数据库连接
    conn.close()

    # 初始化统计变量
    total_revenue = 0
    total_profit = 0
    total_margin = 0
    loss_making_count = 0

    # 遍历每一条车辆记录
    for record in records:
        revenue = float(record["revenue"])
        profit = float(record["profit"])
        profit_margin = float(record["profit_margin"])

        total_revenue += revenue
        total_profit += profit
        total_margin += profit_margin

        # 统计亏损车辆数量
        if profit < 0:
            loss_making_count += 1

    # 统计车辆数量
    truck_count = len(records)

    # 计算平均利润率
    if truck_count > 0:
        average_profit_margin = total_margin / truck_count
    else:
        average_profit_margin = 0

    # 返回 Analytics 页面需要的汇总数据
    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "average_profit_margin": average_profit_margin,
        "loss_making_count": loss_making_count
    }


def get_loss_making_trucks_from_db():
    """从 SQLite 数据库读取亏损车辆数据"""

    # 连接数据库
    conn = get_db_connection()

    # 查询利润小于 0 的车辆
    loss_making_trucks = conn.execute("""
        SELECT
            truck_id,
            revenue,
            total_cost,
            profit,
            risk_level,
            highest_cost_category
        FROM trucks
        WHERE profit < 0
    """).fetchall()

    # 关闭数据库连接
    conn.close()

    return loss_making_trucks


def generate_revenue_chart_from_db():
    """从 SQLite 数据库生成 Revenue by Truck 图表"""

    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # 连接数据库
    conn = get_db_connection()

    # 查询车辆收入数据
    records = conn.execute("""
        SELECT truck_id, revenue
        FROM trucks
    """).fetchall()

    conn.close()

    truck_ids = []
    revenues = []

    for record in records:
        truck_ids.append(record["truck_id"])
        revenues.append(float(record["revenue"]))

    # 确保图表文件夹存在
    os.makedirs("static/charts", exist_ok=True)

    # 生成图表
    plt.figure(figsize=(8, 5))
    plt.bar(truck_ids, revenues)

    plt.title("Revenue by Truck")
    plt.xlabel("Truck ID")
    plt.ylabel("Revenue")

    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig("static/charts/revenue_chart.png")
    plt.close()


def generate_profit_chart_from_db():
    """从 SQLite 数据库生成 Profit by Truck 图表"""

    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # 连接数据库
    conn = get_db_connection()

    # 查询车辆利润数据
    records = conn.execute("""
        SELECT truck_id, profit
        FROM trucks
    """).fetchall()

    conn.close()

    truck_ids = []
    profits = []

    for record in records:
        truck_ids.append(record["truck_id"])
        profits.append(float(record["profit"]))

    # 确保图表文件夹存在
    os.makedirs("static/charts", exist_ok=True)

    # 生成图表
    plt.figure(figsize=(8, 5))
    bars = plt.bar(truck_ids, profits)

    plt.title("Profit by Truck")
    plt.xlabel("Truck ID")
    plt.ylabel("Profit")

    # 在柱状图上显示利润数值
    for bar, profit in zip(bars, profits):
        x_position = bar.get_x() + bar.get_width() / 2

        if profit >= 0:
            y_position = profit
            vertical_align = "bottom"
        else:
            y_position = profit
            vertical_align = "top"

        plt.text(
            x_position,
            y_position,
            f"{profit:.0f}",
            ha="center",
            va=vertical_align
        )

    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig("static/charts/profit_chart.png")
    plt.close()


def generate_risk_chart_from_db():
    """从 SQLite 数据库生成 Risk Level Distribution 图表"""

    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # 连接数据库
    conn = get_db_connection()

    # 查询所有风险等级
    records = conn.execute("""
        SELECT risk_level
        FROM trucks
    """).fetchall()

    conn.close()

    # 固定四种风险等级
    risk_counts = {
        "Excellent": 0,
        "Normal": 0,
        "Warning": 0,
        "High Risk": 0
    }

    for record in records:
        risk_level = record["risk_level"]

        if risk_level in risk_counts:
            risk_counts[risk_level] += 1

    # 确保图表文件夹存在
    os.makedirs("static/charts", exist_ok=True)

    # 生成图表
    plt.figure(figsize=(8, 5))
    bars = plt.bar(risk_counts.keys(), risk_counts.values())

    plt.title("Risk Level Distribution")
    plt.xlabel("Risk Level")
    plt.ylabel("Number of Trucks")

    # 在柱状图上显示数量
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

    plt.savefig("static/charts/risk_chart.png")
    plt.close()


def generate_cost_pressure_chart_from_db():
    """从 SQLite 数据库生成 Cost Pressure Distribution 图表"""

    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # 连接数据库
    conn = get_db_connection()

    # 查询主要成本压力类别
    records = conn.execute("""
        SELECT highest_cost_category
        FROM trucks
    """).fetchall()

    conn.close()

    cost_pressure_counts = {}

    for record in records:
        cost_pressure = record["highest_cost_category"]

        if cost_pressure in cost_pressure_counts:
            cost_pressure_counts[cost_pressure] += 1
        else:
            cost_pressure_counts[cost_pressure] = 1

    # 确保图表文件夹存在
    os.makedirs("static/charts", exist_ok=True)

    # 生成图表
    plt.figure(figsize=(8, 5))
    bars = plt.bar(cost_pressure_counts.keys(), cost_pressure_counts.values())

    plt.title("Cost Pressure Distribution")
    plt.xlabel("Main Cost Pressure")
    plt.ylabel("Number of Trucks")

    # 在柱状图上显示数量
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

    plt.savefig("static/charts/cost_pressure_chart.png")
    plt.close()


def generate_insights_from_db():
    """从 SQLite 数据库生成运营建议"""

    # 连接数据库
    conn = get_db_connection()
    # 读取所有车辆数据
    records = conn.execute("SELECT * FROM trucks").fetchall()
    # 关闭数据库连接
    conn.close()
    # 用来存放所有建议
    insights = []

    # 如果没有数据
    if len(records) == 0:
        insights.append("No truck records found in the database.")
        return insights
    
    # 统计最常见的成本压力
    cost_pressure_count = {}

    # 找出最佳和最差
    best_truck = None
    worst_truck = None
    # 遍历每一辆车
    for record in records:
        truck_id = record["truck_id"]
        profit = float(record["profit"])
        profit_margin = float(record["profit_margin"])
        risk_level = record["risk_level"]
        highest_cost_category = record["highest_cost_category"]

        # 统计成本压力
        if highest_cost_category not in cost_pressure_count:
            cost_pressure_count[highest_cost_category] = 1
        else:
            cost_pressure_count[highest_cost_category] += 1

        # 亏损车辆建议
        if profit < 0:
            insights.append(
                f"{truck_id} is currently loss-making. Please review its pricing, route planning, and operating costs."
            )

        # 高风险车辆建议
        if risk_level == "High Risk":
            insights.append(
                f"{truck_id} is marked as High Risk. The company should carefully check its profit margin and main cost pressure."
            )

        # 低利润车辆建议
        if profit_margin < 5:
            insights.append(
                f"{truck_id} has a very low profit margin. It may need better cost control or route adjustment."
            )

        #找最佳和最差车辆
        if best_truck is None or profit_margin > float(best_truck["profit_margin"]):
            best_truck = record
        
        if worst_truck is None or profit_margin < float(worst_truck["profit_margin"]):
            worst_truck = record

    # 最常见成本压力建议
    if len(cost_pressure_count) > 0:
        most_common_cost_pressure = max(cost_pressure_count, key=cost_pressure_count.get)
        insights.append(
            f"{most_common_cost_pressure} is the most common cost pressure across the fleet. It should be reviewed first."
        )

    # 最佳和最差车辆建议
    if best_truck is not None:
        insights.append(
            f"{best_truck['truck_id']} has the strongest profit margin and can be used as a benchmark for other trucks."
        )

    if worst_truck is not None:
        insights.append(
            f"{worst_truck['truck_id']} has the lowest profit margin. This truck should be reviewed as a priority."
        )

    return insights

def save_truck_to_db(truck):
    """把新车辆数据保存到 SQLite 数据库"""

    try:
        # 连接数据库
        conn = get_db_connection()

        # 找出主要成本压力
        highest_category, highest_value = truck.get_highest_cost_category()

        # 插入一条新车辆记录
        conn.execute("""
            INSERT INTO trucks (
                truck_id,
                driver,
                route,
                revenue,
                fuel_cost,
                toll_cost,
                repair_cost,
                salary_cost,
                insurance_cost,
                other_cost,
                total_cost,
                profit,
                profit_margin,
                risk_level,
                highest_cost_category,
                highest_cost_value
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
        ))

        # 保存修改并关闭连接
        conn.commit()
        conn.close()

        return True

    except Exception as e:
        print("Database save error:", e)
        return False
    

def read_trips_from_db():
    """从 SQLite 数据库读取所有运输任务记录"""

    # 连接数据库
    conn = get_db_connection()

    # 查询 trips 表，并按日期从新到旧排序
    trips = conn.execute("""
        SELECT *
        FROM trips
        ORDER BY trip_date DESC
    """).fetchall()

    # 关闭数据库连接
    conn.close()

    return trips

def get_trip_summary_from_db():
    """从 SQLite 数据库计算 trip summary 数据"""

    # 连接数据库
    conn = get_db_connection()

    # 读取所有trip记录
    trips = conn.execute("SELECT * FROM trips").fetchall()

    # 关闭数据库连接
    conn.close()

    # 初始化统计变量
    total_trips = len(trips)
    total_revenue = 0
    total_profit = 0
    total_cost_per_km = 0
    high_delay_count = 0
    loss_making_count = 0

    # 遍历每一条 trip
    for trip in trips:
        total_revenue += float(trip["revenue"])
        total_profit += float(trip["profit"])
        total_cost_per_km += float(trip["cost_per_km"])

        # 延误超过24小时，认为是高延误
        if float(trip["delay_hours"]) >= 24:
            high_delay_count += 1

        # 利润小于0，认为是亏损trip
        if float(trip["profit"]) < 0:
            loss_making_count += 1

    # 计算平均每公里成本
    if total_trips == 0:
        average_cost_per_km = 0
    else:
        average_cost_per_km = total_cost_per_km / total_trips

    # 返回trips页面需要的summary数据
    return {
        "total_trips": total_trips,
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "average_cost_per_km": average_cost_per_km,
        "high_delay_count": high_delay_count,
        "loss_making_count": loss_making_count
    }


def generate_trip_insights_from_db():
    """从 SQLite 数据库生成 trip-level 运营建议"""

    # 连接数据库
    conn = get_db_connection()

    # 读取所有 trip 记录
    trips = conn.execute("SELECT * FROM trips").fetchall()

    # 关闭数据库连接
    conn.close()

    # 用来存放 trip insights
    insights = []

    # 如果没有 trip 数据
    if len(trips) == 0:
        insights.append("No trip records found in the database.")
        return insights

    # 初始化分析对象
    highest_delay_trip = None
    highest_cost_per_km_trip = None
    most_profitable_trip = None
    lowest_margin_trip = None

    # 遍历每一条 trip
    for trip in trips:
        delay_hours = float(trip["delay_hours"])
        cost_per_km = float(trip["cost_per_km"])
        profit = float(trip["profit"])
        profit_margin = float(trip["profit_margin"])

        # 找出延误最高的 trip
        if highest_delay_trip is None or delay_hours > float(highest_delay_trip["delay_hours"]):
            highest_delay_trip = trip

        # 找出每公里成本最高的 trip
        if highest_cost_per_km_trip is None or cost_per_km > float(highest_cost_per_km_trip["cost_per_km"]):
            highest_cost_per_km_trip = trip

        # 找出利润最高的 trip
        if most_profitable_trip is None or profit > float(most_profitable_trip["profit"]):
            most_profitable_trip = trip

        # 找出利润率最低的 trip
        if lowest_margin_trip is None or profit_margin < float(lowest_margin_trip["profit_margin"]):
            lowest_margin_trip = trip

        # 单独提示高延误 trip
        if delay_hours >= 24:
            insights.append(
                f"{trip['trip_id']} has a high delay of {delay_hours:.1f} hours on the route {trip['route']}. This trip should be reviewed."
            )

        # 单独提示高风险 trip
        if trip["risk_level"] == "High Risk":
            insights.append(
                f"{trip['trip_id']} is marked as High Risk. The company should review its pricing and cost structure."
            )

        # 单独提示亏损 trip
        if profit < 0:
            insights.append(
                f"{trip['trip_id']} is loss-making. Please check revenue, route planning, and operating costs."
            )

    # 总结：最高延误
    if highest_delay_trip is not None:
        insights.append(
            f"{highest_delay_trip['trip_id']} has the highest delay in the current trip records."
        )

    # 总结：最高每公里成本
    if highest_cost_per_km_trip is not None:
        insights.append(
            f"{highest_cost_per_km_trip['trip_id']} has the highest cost per kilometre at ${float(highest_cost_per_km_trip['cost_per_km']):.2f}/km."
        )

    # 总结：最高利润
    if most_profitable_trip is not None:
        insights.append(
            f"{most_profitable_trip['trip_id']} is the most profitable trip with a profit of ${float(most_profitable_trip['profit']):,.2f}."
        )

    # 总结：最低利润率
    if lowest_margin_trip is not None:
        insights.append(
            f"{lowest_margin_trip['trip_id']} has the lowest profit margin at {float(lowest_margin_trip['profit_margin']):.2f}%."
        )

    return insights


