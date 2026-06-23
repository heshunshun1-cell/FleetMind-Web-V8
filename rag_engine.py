import os
# FleetMind V6.2 - 简单 RAG 引擎
# 功能：读取知识库、切分 chunks、检索相关内容，并生成带 sources 的回答。

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


def generate_answer(question, search_results):
    # 如果没有找到相关资料
    if len(search_results) == 0:
        return "Sorry, I could not find relevant information in the FleetMind knowledge base."

    answer = "FleetMind Assistant Answer:\n\n"

    # 生成主要回答内容
    for result in search_results:
        answer += clean_text(result["text"]) + "\n\n"

    return answer

def ask_rag(question, top_k=5):
    # 读取知识库文档
    docs = load_documents()

    # 把文档切成 chunks
    chunks = split_documents_into_chunks(docs)

    # 检索和问题最相关的 chunks
    results = search_chunks(question, chunks, top_k=top_k)

    # 根据检索结果生成回答
    answer = generate_answer(question, results)

    # 提取来源文件
    sources = get_sources(results)

    return {
        "answer": answer,
        "sources": sources,
        "results": results
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