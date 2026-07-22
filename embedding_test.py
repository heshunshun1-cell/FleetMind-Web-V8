from sentence_transformers import SentenceTransformer, util

# 导入项目统一配置
from config import Config

# 使用项目统一配置中的 Embedding 模型
# 它可以把英文句子转换成数字向量
model = SentenceTransformer(Config.EMBEDDING_MODEL_NAME)


# 准备三句测试文本
# 前两句都和“路线延误”有关，第三句和“燃油成本”有关
sentences = [
    "Route B has serious delay problems.",
    "Which route often arrives late?",
    "Truck T001 has high fuel cost."
]


# 把句子转换成 embedding 向量
# 结果形状是：句子数量 x 向量维度
embeddings = model.encode(sentences)


# 查看 embedding 的形状
# 这里应该输出 (3, 384)，表示 3 个句子，每个句子 384 维
print("Embedding shape:", embeddings.shape)


# 打印第一句话 embedding 的前 5 个数字
# 向量本身不需要人工理解，只要知道它代表句子的语义
print("First sentence embedding first 5 numbers:")
print(embeddings[0][:5])


# 计算第 1 句和第 2 句的语义相似度
# 这两句都和 route delay 有关，所以分数应该更高
similarity_1 = util.cos_sim(embeddings[0], embeddings[1])


# 计算第 1 句和第 3 句的语义相似度
# 第 3 句是 fuel cost，主题不同，所以分数应该更低
similarity_2 = util.cos_sim(embeddings[0], embeddings[2])


print("Similarity between sentence 1 and 2:")
print(similarity_1)

print("Similarity between sentence 1 and 3:")
print(similarity_2)