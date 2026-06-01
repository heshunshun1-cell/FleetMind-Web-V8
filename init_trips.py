from database import get_db_connection


def create_trips_table():
    """创建 trips 表，用来保存每一趟运输任务"""

    # 连接数据库
    conn = get_db_connection()

    # 删除旧 trips 表，避免字段不一致
    # 注意：这里只影响 trips 表，不会影响 trucks 表
    conn.execute("DROP TABLE IF EXISTS trips")

    # 创建新的 trips 表
    conn.execute("""
    CREATE TABLE trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_id TEXT,
        truck_id TEXT,
        driver TEXT,
        route TEXT,
        distance REAL,
        revenue REAL,
        fuel_cost REAL,
        toll_cost REAL,
        maintenance_cost REAL,
        driver_cost REAL,
        delay_hours REAL,
        trip_date TEXT,
        total_cost REAL,
        profit REAL,
        profit_margin REAL,
        cost_per_km REAL,
        risk_level TEXT
    )
    """)

    # 保存并关闭数据库
    conn.commit()
    conn.close()


def import_sample_trips():
    """导入 sample trip 数据"""

    # 连接数据库
    conn = get_db_connection()

    # 样本运输任务数据
    # 格式：trip_id, truck_id, driver, route, distance, revenue,
    # fuel_cost, toll_cost, maintenance_cost, driver_cost, delay_hours, trip_date
    sample_trips = [
        (
            "TRIP001",
            "Truck 013",
            "Shunshun",
            "Chongqing to Davis",
            10800,
            260000,
            82000,
            18000,
            16000,
            36000,
            25.0,
            "2026-05-01"
        ),
        (
            "TRIP002",
            "Truck 014",
            "Aijia",
            "Chongqing to Sydney",
            8500,
            235000,
            76000,
            15000,
            14000,
            33000,
            7.0,
            "2026-05-03"
        ),
        (
            "TRIP003",
            "Truck 015",
            "Lau",
            "Chongqing to Shenyang",
            2450,
            62000,
            28000,
            8500,
            7500,
            12000,
            6.5,
            "2026-05-06"
        ),
        (
            "TRIP004",
            "Truck 016",
            "Driver Sao",
            "Chongqing to Berlin",
            9200,
            189000,
            65000,
            22000,
            18000,
            39000,
            30.0,
            "2026-05-10"
        ),
        (
            "TRIP005",
            "Truck 013",
            "Shunshun",
            "Davis to Los Angeles",
            620,
            72000,
            18000,
            5000,
            4000,
            9000,
            2.0,
            "2026-05-12"
        ),
        (
            "TRIP006",
            "Truck 014",
            "Aijia",
            "Sydney to Melbourne",
            880,
            86000,
            23000,
            6000,
            4500,
            11000,
            1.5,
            "2026-05-15"
        )
    ]

    # 逐条处理并写入 trips 表
    for trip in sample_trips:
        (
            trip_id,
            truck_id,
            driver,
            route,
            distance,
            revenue,
            fuel_cost,
            toll_cost,
            maintenance_cost,
            driver_cost,
            delay_hours,
            trip_date
        ) = trip

        # 计算总成本和利润
        total_cost = fuel_cost + toll_cost + maintenance_cost + driver_cost
        profit = revenue - total_cost

        # 计算利润率
        if revenue == 0:
            profit_margin = 0
        else:
            profit_margin = profit / revenue * 100

        # 计算每公里成本
        if distance == 0:
            cost_per_km = 0
        else:
            cost_per_km = total_cost / distance

        # 根据利润率判断风险等级
        if profit_margin >= 25:
            risk_level = "Excellent"
        elif profit_margin >= 15:
            risk_level = "Normal"
        elif profit_margin >= 5:
            risk_level = "Warning"
        else:
            risk_level = "High Risk"

        # 插入一条 trip 记录
        conn.execute("""
            INSERT INTO trips (
                trip_id,
                truck_id,
                driver,
                route,
                distance,
                revenue,
                fuel_cost,
                toll_cost,
                maintenance_cost,
                driver_cost,
                delay_hours,
                trip_date,
                total_cost,
                profit,
                profit_margin,
                cost_per_km,
                risk_level
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trip_id,
            truck_id,
            driver,
            route,
            distance,
            revenue,
            fuel_cost,
            toll_cost,
            maintenance_cost,
            driver_cost,
            delay_hours,
            trip_date,
            total_cost,
            profit,
            profit_margin,
            cost_per_km,
            risk_level
        ))

    # 保存并关闭数据库
    conn.commit()
    conn.close()


# 执行初始化
create_trips_table()
import_sample_trips()

print("Trips table initialized successfully.")