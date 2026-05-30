# 从 Flask 框架中导入需要用到的工具
# Flask：用来创建网页应用
# render_template：用来显示 HTML 页面
# request：用来接收网页表单提交的数据
from flask import Flask, render_template, request

# 从我们自己写的 fleetmind_core.py 中导入核心功能
# 这样 app.py 只负责网页控制，不负责具体计算逻辑
from fleetmind_core import (
    Truck,
    create_sample_trucks,
    save_analysis_history,
    save_truck_to_csv,
    read_trucks_from_csv,
    read_analysis_history,
    compare_trucks,
    get_ai_response,
    get_dashboard_data
)


# 创建一个 Flask 应用对象
# __name__ 代表当前这个 Python 文件
app = Flask(__name__)


# 首页 route
# 当用户访问 http://127.0.0.1:5000/ 时，会运行这个函数
@app.route("/")
def index():
    # 显示 templates 文件夹中的 index.html 首页
    return render_template("index.html")


# 样本车辆列表页面
# 当用户访问 /samples 时，会显示所有匿名化样本车辆
@app.route("/samples")
def samples():
    # 调用 fleetmind_core.py 中的函数，创建 12 辆样本车
    trucks = create_sample_trucks()

    # 把 trucks 传给 samples.html，让网页循环显示这些车辆
    return render_template("samples.html", trucks=trucks)


# 单辆样本车分析页面
# <int:truck_index> 表示网址里会接收一个整数编号
# 例如 /sample/0 表示分析第 1 辆车，/sample/1 表示分析第 2 辆车
@app.route("/sample/<int:truck_index>")
def sample_detail(truck_index):
    # 先创建所有样本车
    trucks = create_sample_trucks()

    # 判断用户点击的编号是否在合理范围内
    if 0 <= truck_index < len(trucks):
        # 根据编号取出对应的那一辆车
        truck = trucks[truck_index]

        # 保存这辆车的分析记录到 fleet_history.txt
        saved = save_analysis_history(truck)

        # 把 truck 和 saved 传给 result.html 显示详细分析结果
        return render_template(
            "result.html",
            truck=truck,
            saved=saved
        )

    # 如果编号不合法，显示错误信息
    return "Truck not found."


# 添加并分析新车页面
# GET：用户打开页面时显示表单
# POST：用户提交表单后处理数据
@app.route("/new-truck", methods=["GET", "POST"])
def new_truck():
    # 如果用户点击提交按钮，网页会发送 POST 请求
    if request.method == "POST":
        # 从网页表单中读取文字信息
        truck_id = request.form["truck_id"]
        driver = request.form["driver"]
        route = request.form["route"]

        # 从网页表单中读取数字信息
        # request.form 读出来默认是字符串，所以要用 float() 转成数字
        revenue = float(request.form["revenue"])
        fuel_cost = float(request.form["fuel_cost"])
        toll_cost = float(request.form["toll_cost"])
        repair_cost = float(request.form["repair_cost"])
        salary_cost = float(request.form["salary_cost"])
        insurance_cost = float(request.form["insurance_cost"])
        other_cost = float(request.form["other_cost"])

        # 用用户输入的数据创建一个 Truck 对象
        truck = Truck(
            truck_id,
            driver,
            route,
            revenue,
            fuel_cost,
            toll_cost,
            repair_cost,
            salary_cost,
            insurance_cost,
            other_cost
        )

        # 保存新车分析记录到 fleet_history.txt
        saved = save_analysis_history(truck)

        # 保存新车结构化数据到 fleet_data.csv
        csv_saved = save_truck_to_csv(truck)
        # 为了debug用的
        print("CSV saved:", csv_saved)

        # 跳转到 result.html，显示这辆新车的分析结果
        return render_template(
            "result.html",
            truck=truck,
            saved=saved,
            csv_saved=csv_saved
        )

    # 如果用户只是打开 /new-truck 页面，就显示输入表单
    return render_template("new_truck.html")


# 比较所有样本车辆页面
@app.route("/compare")
def compare():
    # 创建样本车辆数据
    trucks = create_sample_trucks()

    # 调用 compare_trucks()，按利润率从高到低排序
    # sorted_trucks：排序后的所有车辆
    # best_truck：表现最好的车辆
    # highest_risk_truck：利润率最低、风险最高的车辆
    sorted_trucks, best_truck, highest_risk_truck = compare_trucks(trucks)

    # 把比较结果传给 compare.html 显示
    return render_template(
        "compare.html",
        trucks=sorted_trucks,
        best_truck=best_truck,
        highest_risk_truck=highest_risk_truck
    )


# AI keyword assistant 页面
# GET：用户打开页面
# POST：用户提交问题
@app.route("/assistant", methods=["GET", "POST"])
def assistant():
    # 默认情况下，还没有回答
    answer = None
    question = ""

    # 如果用户提交了问题
    if request.method == "POST":
        # 从表单中读取用户问题
        question = request.form["question"]

        # 调用 keyword-based assistant，生成回答
        answer = get_ai_response(question)

    # 把问题和回答传给 assistant.html 显示
    return render_template(
        "assistant.html",
        question=question,
        answer=answer
    )


# 历史记录页面
@app.route("/history")
def history():
    # 读取 fleet_history.txt 里的所有历史分析记录
    history_text = read_analysis_history()

    # 把历史记录传给 history.html 显示
    return render_template("history.html", history_text=history_text)

# csv 车辆记录页面
@app.route("/records")
def records():
    # 从fleet_data.csv读取新增车辆记录
    records = read_trucks_from_csv()

    # 吧records传给records.html显示
    return render_template("records.html", records=records)

# 用户访问 /records
# Flask 调用 read_trucks_from_csv()
# 读取 fleet_data.csv
# 把 records 传给 records.html

# dashboard页面
@app.route("/dashboard")
def dashboard():
    # 读取csv并计算dashboard数据
    data = get_dashboard_data()
    # 把dashboard数据传给网页
    return render_template("dashboard.html", data=data)


# 程序入口
# 只有直接运行 app.py 时，Flask 才会启动
if __name__ == "__main__":
    # debug=True 表示开发模式
    # 修改代码后通常会自动重启，也方便查看错误信息
    app.run(debug=True, port=5001)
    