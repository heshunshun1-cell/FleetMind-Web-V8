from flask import Blueprint, render_template

from database import (
    get_route_analytics_from_db,
    get_route_summary_from_db,
    generate_route_insights_from_db
)


# Route Analytics 路由模块：管理路线分析页面
route_analytics_bp = Blueprint("route_analytics", __name__)


# 路线分析页面
@route_analytics_bp.route("/route-analytics")
def route_analytics():
    # 获取路线分析数据
    routes = get_route_analytics_from_db()

    # 获取路线 summary cards 数据
    route_summary = get_route_summary_from_db()

    # 生成路线运营建议
    route_insights = generate_route_insights_from_db()

    # 把路线数据和建议传给页面
    return render_template(
        "route_analytics.html",
        routes=routes,
        route_summary=route_summary,
        route_insights=route_insights
    )