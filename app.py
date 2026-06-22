# 从 Flask 框架中导入需要用到的工具
# Flask：用来创建网页应用
# render_template：用来显示 HTML 页面
# request：用来接收网页表单提交的数据
from flask import Flask, render_template, request, redirect
from database import (
    read_trucks_from_db,
    get_dashboard_data_from_db,
    get_analytics_summary_from_db,
    get_loss_making_trucks_from_db,
    generate_revenue_chart_from_db,
    generate_profit_chart_from_db,
    generate_risk_chart_from_db,
    generate_cost_pressure_chart_from_db,
    generate_insights_from_db,
    save_truck_to_db,
    read_trips_from_db,
    get_trip_summary_from_db,
    generate_trip_insights_from_db,
    get_route_analytics_from_db,
    generate_route_insights_from_db,
    get_route_summary_from_db,
    save_trip_to_db,
    get_trip_by_id_from_db,
    update_trip_in_db,
    delete_trip_from_db,
    get_truck_by_id_from_db,
    update_truck_in_db,
    delete_truck_from_db
)

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
    get_dashboard_data,
    generate_revenue_chart,
    generate_profit_chart,
    generate_risk_chart,
    generate_cost_pressure_chart,
    get_analytics_summary,
    get_loss_making_trucks
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
        
        # 保存新车结构化数据到 SQLite 数据库
        db_saved = save_truck_to_db(truck)

        # 为了 debug 用
        print("Database saved:", db_saved)

        # 跳转到 result.html，显示这辆新车的分析结果
        return render_template("result.html", 
                               truck=truck, 
                               saved=saved, 
                               db_saved=db_saved)

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
    # 从 SQLite 数据库读取新增车辆记录
    records = read_trucks_from_db()

    # 吧records传给records.html显示
    return render_template("records.html", records=records)

# 用户访问 /records
# Flask 调用 read_trucks_from_csv()
# 读取 fleet_data.csv
# 把 records 传给 records.html

@app.route("/edit-truck/<truck_id>", methods=["GET", "POST"])
def edit_truck(truck_id):
    # 根据 truck_id 读取当前 truck 数据
    truck = get_truck_by_id_from_db(truck_id)

    # 如果找不到这辆车，返回 Truck Records 页面
    if truck is None:
        return redirect("/records")

    # 如果用户提交了修改表单
    if request.method == "POST":
        truck_data = {
            "driver": request.form["driver"],
            "route": request.form["route"],
            "revenue": request.form["revenue"],
            "fuel_cost": request.form["fuel_cost"],
            "toll_cost": request.form["toll_cost"],
            "repair_cost": request.form["repair_cost"],
            "salary_cost": request.form["salary_cost"],
            "insurance_cost": request.form["insurance_cost"],
            "other_cost": request.form["other_cost"]
        }

        # 更新 truck 数据
        update_truck_in_db(truck_id, truck_data)

        # 修改后返回 Truck Records 页面
        return redirect("/records")

    # 如果只是打开页面，显示编辑表单
    return render_template("edit_truck.html", truck=truck)


@app.route("/delete-truck/<truck_id>")
def delete_truck(truck_id):
    # 根据 truck_id 删除 truck
    delete_truck_from_db(truck_id)

    # 删除后返回 Truck Records 页面
    return redirect("/records")


# dashboard页面
@app.route("/dashboard")
def dashboard():
    # 从 SQLite 数据库读取并计算 dashboard 数据
    data = get_dashboard_data_from_db()
    # 把dashboard数据传给网页
    return render_template("dashboard.html", data=data)

# 分析图表页面
@app.route("/analytics")
def analytics():
    # 从 SQLite 数据库生成四张 analytics 图表
    generate_revenue_chart_from_db()
    generate_profit_chart_from_db()
    generate_risk_chart_from_db()
    generate_cost_pressure_chart_from_db()

    # 从 SQLite 数据库获取 analytics 页面汇总数据
    summary = get_analytics_summary_from_db()

    # 从 SQLite 数据库获取亏损车辆数据
    loss_trucks = get_loss_making_trucks_from_db()

    return render_template(
        "analytics.html",
        summary=summary,
        loss_trucks=loss_trucks
    )

