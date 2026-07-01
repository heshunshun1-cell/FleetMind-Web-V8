# 从 database.py 中导入数据库查询函数
from database import (
    get_high_risk_trucks_from_db,
    get_high_delay_trips_from_db,
    get_loss_making_trips_from_db,
    get_high_cost_per_km_trips_from_db,
    get_route_performance_from_db
)


def format_money(value):
    # 把金额格式化成 12,345.67 这种形式
    return f"{float(value):,.2f}"


def format_number(value):
    # 把普通数字格式化成两位小数
    return f"{float(value):.2f}"


def get_database_context(question):
    """
    根据用户问题，从 SQLite 数据库中检索相关运营数据。

    这个函数的作用是：
    1. 先判断用户问题在问 truck、trip 还是 route
    2. 再判断问题和 risk、delay、loss、cost 哪类业务有关
    3. 最后调用对应的数据库查询函数
    """

    # 把问题转成小写，方便做关键词判断
    question_lower = question.lower()

    # 用字符串保存数据库检索结果，方便直接显示在页面上
    database_context = ""

    # 判断用户问题主要是在问 truck、trip 还是 route
    is_truck_question = "truck" in question_lower or "trucks" in question_lower
    is_trip_question = "trip" in question_lower or "trips" in question_lower
    is_route_question = "route" in question_lower or "routes" in question_lower

    # 判断问题是否和延误有关
    is_delay_question = (
        "delay" in question_lower
        or "delays" in question_lower
        or "late" in question_lower
        or "serious delay" in question_lower
    )

    # 判断问题是否在问路线层面的延误
    # 例如：which routes have serious delay problems
    is_route_delay_question = is_route_question and is_delay_question

    # 如果问题在问高风险车辆，就查询 trucks 表
    if "high risk" in question_lower and is_truck_question:
        high_risk_trucks = get_high_risk_trucks_from_db()

        if len(high_risk_trucks) == 0:
            database_context += "Database Result:\n"
            database_context += "No high risk trucks were found in the current database.\n"

        else:
            database_context += "Database Result - High Risk Trucks:\n\n"

            for truck in high_risk_trucks:
                database_context += f"Truck ID: {truck['truck_id']}\n"
                database_context += f"Driver: {truck['driver']}\n"
                database_context += f"Route: {truck['route']}\n"
                database_context += f"Revenue: {format_money(truck['revenue'])}\n"
                database_context += f"Total Cost: {format_money(truck['total_cost'])}\n"
                database_context += f"Profit: {format_money(truck['profit'])}\n"
                database_context += f"Profit Margin: {format_number(truck['profit_margin'])}%\n"
                database_context += f"Risk Level: {truck['risk_level']}\n"
                database_context += f"Main Cost Pressure: {truck['highest_cost_category']}\n\n"

    # 如果问题在问延误，并且不是路线层面问题，就查询具体 high delay trips
    if (not is_route_question) and is_delay_question:
        high_delay_trips = get_high_delay_trips_from_db()

        if len(high_delay_trips) == 0:
            database_context += "Database Result:\n"
            database_context += "No high delay trips were found in the current database.\n"

        else:
            database_context += "Database Result - High Delay Trips:\n\n"

            for trip in high_delay_trips:
                database_context += f"Trip ID: {trip['trip_id']}\n"
                database_context += f"Truck ID: {trip['truck_id']}\n"
                database_context += f"Driver: {trip['driver']}\n"
                database_context += f"Route: {trip['route']}\n"
                database_context += f"Distance: {trip['distance']} km\n"
                database_context += f"Revenue: {format_money(trip['revenue'])}\n"
                database_context += f"Total Cost: {format_money(trip['total_cost'])}\n"
                database_context += f"Profit: {format_money(trip['profit'])}\n"
                database_context += f"Profit Margin: {format_number(trip['profit_margin'])}%\n"
                database_context += f"Cost Per Km: {format_number(trip['cost_per_km'])}\n"
                database_context += f"Delay Hours: {format_number(trip['delay_hours'])}\n"
                database_context += f"Risk Level: {trip['risk_level']}\n"
                database_context += f"Trip Date: {trip['trip_date']}\n\n"

    # 如果问题在问亏损，并且不是路线层面问题，就查询亏损 trip
    if (not is_route_question) and (
        "loss" in question_lower
        or "unprofitable" in question_lower
        or "losing money" in question_lower
        or "negative profit" in question_lower
    ):
        loss_making_trips = get_loss_making_trips_from_db()

        if len(loss_making_trips) == 0:
            database_context += "Database Result:\n"
            database_context += "No loss-making trips were found in the current database.\n"

        else:
            database_context += "Database Result - Loss-Making Trips:\n\n"

            for trip in loss_making_trips:
                database_context += f"Trip ID: {trip['trip_id']}\n"
                database_context += f"Truck ID: {trip['truck_id']}\n"
                database_context += f"Driver: {trip['driver']}\n"
                database_context += f"Route: {trip['route']}\n"
                database_context += f"Distance: {trip['distance']} km\n"
                database_context += f"Revenue: {format_money(trip['revenue'])}\n"
                database_context += f"Total Cost: {format_money(trip['total_cost'])}\n"
                database_context += f"Profit: {format_money(trip['profit'])}\n"
                database_context += f"Profit Margin: {format_number(trip['profit_margin'])}%\n"
                database_context += f"Cost Per Km: {format_number(trip['cost_per_km'])}\n"
                database_context += f"Delay Hours: {format_number(trip['delay_hours'])}\n"
                database_context += f"Risk Level: {trip['risk_level']}\n"
                database_context += f"Trip Date: {trip['trip_date']}\n\n"

    # 如果问题在问成本，并且不是路线层面问题，就查询高每公里成本 trip
    if (not is_route_question) and (
        "cost per km" in question_lower
        or "cost per kilometre" in question_lower
        or "cost per kilometer" in question_lower
        or "expensive" in question_lower
        or "costly" in question_lower
        or "high cost" in question_lower
    ):
        high_cost_trips = get_high_cost_per_km_trips_from_db()

        if len(high_cost_trips) == 0:
            database_context += "Database Result:\n"
            database_context += "No trip records were found for cost per km analysis.\n"

        else:
            database_context += "Database Result - High Cost Per Km Trips:\n\n"

            for trip in high_cost_trips:
                database_context += f"Trip ID: {trip['trip_id']}\n"
                database_context += f"Truck ID: {trip['truck_id']}\n"
                database_context += f"Driver: {trip['driver']}\n"
                database_context += f"Route: {trip['route']}\n"
                database_context += f"Distance: {trip['distance']} km\n"
                database_context += f"Revenue: {format_money(trip['revenue'])}\n"
                database_context += f"Total Cost: {format_money(trip['total_cost'])}\n"
                database_context += f"Profit: {format_money(trip['profit'])}\n"
                database_context += f"Profit Margin: {format_number(trip['profit_margin'])}%\n"
                database_context += f"Cost Per Km: {format_number(trip['cost_per_km'])}\n"
                database_context += f"Delay Hours: {format_number(trip['delay_hours'])}\n"
                database_context += f"Risk Level: {trip['risk_level']}\n"
                database_context += f"Trip Date: {trip['trip_date']}\n\n"

    # 如果问题在问路线层面，就查询 route summary
    # 包括：路线表现、路线延误、路线成本、路线利润等问题
    if is_route_question and (
        is_route_delay_question
        or "route performance" in question_lower
        or "routes perform" in question_lower
        or "route summary" in question_lower
        or "average delay" in question_lower
        or "average cost" in question_lower
        or "expensive" in question_lower
        or "costly" in question_lower
        or "high cost" in question_lower
        or "low profit" in question_lower
        or "unprofitable" in question_lower
    ):
        route_performance = get_route_performance_from_db()

        if len(route_performance) == 0:
            database_context += "Database Result:\n"
            database_context += "No route performance records were found in the current database.\n"

        else:
            database_context += "Database Result - Route Performance Summary:\n\n"

            for route in route_performance:
                database_context += f"Route: {route['route']}\n"
                database_context += f"Total Trips: {route['total_trips']}\n"
                database_context += f"Total Distance: {format_number(route['total_distance'])} km\n"
                database_context += f"Total Revenue: {format_money(route['total_revenue'])}\n"
                database_context += f"Total Cost: {format_money(route['total_cost'])}\n"
                database_context += f"Total Profit: {format_money(route['total_profit'])}\n"
                database_context += f"Average Profit Margin: {format_number(route['average_profit_margin'])}%\n"
                database_context += f"Average Cost Per Km: {format_number(route['average_cost_per_km'])}\n"
                database_context += f"Average Delay Hours: {format_number(route['average_delay_hours'])}\n\n"

    return database_context


# 单独运行本文件时，用于测试数据库检索效果
if __name__ == "__main__":
    test_question = "which routes have serious delay problems"
    result = get_database_context(test_question)

    print(result)