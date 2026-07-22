from flask import Blueprint, render_template, request, redirect

from database import (
    read_trips_from_db,
    get_trip_summary_from_db,
    generate_trip_insights_from_db,
    save_trip_to_db,
    read_trucks_from_db,
    get_trip_by_id_from_db,
    update_trip_in_db,
    delete_trip_from_db
)

# Trip 路由模块：管理运输任务记录页面
trip_bp = Blueprint("trip", __name__)


# 运输任务记录页面
@trip_bp.route("/trips")
def trips():
    # 从 SQLite 数据库读取所有 trip records
    trips = read_trips_from_db()

    # 计算 trip summary
    summary = get_trip_summary_from_db()

    # 生成 trip-level 运营建议
    trip_insights = generate_trip_insights_from_db()

    # 把数据传给 trips.html
    return render_template(
        "trips.html",
        trips=trips,
        summary=summary,
        trip_insights=trip_insights
    )

    # 添加运输任务页面
@trip_bp.route("/add-trip", methods=["GET", "POST"])
def add_trip():
    # 用户提交表单时，保存新 trip
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

        # 保存到 SQLite 数据库
        save_trip_to_db(trip_data)

        # 保存后返回 Trip Records 页面
        return redirect("/trips")

    # 打开表单时，读取已有车辆用于下拉选择
    trucks = read_trucks_from_db()

    return render_template("add_trip.html", trucks=trucks)


# 编辑运输任务页面
@trip_bp.route("/edit-trip/<trip_id>", methods=["GET", "POST"])
def edit_trip(trip_id):
    # 根据 trip_id 读取当前 trip 数据
    trip = get_trip_by_id_from_db(trip_id)

    # 如果找不到这条 trip，返回 Trip Records 页面
    if trip is None:
        return redirect("/trips")

    # 用户提交修改表单时，更新 trip 数据
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

        # 更新 SQLite 数据库中的 trip
        update_trip_in_db(trip_id, trip_data)

        # 修改后返回 Trip Records 页面
        return redirect("/trips")

    # 首次打开页面时，显示当前 trip 数据
    return render_template("edit_trip.html", trip=trip)


# 删除运输任务
@trip_bp.route("/delete-trip/<trip_id>")
def delete_trip(trip_id):
    # 根据 trip_id 删除 trip
    delete_trip_from_db(trip_id)

    # 删除后返回 Trip Records 页面
    return redirect("/trips")