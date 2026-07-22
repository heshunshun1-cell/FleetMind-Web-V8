# 导入 Flask 应用工厂
from app import create_app

# 导入项目配置
from config import Config

# 创建 Flask 应用实例
app = create_app()


# 项目启动入口
if __name__ == "__main__":
    app.run(
        # 是否开启调试模式（开发环境一般开启）
        debug=Config.DEBUG,

        # Flask 运行端口（从 config.py 读取）
        port=Config.PORT
    )

# run.py 负责创建 Flask 应用并启动 Web 服务，是整个项目的启动入口。
# run.py = 启动按钮（真正把程序运行起来）