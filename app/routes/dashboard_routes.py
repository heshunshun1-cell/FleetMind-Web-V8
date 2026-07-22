from flask import Blueprint, render_template

from database import get_dashboard_data_from_db


# Dashboard 路由模块：管理车队看板页面
dashboard_bp = Blueprint("dashboard", __name__)


# 车队 Dashboard 页面
@dashboard_bp.route("/dashboard")
def dashboard():
    # 从 SQLite 数据库读取并计算 dashboard 数据
    data = get_dashboard_data_from_db()

    # 把 dashboard 数据传给页面
    return render_template("dashboard.html", data=data)