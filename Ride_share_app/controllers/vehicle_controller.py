from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.vehicles import Vehicle
from schemas.vehicle_schema import vehicles_schema, vehicle_schema
from flask_login import login_required, current_user
import boto3
from random import randint
from sqlalchemy import exc

vehicles = Blueprint('vehicles', __name__)


@vehicles.route("/vehicles/", methods=["GET"])
def get_vehicles():
    """This will display a list of vehicles that have been created.
    args:       Takes in GET requests
    returns:    Displays a list of vehicles.
    Raises:     None
    """
    data = {
        "page_title": "Vehicle Index",
        "vehicles": vehicles_schema.dump(Vehicle.query.order_by(Vehicle.driver_id.asc()).all())
    }
    return render_template("vehicle_index.html", page_data=data)

@vehicles.route("/vehicles/", methods=["POST"])
@login_required
def create_vehicle():
    """This will allows Drivers to save a vehicle.
    args:       Takes in POST requests
    returns:    Loads user input to the Trip Schema to create a new vehicle.
    Raises:     If users does not have a drivers account it will redirect them to the 
                    create drivers page.

                403 page will be raised If the user has already got a vehicle saved against
                    their driver profile. 

                If the vehicle registration has already been save to the data base, the page
                    will reload notifying the driver that the registration is already in use. 
    """
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
            "rego_error": "registration is already in use. Please enter different registration "}
        return render_template("vehicle_index.html", page_data=data)


@vehicles.route("/vehicles/<int:id>/", methods = ["GET"])
@login_required
def get_vehicle(id):
    """This will Display the vehicles information.
    args:       Takes in GET requests
    returns:    Loads vehicle detail's page with the selected vehicle details from the database.
    """
    vehicle = Vehicle.query.get_or_404(id)

    data = {
        "page_title": "Vehicle Detail",
        "vehicle": vehicle_schema.dump(vehicle),
        # "image": image_url
    }
    return render_template("vehicle_detail.html", page_data=data)


@vehicles.route("/vehicles/<int:id>/", methods=["POST"])
@login_required
def update_vehicle(id):
    """This will allows drivers to update their vehicle details.
    args:       Takes in the updated vehicle details as a POST requests.
    returns:    Loads user input to the Vehicle Schema to update vehicle information.
    Raises:     If users is not the driver who created the vehicle, the user will be directed
                to a 403 page notifying them they do not have permission to alter this vehicle.
    """
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


@vehicles.route("/vehicles/<int:id>/delete/", methods=["POST"])
@login_required
def delete_vehicle(id):
    """This will delete vehicles information from database.
    args:       Takes in the drivers ID number that is requesting to deleted trip and 
                will verify that the driver deleting the vehicle was the creator of the vehicle. 
    returns:    Loads vehicle index page .
    Raises:     Takes in the drivers ID number that is requesting to deleted trip and 
                will verify that the riders deleting the trip was the creator. If they dont match
                it will bring up a 403 page notifying the user they do not have permission to 
                delete the trip.
    """
    vehicle = Vehicle.query.get_or_404(id)

    if current_user.drivers[0].driver_id != vehicle.vehicle_driver.driver_id:
        abort(403, "This Vehicle does not belong to you. You do not have permission to delete it")

    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for("vehicles.get_vehicles"))