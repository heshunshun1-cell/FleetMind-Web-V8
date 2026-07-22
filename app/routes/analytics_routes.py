from flask import Blueprint, render_template

from database import (
    generate_revenue_chart_from_db,
    generate_profit_chart_from_db,
    generate_risk_chart_from_db,
    generate_cost_pressure_chart_from_db,
    get_analytics_summary_from_db,
    get_loss_making_trucks_from_db
)


# Analytics 路由模块：管理车队分析图表页面
analytics_bp = Blueprint("analytics", __name__)


# 车队 Analytics 页面
@analytics_bp.route("/analytics")
def analytics():
    # 生成四张分析图表
    generate_revenue_chart_from_db()
    generate_profit_chart_from_db()
    generate_risk_chart_from_db()
    generate_cost_pressure_chart_from_db()

    # 获取页面汇总数据
    summary = get_analytics_summary_from_db()

    # 获取亏损车辆数据
    loss_trucks = get_loss_making_trucks_from_db()

    # 把数据传给 analytics 页面
    return render_template(
        "analytics.html",
        summary=summary,
        loss_trucks=loss_trucks
    )