# 运营建议页面
@app.route("/insights")
def insights():
    # 从 SQLite 数据库生成运营建议
    insights = generate_insights_from_db()
    # 把建议传给 insight.html 页面
    return render_template("insights.html", insights=insights)

# 运输任务记录页面
@app.route("/trips")
def trips():
    # 从 SQLite 数据库读取所有 trip records
    trips = read_trips_from_db()

    # 从SQLite 计算 trip summary
    summary = get_trip_summary_from_db()

    # 从 SQLite 生成trip-level insights
    trip_insights = generate_trip_insights_from_db()

    # 把 trips 传给 trips.html 显示
    return render_template(
        "trips.html", 
        trips=trips,
        summary=summary,
        trip_insights=trip_insights
        )

@app.route("/add-trip", methods=["GET", "POST"])
def add_trip():
    # 如果用户提交了表单
    if request.method == "POST":
        trip_data = {
            "trip_id": request.form["trip_id"],
            "truck_id": request.form["truck_id"],
            "driver": request.form["driver"],
            "route": request.form["route"],
            "distance": request.form["distance"],
            "revenue": request.form["revenue"],
            "total_cost": request.form["total_cost"],
            "delay_hours": request.form["delay_hours"],
            "trip_date": request.form["trip_date"]
        }

        # 保存新 trip 到 SQLite 数据库
        save_trip_to_db(trip_data)

        # 保存后跳转到 Trip Records 页面查看结果
        return redirect("/trips")

    # 从数据库读取已有 truck records
    trucks = read_trucks_from_db()

    # 把 trucks 传给 add_trip.html，用来生成 Truck ID 下拉菜单
    return render_template("add_trip.html", trucks=trucks)

@app.route("/edit-trip/<trip_id>", methods=["GET", "POST"])
def edit_trip(trip_id):
    # 根据 trip_id 读取当前 trip 数据
    trip = get_trip_by_id_from_db(trip_id)

    # 如果找不到这条 trip，返回 Trip Records 页面
    if trip is None:
        return redirect("/trips")

    # 如果用户提交了修改表单
    if request.method == "POST":
        trip_data = {
            "truck_id": request.form["truck_id"],
            "driver": request.form["driver"],
            "route": request.form["route"],
            "distance": request.form["distance"],
            "revenue": request.form["revenue"],
            "total_cost": request.form["total_cost"],
            "delay_hours": request.form["delay_hours"],
            "trip_date": request.form["trip_date"]
        }

        # 更新 trip 数据
        update_trip_in_db(trip_id, trip_data)

        # 修改后返回 Trip Records 页面
        return redirect("/trips")

    # 如果只是打开页面，显示编辑表单
    return render_template("edit_trip.html", trip=trip)


@app.route("/delete-trip/<trip_id>")
def delete_trip(trip_id):
    # 根据 trip_id 删除 trip
    delete_trip_from_db(trip_id)

    # 删除后返回 Trip Records 页面
    return redirect("/trips")

@app.route("/route-analytics")
def route_analytics():
    # 从 SQLite 数据库获取路线分析数据
    routes = get_route_analytics_from_db()

    # 获取路线 summary cards 数据
    route_summary = get_route_summary_from_db()

    # 根据路线数据生成运营建议
    route_insights = generate_route_insights_from_db()

    # 把路线分析数据和建议传给 HTML 页面
    return render_template(
        "route_analytics.html",
        routes=routes,
        route_summary=route_summary,
        route_insights=route_insights
    )




# 程序入口
# 只有直接运行 app.py 时，Flask 才会启动
if __name__ == "__main__":
    # debug=True 表示开发模式
    # 修改代码后通常会自动重启，也方便查看错误信息
    app.run(debug=True, port=5001)
    