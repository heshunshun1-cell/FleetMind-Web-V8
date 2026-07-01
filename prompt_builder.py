def format_knowledge_evidence(doc_results):
    """
    把 knowledge_base 检索结果整理成 prompt 里的证据文本。
    doc_results 是一个 list，每一项是一段知识库内容。
    """
    
    # 如果没有检索到知识库
    if len(doc_results) == 0:
        return "No relevant knowledge base evidence was retrieved."
    
    evidence_text = ""

    # 给每条知识库证据编号，方便 LLM 引用
    for index, item in enumerate(doc_results, start=1):
        evidence_text += f"[Knowledge Evidence {index}]\n"
        evidence_text += item
        evidence_text += "\n\n"

    return evidence_text.strip()


def format_database_context(database_context):
    """
    把数据库检索结果整理成 prompt 里的数据库上下文。
    database_context 目前是 database_retriever.py 返回的字符串。
    """
    # 如果没有数据库结构
    if len(database_context) == 0:
        return "No relevant database records were retrieved."
    
    return database_context.strip()


def build_rag_prompt(question, doc_results, database_context):
    """
    构建未来发送给 LLM 的 RAG prompt。
    目前只生成 prompt，不调用任何 LLM API。
    """

    # 整理知识库证据
    knowledge_evidence = format_knowledge_evidence(doc_results)

    # 整理数据库上下文
    database_evidence = format_database_context(database_context)

    prompt = f"""
You are FleetMind Assistant, a logistics management assistant.

Your task is to answer the user's question using ONLY the provided knowledge base evidence and database context.

User Question:
{question}

Knowledge Base Evidence:
{knowledge_evidence}

Database Context:
{database_evidence}

Answer Requirements:
1. Answer the user question using only the provided Knowledge Base Evidence and Database Context.
2. Separate factual findings from management recommendations.
3. Prioritise Database Context when the question asks about actual trucks, trips, routes, costs, profit, delay, or risk.
4. Use Knowledge Base Evidence to explain policies, rules, and management reasoning.
5. Keep the answer concise, practical, and suitable for logistics managers.

Hallucination Control Rules:
1. Do not invent truck IDs, trip IDs, route names, drivers, dates, revenue, costs, profits, margins, delay hours, or risk levels.
2. If a truck, trip, or route is not shown in the Database Context, do not claim it exists.
3. If Database Context says no records were found, clearly state that no related database records were retrieved.
4. If Knowledge Base Evidence is missing or weak, clearly state that the knowledge evidence is limited.
5. If the answer requires data that is not provided, say that more data is needed instead of guessing.
6. Treat Database Context as factual operational data and Knowledge Base Evidence as policy or reasoning support.
7. If Knowledge Base Evidence and Database Context appear to conflict, prioritise Database Context for factual claims.

Required Answer Structure:
1. Direct Answer
   - Answer the user's question directly in one or two sentences.

2. Key Operational Findings
   - Summarise the most relevant database records, such as trucks, trips, routes, costs, profit, delay, or risk level.
   - If no database records were retrieved, clearly state that no related database records were found.

3. Risk or Cost Explanation
   - Explain the operational meaning of the findings using the knowledge base evidence.
   - Do not introduce facts that are not present in the evidence.

4. Recommended Actions
   - Give practical management actions based on the retrieved evidence and database context.
   - Recommendations should be specific, realistic, and suitable for logistics managers.

5. Data Limitations
   - State what information is missing or limited.
   - If the answer is based only on limited evidence, clearly mention this.
""".strip()
    
    return prompt

# 单独运行本文件时，用于测试 prompt 生成效果
if __name__ == "__main__":
    test_question = "Which routes are expensive?"

    test_doc_results = [
        "Cost per kilometre is important because it helps managers compare route efficiency.",
        "Routes with high fuel cost or high maintenance cost should be reviewed carefully."
    ]

    test_database_context = """
Database Result - Route Performance Summary:

Route: Davis to Los Angeles
Total Trips: 1
Total Distance: 620.00 km
Total Revenue: 72,000.00
Total Cost: 36,000.00
Total Profit: 36,000.00
Average Profit Margin: 50.00%
Average Cost Per Km: 58.06
Average Delay Hours: 2.00
"""

    result = build_rag_prompt(
        test_question,
        test_doc_results,
        test_database_context
    )

    print(result)

