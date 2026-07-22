import os
from sentence_transformers import SentenceTransformer, util

# 导入项目统一配置
from config import Config

# 知识库文件夹路径
KNOWLEDGE_BASE_DIR = Config.KNOWLEDGE_BASE_PATH

# 加在一个轻量级 embedding 模型
model = SentenceTransformer(Config.EMBEDDING_MODEL_NAME)

def load_documents():
    """
    读取 knowledge_base 文件夹中的 txt 文件，
    并把每个文件按空行切分成多个知识片段。
    """
    documents = []

    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(KNOWLEDGE_BASE_DIR, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                # 用空行切分知识片段
                chunks = content.split("\n\n")

                for chunk in chunks:
                    # 去掉首尾空白字符
                    chunk = chunk.strip()

                    if chunk:
                        documents.append({
                            "source": filename,
                            "content": chunk
                        })

    return documents


def semantic_search(query, top_k=3):
    """
    根据用户问题进行语义检索，
    返回最相关的 top_k 个知识片段。
    """
    documents = load_documents()

    if not documents:
        return []
    
    # 只取知识片段文本，用于生成 embedding
    texts = [doc["content"] for doc in documents]

    # 把用户问题转换成 embedding
    query_embedding = model.encode(query, convert_to_tensor=True)

    # 把所有知识片段换成 embedding
    document_embeddings = model.encode(texts, convert_to_tensor=True)

    # 计算用户问题和每个知识片段之间语意的相似度
    similarities = util.cos_sim(query_embedding, document_embeddings)[0]

    # 获取相似度最高的 top_k 个结果
    top_results = similarities.topk(k=min(top_k, len(documents)))

    results = []

    for score, index in zip(top_results.values, top_results.indices):
        doc = documents[index]

        results.append({
            "source": doc["source"],
            "content": doc["content"],
            "score": round(float(score), 4)
        })

    return results

if __name__ == "__main__":
    question = "Which routes have serious delay problems?"

    results = semantic_search(question)

    print("Question:", question)
    print("=" * 50)

    for result in results:
        print("Source:", result["source"])
        print("Score:", result["score"])
        print("Content:", result["content"])
        print("-" * 50)

   
