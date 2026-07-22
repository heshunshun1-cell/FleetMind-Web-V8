# config.py 负责集中管理整个项目的配置参数，实现配置与业务代码分离。
# config.py = 项目说明书（告诉程序怎么运行）
import os

from dotenv import load_dotenv


# 读取项目根目录中的 .env 文件
# dotenv 就是负责把 .env 文件里的配置，加载到 Python 程序里面。
load_dotenv()


class Config:
    """集中管理 FleetMind 的应用配置。"""

    # 是否开启 Flask 调试模式
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # Flask 本地运行端口
    PORT = int(os.getenv("PORT", "5001"))

    # SQLite 数据库文件路径
    DATABASE_PATH = os.getenv("DATABASE_PATH", "fleetmind.db")

    # 知识库文件夹路径
    KNOWLEDGE_BASE_PATH = os.getenv(
        "KNOWLEDGE_BASE_PATH",
        "knowledge_base"
    )

    # 语义检索使用的 Embedding 模型
    EMBEDDING_MODEL_NAME = os.getenv(
        "EMBEDDING_MODEL_NAME",
        "all-MiniLM-L6-v2"
    )

    # OpenAI API Key：从 .env 读取，不写死在代码中
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # OpenAI 模型名称
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    # 是否启用大模型回答
    USE_LLM = os.getenv("USE_LLM", "True").lower() == "true"