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
1. You must answer using ONLY the provided Knowledge Base Evidence and Database Context.
2. You must return ONLY valid JSON.
3. Do not include markdown, bullet points, explanations outside JSON, or code fences.
4. Prefer Database Context for factual operational claims.
5. Use Knowledge Base Evidence only for policies, rules, and management reasoning.
6. Keep the answer concise, practical, and easy to scan.

Hallucination Control Rules:
1. Do not invent truck IDs, trip IDs, route names, drivers, dates, revenue, costs, profits, margins, delay hours, or risk levels.
2. If a truck, trip, route, or cost item is not shown in the Database Context, do not claim it exists.
3. If Database Context says no related records were retrieved, clearly state that no related database records were found.
4. If Knowledge Base Evidence is missing or weak, clearly state that the policy evidence is limited.
5. If Database Context and Knowledge Base Evidence conflict, prioritize Database Context for factual claims.
6. If the question requires data that is not provided, say that more data is needed instead of guessing.

JSON Output Schema:
Return exactly one JSON object with the following keys:

{{
  "short_answer": "Answer the user's question directly in 1-2 short sentences.",
  "data_status": "sufficient | limited | missing",
  "key_evidence": [
    "Evidence point 1. Prefer database evidence if available.",
    "Evidence point 2. Use policy evidence if database evidence is missing.",
    "Evidence point 3. Keep each evidence point short."
  ],
  "recommended_actions": [
    "Action 1. Keep it practical and specific.",
    "Action 2. Keep it short.",
    "Action 3. Do not exceed three actions."
  ],
  "limitation": "State missing or limited data in one short sentence."
}}

Strict JSON Rules:
1. Return valid JSON only.
2. Use double quotes for all keys and string values.
3. Do not add any text before or after the JSON object.
4. Do not wrap the JSON in markdown or code blocks.
5. The key_evidence array must contain at most 3 items.
6. The recommended_actions array must contain at most 3 items.
7. The data_status value must be one of: "sufficient", "limited", or "missing".
8. If there is no database evidence, set data_status to "missing" or "limited" and explain this in limitation.
"""
    
    return prompt.strip()

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

