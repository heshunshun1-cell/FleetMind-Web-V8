import os
import re

# 知识库文件夹路径
KNOWLEDGE_BASE_DIR = "knowledge_base"


# 停用词：这些词太常见，对检索帮助不大
STOP_WORDS = ["what", "which", "why", "how",
    "is", "are", "was", "were",
    "the", "a", "an",
    "we", "do", "does", "did",
    "should", "can", "could",
    "to", "for", "of", "and", "or", "in", "on", "at", "by",
    "with", "about", "know", "check", "manager", "managers"
]


# 同义词扩展：让用户换一种说法已能匹配到相关知识
SYNONYM_MAP = {"late": ["delay", "delayed"],
    "delayed": ["delay", "late"],
    "delay": ["late", "delayed"],

    "expensive": ["cost", "fuel", "maintenance"],
    "costly": ["cost", "fuel", "maintenance"],
    "cost": ["expense", "fuel", "maintenance"],

    "unprofitable": ["loss", "profit", "negative"],
    "losing": ["loss", "unprofitable", "negative"],
    "loss": ["unprofitable", "negative", "profit"],

    "dangerous": ["risk", "high", "high-risk"],
    "risky": ["risk", "high", "high-risk"],
    "risk": ["dangerous", "high-risk"],

    "truck": ["trucks"],
    "trip": ["trips"],
    "route": ["routes"]
}


# （业务）关键词：这些词对物流管理问题更重要
BUSINESS_KEYWORDS = [
    "delay", "risk", "fuel", "cost", "maintenance",
    "profit", "loss", "route", "truck", "trip",
    "revenue", "margin"
]


# （业务）短语匹配加权：完整短语出现时，相关性更高
BUSINESS_PHRASES = [ "high delay",
    "delay risk",
    "high risk",
    "fuel cost",
    "maintenance cost",
    "cost per kilometre",
    "cost per kilometer",
    "profit margin",
    "loss making",
    "negative profit"
]


def normalize_text(text):
    # 简单文本标准化：-转小写 -去掉多余符号 -方便做 keyword matching
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def normalize_word(word):
    # 单个词标准化
    word = word.lower().strip(".,?!:;()[]{}\"'")
    
    if word == "delayed":
        return "delay"
    
    # trips -> trip, trucks -> truck
    if word.endswith("s") and len(word) > 3:
        word = word[:-1]

    return word


def get_query_words(query):
    # 把用户问题变成关键词，并加入同义词
    query_words = []
    # 先把问题标准化，再按空格拆成单词
    #清理单个单词，比如trips -> trip
    for word in normalize_text(query).split():
        clean_word = normalize_word(word)

    # 跳过空词和无意义的常见词
    if clean_word != "" and clean_word not in STOP_WORDS:
        query_words.append(clean_word)
        
        # 如果这个词有同义词，就一起加入检索
        if clean_word in SYNONYM_MAP:
            for synonym in SYNONYM_MAP[clean_word]:
                # 同义词也做一次标准化
                synonym = normalize_word(synonym)

                # 避免重复加入同一个词
                if synonym not in query_words:
                    query_words.append(synonym)
    
    # 返回最终用于检索的关键词列表
    return query_words



def load_knowledge_base(folder_path=KNOWLEDGE_BASE_DIR):
    # 读取 knowledge_base 文件夹里所有 txt 文件
    documents = []

    # 如果知识库文件夹不存在 直接返回空列表
    if not os.path.exists(folder_path):
        return documents
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            # 使用 utf-8 读取知识库文本
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            documents.append({
                "source": filename,
                "content": content
            })

    return documents


def split_into_chunks(text, source, chunk_size=500):
    # 把长文本切成较小的chunks
    # RAG 通常不会直接使用整篇文档， 而是先切成片段
    chunks = []

    # 优先按段落切分，保留语意完整性
    paragraphs = text.split("\n\n")

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        # 跳过空段落
        if not paragraph:
            continue

        # 短段落直接作为一个chunk
        if len(paragraph) <= chunk_size:
            chunks.append({
                "source": source,
                "content": paragraph
            })
        else:
            # 过长段落再按固定长度切开
            for i in range(0, len(paragraph), chunk_size):
                chunks.append({
                    "source": source,
                    "content": paragraph[i:i + chunk_size]
                })

    return chunks


def build_document_chunks():
    # 加载所有知识库文件，并统一切成 chunks
    documents = load_knowledge_base()
    all_chunks = []

    for doc in documents:
        chunks = split_into_chunks(
            text=doc["content"],
            source=doc["source"]
        )
        all_chunks.extend(chunks)

    return all_chunks


def analyze_chunk_match(query, chunk):
    # 分析一个 chunk 匹配到了哪些关键词和短语
    query_words = get_query_words(query) # 用户问题里的关键词列表
    query_text = normalize_text(query) # 用户问题的标准化完整句子
    chunk_text = normalize_text(chunk["content"]) # 知识库片段的标准化完整内容

    matched_keywords = []
    matched_phrases = []

    # 检查匹配到的关键词
    for word in query_words:
        if word in chunk_text:
            matched_keywords.append(word)

    # 检查匹配到的业务短语
    for phrase in BUSINESS_PHRASES:
        normalized_phrase = normalize_text(phrase)

        if normalized_phrase in query_text and normalized_phrase in chunk_text:
            matched_phrases.append(phrase)

    return matched_keywords, matched_phrases


def calculate_score(matched_keywords, matched_phrases):
    # 根据匹配到的关键词和短语计算分数
    score = 0 

    # 关键词打分
    for word in matched_keywords:
        if word in BUSINESS_KEYWORDS:
            score += 2
        else:
            score += 1

    # 短语打分，每个短语额外加3分
    for phrase in matched_phrases:
        score += 3

    return score


def score_chunk(query, chunk):
    # 保留这个函数，方便以后单独测试 chunk 分数
    matched_keywords, matched_phrases = analyze_chunk_match(query, chunk)

    score = calculate_score(matched_keywords, matched_phrases)

    return score


def retrieve_documents(query, top_k=3):
    # 根据用户问题，从 knowledge_base 找出最相关的 chunks
    chunks = build_document_chunks()
    scored_chunks = []

    for chunk in chunks:
        # 先分析当前 chunk 匹配到了哪些关键词和短语
        matched_keywords, matched_phrases = analyze_chunk_match(query, chunk)

        # 根据匹配结果计算相关性分数
        score = calculate_score(matched_keywords, matched_phrases)

        # 只保留有匹配结果的 chunk
        if score > 0:
            scored_chunks.append({
                "source": chunk["source"],
                "content": chunk["content"],
                "score": score,
                "matched_keywords": matched_keywords,
                "matched_phrases": matched_phrases
            })

    # 按相关性分数从高到低排序
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)

    # 只返回分数最高的 top_k 个结果
    return scored_chunks[:top_k]


# 单独运行文本时，用于快速测试知识库检索效果
if __name__ == "__main__":
    question = "Which routes have high delay risk?"
    results = retrieve_documents(question)

    for result in results:
        print("Source:", result["source"])
        print("Score:", result["score"])
        print("Matched Keywords:", result["matched_keywords"])
        print("Matched Phrases:", result["matched_phrases"])
        print("Content:", result["content"])
        print("-" * 50)


# normalize_text()          清理整段文本
# normalize_word()          清理单个词
# get_query_words()         从用户问题提取关键词
# analyze_chunk_match()     判断 chunk 匹配到了什么
# calculate_score()         根据匹配结果计算分数
# retrieve_documents()      返回最终检索结果
