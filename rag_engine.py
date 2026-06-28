# FleetMind V7.1 - 模块化 RAG 引擎
# 功能：负责调度知识库检索、数据库检索和管理回答生成。

from document_retriever import retrieve_documents
from database_retriever import get_database_context
from answer_generator import clean_text, get_sources, generate_management_answer


def ask_rag(question, top_k=5):
    """
    RAG 主函数：
    1. 检索 knowledge_base
    2. 检索 SQLite 数据库
    3. 生成管理建议
    """

    # 从知识库中检索相关 chunks
    results = retrieve_documents(question, top_k=top_k)

    # 提取知识库文本，给管理建议函数使用
    doc_results = []

    for result in results:
        # document_retriever 返回的字段名是 content
        clean_result = clean_text(result["content"])
        doc_results.append(clean_result)

    # 根据问题从数据库中检索相关运营数据
    database_context = get_database_context(question)

    # 把数据库文字结果转成列表，方便统一展示
    db_results = []

    if database_context != "":
        for line in database_context.split("\n"):
            clean_line = line.strip()

            # 跳过空行
            if clean_line != "":
                db_results.append(clean_line)

    # 生成管理建议回答
    answer = generate_management_answer(question, doc_results, db_results)

    # 提取来源文件
    sources = get_sources(results)

    return {
        "answer": answer,
        "sources": sources,
        "results": results,
        "database_context": database_context
    }


# 直接运行本文件时，用于测试 RAG 整体流程
if __name__ == "__main__":
    test_questions = [
        "what should we do with high delay trips",
        "what should we check if fuel cost is high",
        "what should we know about Chongqing-Kunming route",
        "why is cost per kilometre important",
        "what should managers do with high risk trucks"
    ]

    for question in test_questions:
        response = ask_rag(question, top_k=3)

        print("=" * 60)
        print("Question:", question)
        print()
        print(response["answer"])

        print("Sources:")
        for source in response["sources"]:
            print("-", source)