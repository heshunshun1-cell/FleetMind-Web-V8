import csv
from database import get_db_connection

# CSV 文件名
CSV_FILE = "fleet_data.csv"


def create_trucks_table():
    """创建 trucks 表, 从 CSV 导入数据"""

    # 连接数据库
    conn = get_db_connection()

    # 创建 trucks 表，字段和 fleet_data.csv 保持一致
    conn.execute("""
    CREATE TABLE IF NOT EXISTS trucks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        truck_id TEXT,
        driver TEXT,
        route TEXT,
        revenue REAL,
        fuel_cost REAL,
        toll_cost REAL,
        repair_cost REAL,
        salary_cost REAL,
        insurance_cost REAL,
        other_cost REAL,
        total_cost REAL,
        profit REAL,
        profit_margin REAL,
        risk_level TEXT,
        highest_cost_category TEXT,
        highest_cost_value REAL
    )
    """)

    # 保存修改并关闭连接
    conn.commit()
    conn.close()


def import_csv_to_db():
    """把 fleet_data.csv 导入 trucks 表"""

    # 连接数据库
    conn = get_db_connection()

    # 先清空旧数据，避免重复导入
    conn.execute("DELETE FROM trucks")

    # 打开 CSV 文件
    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # 一行一行读取 CSV，并插入数据库
        for row in reader:
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
                row["truck_id"],
                row["driver"],
                row["route"],
                float(row["revenue"]),
                float(row["fuel_cost"]),
                float(row["toll_cost"]),
                float(row["repair_cost"]),
                float(row["salary_cost"]),
                float(row["insurance_cost"]),
                float(row["other_cost"]),
                float(row["total_cost"]),
                float(row["profit"]),
                float(row["profit_margin"]),
                row["risk_level"],
                row["highest_cost_category"],
                float(row["highest_cost_value"])
            ))

    # 保存修改并关闭连接
    conn.commit()
    conn.close()




# 程序从这里开始执行
create_trucks_table()
import_csv_to_db()

print("Database initialized and CSV data imported successfully.")