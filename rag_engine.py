# FleetMind V6.2 - 简单 RAG 引擎
# 功能：读取知识库、切分 chunks、检索相关内容，并生成带 sources 的回答。
import os

# 从 database.py 中导入高风险车辆查询函数
from database import get_high_risk_trucks_from_db

# 知识库文件夹路径
KNOWLEDGE_BASE_DIR = "knowledge_base"

# 停用词：这些词太常见，对搜索帮助不大，所以先忽略
STOP_WORDS = [
    "what", "is", "the", "a", "an", "we", "do", "with",
    "should", "to", "for", "of", "and", "or", "in"
]

def normalize_word(word):
    # 简单去掉标点
    word = word.strip(".,?!:")

    # 简单处理复数：trips -> trip
    if word.endswith("s") and len(word) > 3:
        word = word[:-1]

    return word

def load_documents():
    # 用来保存所有读取到的文档
    documents = []

    # 遍历 knowledge_base 文件夹里所有的文件件
    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        #只读取 .txt 文件
        if filename.endswith(".txt"):
            file_path = os.path.join(KNOWLEDGE_BASE_DIR, filename)

            # 读取 txt 文件内容
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # 保存文件名和文件内容
            documents.append({
                "source": filename,
                "content": content
            })

    return documents

def split_documents_into_chunks(documents):
    # 用来保存所有被切分出来的知识片段
    chunks = []

    # 遍历每一个文档
    for doc in documents:
        source = doc["source"]
        content = doc["content"]

        # 用空行切分文档内容
        parts = content.split("\n\n")

        # 遍历每一个切分出来的小段
        for part in parts:
            clean_part = part.strip()

            # 跳过空内容
            if clean_part != "":
                chunks.append({
                    "source": source,
                    "text": clean_part
                })

    return chunks

def search_chunks(question, chunks, top_k=5, min_score=2):
    # 用来保存匹配到的知识片段
    results = []

    # 把用户问题拆成单词，并去掉停用词
    question_words = []

    for word in question.lower().split():
        clean_word = normalize_word(word)

        if clean_word not in STOP_WORDS:
            question_words.append(clean_word)

    # 如果问题里有核心业务词，就要求结果必须包含这个词
    required_words = []

    if "delay" in question_words:
        required_words.append("delay")

    if "fuel" in question_words:
        required_words.append("fuel")

    # 遍历所有 chunk
    for chunk in chunks:
        text_lower = chunk["text"].lower()

        # 把 chunk 文本也拆成单词，并做 normalization
        text_words = []

        for word in text_lower.split():
            text_words.append(normalize_word(word))

        # 检查 chunk 是否包含必须关键词
        has_required_words = True

        for required_word in required_words:
            if required_word not in text_words:
                has_required_words = False

        # 计算这个 chunk 匹配了多少关键词
        score = 0

        for word in question_words:
            if word in text_words:
                score += 1

        # 只保存至少匹配到1个关键词的 chunk
        if score >= min_score and has_required_words:
            results.append({
                "source": chunk["source"],
                "text": chunk["text"],
                "score": score
            })

    # 按匹配分数从高到低排序
    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:top_k]

def clean_text(text):
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
    # 用来保存不重复的来源文件
    sources = []

    for result in search_results:
        if result["source"] not in sources:
            sources.append(result["source"])

    return sources

def get_database_context(question):
    """根据用户问题，从数据库中检索相关运营数据"""

    # 把问题转成小写，方便关键词判断
    question_lower = question.lower()

    # 用来保存数据库检索结果
    database_context = ""

    # 如果问题和高风险车辆有关，就查询 trucks 表
    if "high risk" in question_lower and "truck" in question_lower:
        high_risk_trucks = get_high_risk_trucks_from_db()

        # 如果数据库中没有高风险车辆
        if len(high_risk_trucks) == 0:
            database_context += "Database Result:\n"
            database_context += "No high risk trucks were found in the current database.\n"

        else:
            database_context += "Database Result - High Risk Trucks:\n\n"

            # 把每一辆高风险车整理成文字
            for truck in high_risk_trucks:
                database_context += f"Truck ID: {truck['truck_id']}\n"
                database_context += f"Driver: {truck['driver']}\n"
                database_context += f"Route: {truck['route']}\n"
                database_context += f"Revenue: {truck['revenue']}\n"
                database_context += f"Total Cost: {truck['total_cost']}\n"
                database_context += f"Profit: {truck['profit']}\n"
                database_context += f"Profit Margin: {truck['profit_margin']}%\n"
                database_context += f"Risk Level: {truck['risk_level']}\n"
                database_context += f"Main Cost Pressure: {truck['highest_cost_category']}\n\n"

    return database_context


def generate_answer(question, search_results):
    # 如果没有找到相关资料
    if len(search_results) == 0:
        return "Sorry, I could not find relevant information in the FleetMind knowledge base."

    answer = "FleetMind Assistant Answer:\n\n"

    # 生成主要回答内容
    for result in search_results:
        answer += clean_text(result["text"]) + "\n\n"

    return answer


def generate_management_answer(question, doc_results, db_results):
    """V6.5: 把knowledge_base结果和SQLite结果整理成管理建议"""

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

            # 其他数据库字段显示正常
            else:
                answer.append(item)

    else:
        answer.append("No directly related database records were found.")

    # 显示知识库检索结果
    answer.append("Knowledge Base Findings:")
    if len(doc_results) > 0:
        for item in doc_results:
            answer.append(f"- {item}")
    else:
        answer.append("- No directly related database records were found.")
    answer.append("")

    # 生成管理回答建议
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

    # 把 list 里的每一项，用换行符 \n 连接成一整段字符串
    return "\n".join(answer)


def ask_rag(question, top_k=5):
    """RAG 主函数：检索知识库 + 数据库，并生成管理建议"""

    # 读取知识库文档
    docs = load_documents()

    # 把长文档切成小片段，方便检索
    chunks = split_documents_into_chunks(docs)

    # 从知识库中检索和问题最相关的 chunks
    results = search_chunks(question, chunks, top_k=top_k)

    # 提取知识库文本，给管理建议函数使用
    doc_results = []

    for result in results:
        # 清理文本格式，去掉多余的 markdown 符号
        clean_result = clean_text(result["text"])
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

    # 用 V6.5 新函数生成更像管理建议的回答
    answer = generate_management_answer(question, doc_results, db_results)

    # 提取来源文件
    sources = get_sources(results)

    return {
        "answer": answer,
        "sources": sources,
        "results": results,
        "database_context": database_context
    }

# 直接运行这个文件时，用来测试读取结果
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