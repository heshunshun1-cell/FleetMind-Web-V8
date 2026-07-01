import os

from dotenv import load_dotenv
from openai import OpenAI


# 读取 .env 文件里的配置
load_dotenv()


def generate_llm_answer(prompt):
    """
    调用 LLM 生成回答。

    当前如果没有 API key，就不会真正调用 LLM。
    返回 None，表示后面继续使用原来的 rule-based answer。
    """

    # 从 .env 读取 API key
    api_key = os.getenv("OPENAI_API_KEY")

    # 从 .env 读取模型名；如果没写，就默认用 gpt-5.5
    model = os.getenv("OPENAI_MODEL", "gpt-5.5")

    # 如果没有 API key，就直接跳过 LLM
    if api_key is None or api_key.strip() == "":
        return None

    try:
        # 创建 OpenAI 客户端
        client = OpenAI(api_key=api_key)

        # 把 prompt 发给 LLM
        response = client.responses.create(
            model=model,
            input=prompt
        )

        # 返回 LLM 生成的文字
        return response.output_text

    except Exception as error:
        # 如果 API 调用失败，不让整个系统崩掉
        print("LLM API error:", error)
        return None


# 单独运行本文件时，用来测试 LLM 通道
if __name__ == "__main__":
    test_prompt = "Give one short logistics management suggestion."

    result = generate_llm_answer(test_prompt)

    if result is None:
        print("No API key found. LLM was skipped. Fallback mode is working.")
    else:
        print(result)