from flask import Blueprint, render_template

from database import generate_insights_from_db


# Insights 路由模块：管理运营建议页面
insights_bp = Blueprint("insights", __name__)


# 运营建议页面
@insights_bp.route("/insights")
def insights():
    # 从 SQLite 数据库生成运营建议
    insights = generate_insights_from_db()

    # 把建议传给页面
    return render_template("insights.html", insights=insights)