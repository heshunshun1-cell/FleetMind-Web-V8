import json

from flask import Blueprint, render_template, request

from rag_engine import ask_rag


# RAG 路由模块：管理知识库问答助手页面
rag_bp = Blueprint("rag", __name__)


# RAG Assistant 页面
@rag_bp.route("/rag", methods=["GET", "POST"])
def rag_assistant():
    answer = None
    structured_answer = None
    sources = []
    results = []
    generated_prompt = ""
    question = ""

    # 用户提交问题后，调用 RAG 引擎生成回答
    if request.method == "POST":
        question = request.form.get("question", "")

        # 避免空问题触发检索
        if question.strip() != "":
            response = ask_rag(question)

            answer = response["answer"]
            sources = response["sources"]
            results = response["results"]
            generated_prompt = response["generated_prompt"]

            # 尝试把 JSON 字符串解析成结构化答案
            try:
                structured_answer = json.loads(answer)
            except json.JSONDecodeError:
                # 如果模型没有返回合法 JSON，就保留原始文本作为 fallback
                structured_answer = None

    # 把问题、结构化回答、原始回答、证据和 prompt 传给页面
    return render_template(
        "rag.html",
        question=question,
        answer=answer,
        structured_answer=structured_answer,
        sources=sources,
        results=results,
        generated_prompt=generated_prompt
    )