import sqlite3

# 导入项目统一配置
from config import Config


def fix_trip_risk_levels():
    """重新计算旧 trip records 的 risk level"""

    # 连接数据库
    # 从统一配置中读取数据库路径
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    # 读取所有 trip records
    trips = conn.execute("SELECT * FROM trips").fetchall()

    # 逐条重新计算 risk level
    for trip in trips:
        profit = float(trip["profit"])
        profit_margin = float(trip["profit_margin"])
        delay_hours = float(trip["delay_hours"])

        # 按 V5.4 最新规则判断风险等级
        if profit < 0 or delay_hours >= 24:
            risk_level = "High Risk"
        elif profit_margin < 10 or delay_hours >= 12:
            risk_level = "Warning"
        elif profit_margin >= 25 and delay_hours < 6:
            risk_level = "Excellent"
        else:
            risk_level = "Normal"

        # 更新当前 trip 的 risk level
        conn.execute("""
            UPDATE trips
            SET risk_level = ?
            WHERE trip_id = ?
        """, (risk_level, trip["trip_id"]))

    # 保存修改
    conn.commit()

    # 关闭数据库
    conn.close()

    print("Trip risk levels updated successfully.")


fix_trip_risk_levels()