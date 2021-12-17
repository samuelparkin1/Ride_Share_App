from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.trips import Trip
from schemas.trip_schema import trips_schema, trip_schema
from flask_login import login_required, current_user
import boto3
from random import randint

trips = Blueprint('trips', __name__)


@trips.route("/trips/", methods=["GET"])
@login_required
def get_trips():
    """This will display a list of Trips that have been created.

    args:       Takes in GET requests

    returns:    Displays a list of trips.
    
    Raises:     None
    """
    data = {
        "page_title": "Trips ",
        "trips": trips_schema.dump(Trip.query.order_by(Trip.driver_id.desc()).all())
    }
    return render_template("trip_index.html", page_data=data)


@trips.route("/trips/", methods=["POST"])
@login_required
def create_trip():
    """This will allows riders to become create trips.

    args:       Takes in POST requests

    returns:    Loads user input to the Trip Schema to create a new trip.
                creates a random cost for the trip 
    
    Raises:     If users does not have a riders account it will redirect them to the 
                create riders page.
    """
    if not current_user.riders:
        error = {"error_message": "You need to become a rider before creating a trip"}
        return render_template ("rider_index.html", page_data = error)

    new_trip=trip_schema.load(request.form)

    new_trip.creator = current_user.riders[0]        
    # Creates a random cost for the trip.
    new_trip.cost = randint(20, 100) 

    db.session.add(new_trip)
    db.session.commit()

    return redirect(url_for("trips.get_trips"))

# An endpoint to GET info about a specific trip
@trips.route("/trips/<int:id>/", methods = ["GET"])
@login_required
def get_trip(id):
    """This will Display the drivers information.

    args:       Takes in GET requests

    returns:    Loads trip detail's page with the selected trips details from the database.
    """
    trip = Trip.query.get_or_404(id)
    data = {
        "page_title": "Trip Detail",
        "trip": trip_schema.dump(trip),
    }
    return render_template("trip_detail.html", page_data=data)


@trips.route("/trips/<int:id>/", methods=["POST"])
@login_required
def update_trip(id):
    """This will allows riders to update current trips.

    args:       Takes in the updated trip details as a POST requests.

    returns:    Loads user input to the Trip Schema to create a new trip.
                creates a random cost for the trip 
    
    Raises:     If users is not the rider who created the trip, the user will be directed
                to a 403 page notifying them they do not have permission to alter this trip.
    """
    trip = Trip.query.filter_by(trip_id=id)

    if current_user.riders[0].rider_id != trip.first().creator.rider_id:
        abort(403, "You do not have permission to alter this trip!")

    updated_fields = trip_schema.dump(request.form)
    if updated_fields:
        trip.first().cost = randint(20, 100) 
        trip.update(updated_fields)
        db.session.commit()

    data = {
        "page_title": "Trip Detail",
        "trip": trip_schema.dump(trip.first())
    }
    return render_template("trip_detail.html", page_data=data)

@trips.route("/trips/<int:id>/accept/", methods=["POST"])
@login_required
def accept_trip(id):
    """This will allows riders to become create trips.

    args:       Takes in POST requests

    returns:    Loads user input to the Trip Schema to accept a trip.

    Raises:     If users does not have a drivers account it will redirect them to the 
                create drivers page.
    """
    trip = Trip.query.get_or_404(id)
    if current_user.drivers:
        trip.acceptor = current_user.drivers[0]
        db.session.commit()
        return redirect(url_for("trips.get_trips"))

    error = {"error_message": "You need to become a Driver before accepting a trip"}
    return render_template ("driver_index.html", page_data = error)

@trips.route("/trips/<int:id>/delete/", methods=["POST"])
@login_required
def delete_trip(id):
    """This will delete drivers information from database.

    args:       Takes in the riders ID number that is requesting to deleted trip and 
                will verify that the riders deleting the trip was the creator. 

    returns:    Loads trip index page .

    Raises:     Takes in the riders ID number that is requesting to deleted trip and 
                will verify that the riders deleting the trip was the creator, it will 
                bring up a 403 page notifying the user they do not have permission to 
                delete the trip.
    """
    trip = Trip.query.get_or_404(id)

    if current_user.riders[0] != trip.creator:
        abort(403, "You do not have permission to delete this trip!")
    if trip.acceptor:
        abort(403, "You are unable to delete ride because the trip has already been accepted!")

    db.session.delete(trip)
    db.session.commit()
    return redirect(url_for("trips.get_trips"))