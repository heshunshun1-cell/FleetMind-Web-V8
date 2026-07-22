from openai import OpenAI

# 导入项目统一配置
from config import Config


def generate_llm_answer(prompt):
    """
    调用大模型生成回答。
    如果未启用 LLM 或缺少 API Key，就返回 None。
    """

    # 如果关闭了 LLM，就使用后备回答
    if not Config.USE_LLM:
        return None

    # 从统一配置读取 API Key
    api_key = Config.OPENAI_API_KEY

    # 从统一配置读取模型名称
    model = Config.OPENAI_MODEL

    # 如果没有 API Key，就跳过 LLM 调用
    if not api_key or api_key.strip() == "":
        return None

    try:
        # 创建 OpenAI 客户端
        client = OpenAI(api_key=api_key)

        # 把 prompt 发送给大模型
        response = client.responses.create(
            model=model,
            input=prompt
        )

        # 返回大模型生成的文本
        return response.output_text

    except Exception as error:
        # API 调用失败时，不让整个系统崩溃
        print("LLM API error:", error)
        return None


# 单独运行本文件时，用来测试 LLM 通道
if __name__ == "__main__":
    test_prompt = "Give one short logistics management suggestion."

    result = generate_llm_answer(test_prompt)

    if result is None:
        print("LLM was skipped or failed. Fallback mode is working.")
    else:
        print(result)