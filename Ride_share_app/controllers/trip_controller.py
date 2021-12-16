from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.trips import Trip
from schemas.trip_schema import trips_schema, trip_schema
from flask_login import login_required, current_user
import boto3
from random import randint

trips = Blueprint('trips', __name__)

# This one is just a placeholder for now, no CRUD here
@trips.route('/')
def homepage():
    data = {
        "page_title": "Homepage"
    }
    return render_template("homepage.html", page_data=data)

# The GET routes endpoint
@trips.route("/trips/", methods=["GET"])
def get_trips():
    data = {
        "page_title": "Trip Index",
        "trips": trips_schema.dump(Trip.query.order_by(Trip.driver_id.desc()).all())
    }
    return render_template("trip_index.html", page_data=data)

# The POST route endpoint
@trips.route("/trips/", methods=["POST"])
@login_required
def create_trip():
    new_trip=trip_schema.load(request.form)

    new_trip.creator = current_user.riders[0]        
    # Creates a random cost for the course.
    new_trip.cost = randint(20, 100) 

    db.session.add(new_trip)
    db.session.commit()

    return redirect(url_for("trips.get_trips"))

# An endpoint to GET info about a specific trip
@trips.route("/trips/<int:id>/", methods = ["GET"])
def get_trip(id):
    trip = Trip.query.get_or_404(id)

    # s3_client=boto3.client("s3")
    # bucket_name=current_app.config["AWS_S3_BUCKET"]
    # image_url = s3_client.generate_presigned_url(
    #     'get_object',
    #     Params={
    #         "Bucket": bucket_name,
    #         "Key": trip.image_filename
    #     },
    #     ExpiresIn=100
    # )

    data = {
        "page_title": "Trip Detail",
        "trip": trip_schema.dump(trip),
        # "image": image_url
    }
    return render_template("trip_detail.html", page_data=data)

# A PUT/PATCH route to update trip info
@trips.route("/trips/<int:id>/", methods=["POST"])
@login_required
def update_trip(id):
    trip = Trip.query.filter_by(trip_id=id)

    if current_user.id != trip.first().creator_id:
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
    trip = Trip.query.get_or_404(id)
    trip.acceptor = current_user.drivers[0]
    db.session.commit()
    return redirect(url_for("trips.get_trips"))

@trips.route("/trips/<int:id>/drop/", methods=["POST"])
@login_required
def drop_trip(id):
    trip = Trip.query.get_or_404(id)
    trip.students.remove(current_user)
    db.session.commit()
    return redirect(url_for('riders.rider_detail'))

@trips.route("/trips/<int:id>/delete/", methods=["POST"])
@login_required
def delete_trip(id):
    trip = Trip.query.get_or_404(id)

    if current_user.id != trip.creator_id:
        abort(403, "You do not have permission to delete this trip!")

    db.session.delete(trip)
    db.session.commit()
    return redirect(url_for("trips.get_trips"))