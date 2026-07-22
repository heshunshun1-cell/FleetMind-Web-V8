from flask import Blueprint, render_template

# 主路由 Blueprint：管理首页和健康检查
main_bp = Blueprint("main", __name__)


# 首页：渲染 FleetMind 主页面
@main_bp.route("/")
def index():
    return render_template("index.html")


# 健康检查接口：用于部署和服务状态检测
@main_bp.route("/healthz")
def health_check():
    return {
        "status": "ok",
        "message": "service is running"
    }