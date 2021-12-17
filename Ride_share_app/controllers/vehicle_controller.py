from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.vehicles import Vehicle
from schemas.vehicle_schema import vehicles_schema, vehicle_schema
from flask_login import login_required, current_user
import boto3
from random import randint
from sqlalchemy import exc

vehicles = Blueprint('vehicles', __name__)

# This one is just a placeholder for now, no CRUD here
@vehicles.route('/')
@login_required
def homepage():
    data = {
        "page_title": "Homepage"
    }
    return render_template("homepage.html", page_data=data)

# The GET routes endpoint
@vehicles.route("/vehicles/", methods=["GET"])
def get_vehicles():
    data = {
        "page_title": "Vehicle Index",
        "vehicles": vehicles_schema.dump(Vehicle.query.order_by(Vehicle.driver_id.asc()).all())
    }
    return render_template("vehicle_index.html", page_data=data)

# The POST route endpoint
@vehicles.route("/vehicles/", methods=["POST"])
@login_required
def create_vehicle():
    new_vehicle=vehicle_schema.load(request.form)
    if not current_user.drivers:
        abort(403, "You need to register as a driver")
    if current_user.drivers[0].vehicles:
        abort(403, "You can only register one vehicle per driver")
    new_vehicle.vehicle_driver = current_user.drivers[0]        
    try:
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for("vehicles.get_vehicles"))
    except exc.IntegrityError:
        db.session.rollback()
        data = {
            "page_title": "Vehicle Index",
            "vehicles": vehicles_schema.dump(Vehicle.query.all()),
            "rego_error": "rego is already in use. Please enter different registration "}
        return render_template("vehicle_index.html", page_data=data)


# An endpoint to GET info about a specific vehicle
@vehicles.route("/vehicles/<int:id>/", methods = ["GET"])
@login_required
def get_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)

    data = {
        "page_title": "Vehicle Detail",
        "vehicle": vehicle_schema.dump(vehicle),
        # "image": image_url
    }
    return render_template("vehicle_detail.html", page_data=data)

# A PUT/PATCH route to update vehicle info
@vehicles.route("/vehicles/<int:id>/", methods=["POST"])
@login_required
def update_vehicle(id):
    vehicle = Vehicle.query.filter_by(vehicle_id=id)

    if current_user.drivers[0].driver_id != vehicle.first().vehicle_driver.driver_id:
        abort(403, "This Vehicle does not belong to you. You do not have permission")

    updated_fields = vehicle_schema.dump(request.form)
    if updated_fields:
        vehicle.update(updated_fields)
        db.session.commit()

    data = {
        "page_title": "Vehicle Detail",
        "vehicle": vehicle_schema.dump(vehicle.first())
    }
    return render_template("vehicle_detail.html", page_data=data)

@vehicles.route("/vehicles/<int:id>/accept/", methods=["POST"])
@login_required
def accept_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    vehicle.acceptor = current_user.drivers[0]
    db.session.commit()
    return redirect(url_for("vehicles.get_vehicles"))

@vehicles.route("/vehicles/<int:id>/drop/", methods=["POST"])
@login_required
def drop_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    vehicle.students.remove(current_user)
    db.session.commit()
    return redirect(url_for('riders.rider_detail'))

@vehicles.route("/vehicles/<int:id>/delete/", methods=["POST"])
@login_required
def delete_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)

    if current_user.drivers[0].driver_id != vehicle.vehicle_driver.driver_id:
        abort(403, "This Vehicle does not belong to you. You do not have permission to delete it")

    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for("vehicles.get_vehicles"))