import torch

# 一维 tensor：像一个数字列表
a = torch.tensor([1, 2, 3])

print("a =", a)
print("a shape =", a.shape)


# 二维 tensor：像一个表格 / 矩阵
b = torch.tensor([
    [1, 2, 3],
    [4, 5, 6]
])

print("b =")
print(b)
print("b shape =", b.shape)


# tensor 可以直接做数学运算
c = a + 10
print("a + 10 =", c)


# 两个向量可以做点乘
x = torch.tensor([1.0, 2.0, 3.0])
y = torch.tensor([2.0, 2.0, 2.0])

dot_product = torch.dot(x, y)

print("dot product =", dot_product)


import torch.nn.functional as F


# cosine similarity：判断两个向量方向像不像
query = torch.tensor([1.0, 1.0, 0.0])

doc_a = torch.tensor([1.0, 1.0, 0.0])  # 和 query 方向完全一样
doc_b = torch.tensor([0.0, 1.0, 1.0])  # 和 query 有一部分相似
doc_c = torch.tensor([-1.0, -1.0, 0.0])  # 和 query 方向相反

score_a = F.cosine_similarity(query, doc_a, dim=0)
score_b = F.cosine_similarity(query, doc_b, dim=0)
score_c = F.cosine_similarity(query, doc_c, dim=0)

print("score A =", score_a)
print("score B =", score_b)
print("score C =", score_c)


# mini semantic search：模拟用户问题和知识库片段的匹配
query_embedding = torch.tensor([1.0, 1.0, 0.0])

documents = [
    {
        "text": "Route B has serious delay problems.",
        "embedding": torch.tensor([1.0, 1.0, 0.0])
    },
    {
        "text": "Truck T03 has high fuel cost.",
        "embedding": torch.tensor([0.0, 0.2, 1.0])
    },
    {
        "text": "Route C is stable and profitable.",
        "embedding": torch.tensor([-1.0, -1.0, 0.0])
    }
]

results = []

for doc in documents:
    score = F.cosine_similarity(query_embedding, doc["embedding"], dim=0)

    results.append({
        "text": doc["text"],
        "score": round(float(score), 4)
    })

results = sorted(results, key=lambda item: item["score"], reverse=True)

print("Semantic Search Results:")

for result in results:
    print(result["score"], "-", result["text"])