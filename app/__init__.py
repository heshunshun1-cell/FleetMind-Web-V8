from flask import Flask

# 倒入项目统一配置
from config import Config


def create_app():
    """
    创建并返回 Flask 应用。
    这里负责加载配置和注册各个路由模块。
    """
    # 创建 Flask 应用实例
    app = Flask(__name__)
    # 把 config.py 中的配置加载到 Flask 应用中
    app.config.from_object(Config)

    # 注册主路由模块
    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    # 注册 Dashboard 路由模块
    from app.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp)

    # 注册 Analytics 路由模块
    from app.routes.analytics_routes import analytics_bp
    app.register_blueprint(analytics_bp)

    # 注册 Insights 路由模块
    from app.routes.insights_routes import insights_bp
    app.register_blueprint(insights_bp)

    # 注册 Trip 路由模块
    from app.routes.trip_routes import trip_bp
    app.register_blueprint(trip_bp)


    # 注册 Route Analytics 路由模块
    from app.routes.route_analytics_routes import route_analytics_bp
    app.register_blueprint(route_analytics_bp)

    # 注册 Truck 路由模块
    from app.routes.truck_routes import truck_bp
    app.register_blueprint(truck_bp)

    # 注册 RAG 路由模块
    from app.routes.rag_routes import rag_bp
    app.register_blueprint(rag_bp)


    return app