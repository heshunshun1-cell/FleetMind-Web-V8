def clean_text(text):
    """
    清理知识库文本格式。
    主要去掉多余的 markdown 符号。
    """

    # 用来保存清理后的每一行
    cleaned_lines = []

    # 按行处理文本
    for line in text.split("\n"):
        clean_line = line.strip()

        # 如果这一行以 # 开头，就去掉 #
        if clean_line.startswith("#"):
            clean_line = clean_line.lstrip("#").strip()

        cleaned_lines.append(clean_line)

    return "\n".join(cleaned_lines)


def get_sources(search_results):
    """
    从检索结果中提取不重复的来源文件名。
    """

    # 用来保存不重复的来源文件
    sources = []

    for result in search_results:
        if result["source"] not in sources:
            sources.append(result["source"])

    return sources


def generate_answer(question, search_results):
    """
    基础回答生成函数。
    如果没有数据库结果，也可以只根据知识库回答。
    """

    # 如果没有找到相关资料
    if len(search_results) == 0:
        return "Sorry, I could not find relevant information in the FleetMind knowledge base."

    answer = "FleetMind Assistant Answer:\n\n"

    # 把检索到的知识库片段拼接成回答
    for result in search_results:
        answer += clean_text(result["text"]) + "\n\n"

    return answer


def generate_management_answer(question, doc_results, db_results):
    """
    把 knowledge_base 结果和 SQLite 结果整理成管理建议。
    """

    answer = []

    # 显示用户问题
    answer.append("Question:")
    answer.append(question)
    answer.append("")

    # 总体管理判断
    answer.append("Management Answer:")
    answer.append(
        "Based on the retrieved fleet knowledge and database records, "
        "this issue should be reviewed from both policy rules and real operation data."
    )
    answer.append("")

    # 显示数据库检索结果
    answer.append("Database Findings:")

    # 如果数据库找到相关结果，就逐条显示
    if len(db_results) > 0:
        for item in db_results:
            # 数据库标题不加横线，更像小标题
            if item.startswith("Database Result"):
                answer.append(item)

            # Truck ID 前面加空行，方便区分不同车辆
            elif item.startswith("Truck ID"):
                answer.append("")
                answer.append(item)

            # 其他数据库字段正常显示
            else:
                answer.append(item)

    else:
        answer.append("No directly related database records were found.")

    answer.append("")

    # 显示知识库检索结果
    answer.append("Knowledge Base Findings:")

    if len(doc_results) > 0:
        for item in doc_results:
            answer.append(f"- {item}")
    else:
        answer.append("- No directly related knowledge base records were found.")

    answer.append("")

    # 根据问题生成管理建议
    answer.append("Suggested Action:")

    question_lower = question.lower()

    if "high risk" in question_lower and "truck" in question_lower:
        answer.append(
            "- Prioritise the listed high-risk trucks and review their profit margin, "
            "main cost pressure, and route performance."
        )
        answer.append(
            "- Consider route adjustment, cost control, or maintenance review before future dispatch."
        )
    else:
        answer.append(
            "- Review the retrieved knowledge and database findings together before making an operation decision."
        )

    # 把 list 里的每一项，用换行符连接成一整段字符串
    return "\n".join(answer)