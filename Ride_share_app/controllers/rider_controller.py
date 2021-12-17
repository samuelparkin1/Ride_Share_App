from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.riders import Rider
from controllers.user_controller import user_detail
from schemas.rider_schema import riders_schema, rider_schema
from flask_login import login_required, current_user
import boto3
from random import randint

riders = Blueprint('riders', __name__)

# This one is just a placeholder for now, no CRUD here
@riders.route('/')
@login_required
def homepage():
    data = {
        "page_title": "Homepage"
    }
    return render_template("homepage.html", page_data=data)

# The GET routes endpoint
@riders.route("/riders/", methods=["GET"])
@login_required
def get_riders():
    data = {
        "page_title": "Rider Index",
        "riders": riders_schema.dump(Rider.query.all())
    }
    return render_template("rider_index.html", page_data=data)

# The POST route endpoint
@riders.route("/riders/", methods=["POST"])
@login_required
def create_rider():
    if current_user.riders:
            data = {
                "riders": riders_schema.dump(Rider.query.all()),
                "existing_rider_error": "You are already a registered rider"
                }
            return render_template("rider_index.html", page_data=data)

    new_rider=rider_schema.load(request.form)

    new_rider.user_id = current_user

    db.session.add(new_rider)
    db.session.commit()

    return redirect(url_for('users.user_detail'))

# An endpoint to GET info about a specific rider
@riders.route("/riders/<int:id>/", methods = ["GET"])
@login_required
def get_rider(id):
    rider = Rider.query.get_or_404(id)

    # s3_client=boto3.client("s3")
    # bucket_name=current_app.config["AWS_S3_BUCKET"]
    # image_url = s3_client.generate_presigned_url(
    #     'get_object',
    #     Params={
    #         "Bucket": bucket_name,
    #         "Key": rider.image_filename
    #     },
    #     ExpiresIn=100
    # )

    data = {
        "page_title": "Rider Detail",
        "rider": rider_schema.dump(rider),
        # "image": image_url
    }
    return render_template("rider_detail.html", page_data=data)

# A PUT/PATCH route to update rider info
@riders.route("/riders/<int:id>/", methods=["POST"])
@login_required
def update_rider(id):
    rider = Rider.query.filter_by(rider_id=id)

    if current_user.id != rider.first().user_profile:
        abort(403, "You do not have permission to alter this rider!")

    updated_fields = rider_schema.dump(request.form)
    if updated_fields:
        rider.update(updated_fields)
        db.session.commit()

    data = {
        "page_title": "Rider Detail",
        "rider": rider_schema.dump(rider.first())
    }
    return render_template("rider_detail.html", page_data=data)


@riders.route("/riders/<int:id>/drop/", methods=["POST"])
@login_required
def drop_rider(id):
    rider = Rider.query.get_or_404(id)
    rider.students.remove(current_user)
    db.session.commit()
    return redirect(url_for('users.user_detail'))

@riders.route("/riders/<int:id>/delete/", methods=["POST"])
@login_required
def delete_rider(id):
    rider = Rider.query.get_or_404(id)

    if current_user.id != rider.user_profile:
        abort(403, "You do not have permission to delete this rider!")

    db.session.delete(rider)
    db.session.commit()
    return redirect(url_for('users.user_detail'))