from flask import Blueprint, render_template, request, redirect

from database import (
    read_trucks_from_db,
    get_truck_by_id_from_db,
    update_truck_in_db,
    delete_truck_from_db
)


# Truck 路由模块：管理车辆记录页面
truck_bp = Blueprint("truck", __name__)


# 车辆记录页面
@truck_bp.route("/records")
def records():
    # 从 SQLite 数据库读取车辆记录
    records = read_trucks_from_db()

    # 把车辆记录传给页面
    return render_template("records.html", records=records)


# 编辑车辆记录页面
@truck_bp.route("/edit-truck/<truck_id>", methods=["GET", "POST"])
def edit_truck(truck_id):
    # 根据 truck_id 读取当前车辆数据
    truck = get_truck_by_id_from_db(truck_id)

    # 如果找不到车辆，返回车辆记录页面
    if truck is None:
        return redirect("/records")

    # 用户提交修改表单时，更新车辆数据
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

        # 更新 SQLite 数据库中的车辆记录
        update_truck_in_db(truck_id, truck_data)

        # 修改后返回车辆记录页面
        return redirect("/records")

    # 首次打开页面时，显示当前车辆数据
    return render_template("edit_truck.html", truck=truck)

# 删除车辆记录
@truck_bp.route("/delete-truck/<truck_id>")
def delete_truck(truck_id):
    # 根据 truck_id 删除车辆记录
    delete_truck_from_db(truck_id)

    # 删除后返回车辆记录页面
    return redirect("/records")