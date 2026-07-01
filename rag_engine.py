# FleetMind V7.6 - Semantic RAG 引擎
# 功能：负责调度语义知识库检索、数据库检索、Prompt 构建和回答生成。

from semantic_retriever import semantic_search
from database_retriever import get_database_context
from answer_generator import clean_text, get_sources, generate_management_answer
from prompt_builder import build_rag_prompt
from llm_client import generate_llm_answer


def ask_rag(question, top_k=5):
    """
    RAG 主函数：
    1. 用 semantic_search 从 knowledge_base 中找相关知识片段
    2. 从 SQLite 数据库中找相关运营数据
    3. 构建 prompt
    4. 优先使用 LLM 生成回答
    5. 如果没有 API key 或 LLM 调用失败，就使用 rule-based fallback
    """

    # 第一步：从知识库中进行语义检索
    # 这里已经不是简单 keyword search，而是 embedding-based semantic search
    document_results = semantic_search(question, top_k=top_k)

    # 第二步：提取知识库文本内容
    # generate_management_answer 和 prompt_builder 需要的是纯文本列表
    doc_context = []

    for result in document_results:
        clean_content = clean_text(result["content"])
        doc_context.append(clean_content)

    # 第三步：根据用户问题，从数据库中检索相关运营数据
    # 例如 high delay trips, loss-making trucks, high cost routes 等
    database_context = get_database_context(question)

    # 第四步：把数据库结果整理成列表
    # rule-based answer 需要 list 格式，方便逐条生成建议
    db_context = []

    if database_context != "":
        for line in database_context.split("\n"):
            clean_line = line.strip()

            if clean_line != "":
                db_context.append(clean_line)

    # 第五步：先生成 rule-based answer
    # 这是备用回答，不依赖 API，所以系统更稳定
    rule_based_answer = generate_management_answer(
        question,
        doc_context,
        db_context
    )

    # 第六步：构建给 LLM 使用的 prompt
    # prompt 中会包含：用户问题、知识库证据、数据库结果和回答要求
    generated_prompt = build_rag_prompt(
        question,
        doc_context,
        database_context
    )

    # 第七步：尝试调用 LLM 生成自然语言回答
    # 如果没有配置 API key，generate_llm_answer 会返回 None
    llm_answer = generate_llm_answer(generated_prompt)

    # 第八步：优先使用 LLM 回答；如果失败，就使用 rule-based fallback
    if llm_answer is not None:
        answer = llm_answer
        answer_mode = "LLM"
    else:
        answer = rule_based_answer
        answer_mode = "Rule-based fallback"

    # 第九步：提取知识来源，方便网页展示 evidence / sources
    sources = get_sources(document_results)

    # 最后统一返回结果
    # Flask 页面可以用这些字段展示 answer、sources、database context 和 prompt
    return {
        "answer": answer,
        "answer_mode": answer_mode,
        "sources": sources,
        "results": document_results,
        "database_context": database_context,
        "generated_prompt": generated_prompt
    }


# 直接运行本文件时，用于测试 RAG 整体流程
if __name__ == "__main__":
    test_questions = [
        "what should we do with high delay trips",
        "which routes have serious delay problems",
        "which trucks have high fuel cost"
    ]

    for question in test_questions:
        response = ask_rag(question, top_k=3)

        print("=" * 60)
        print("Question:", question)
        print()
        print("Answer:")
        print(response["answer"])

        print()
        print("Answer Mode:")
        print(response["answer_mode"])

        print()
        print("Sources:")
        for source in response["sources"]:
            print("-", source)

        print()
        print("Database Context:")
        print(response["database_context"])

        print()
        print("Generated Prompt:")
        print(response["generated_prompt"])