from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.drivers import Driver
from controllers.user_controller import user_detail
from schemas.driver_schema import drivers_schema, driver_schema
from flask_login import login_required, current_user
import boto3
from random import randint

drivers = Blueprint('drivers', __name__)

# This one is just a placeholder for now, no CRUD here
@drivers.route('/')
def homepage():
    data = {
        "page_title": "Homepage"
    }
    return render_template("homepage.html", page_data=data)

# The GET routes endpoint
@drivers.route("/drivers/", methods=["GET"])
def get_drivers():
    data = {
        "page_title": "Driver Index",
        "drivers": drivers_schema.dump(Driver.query.all())
    }
    return render_template("driver_index.html", page_data=data)

# The POST route endpoint
@drivers.route("/drivers/", methods=["POST"])
@login_required
def create_driver():
    new_driver=driver_schema.load(request.form)

    new_driver.user_id = current_user

    db.session.add(new_driver)
    db.session.commit()

    return redirect(url_for('users.user_detail'))

# An endpoint to GET info about a specific driver
@drivers.route("/drivers/<int:id>/", methods = ["GET"])
def get_driver(id):
    driver = Driver.query.get_or_404(id)

    # s3_client=boto3.client("s3")
    # bucket_name=current_app.config["AWS_S3_BUCKET"]
    # image_url = s3_client.generate_presigned_url(
    #     'get_object',
    #     Params={
    #         "Bucket": bucket_name,
    #         "Key": driver.image_filename
    #     },
    #     ExpiresIn=100
    # )

    data = {
        "page_title": "Driver Detail",
        "driver": driver_schema.dump(driver),
        # "image": image_url
    }
    return render_template("driver_detail.html", page_data=data)

# A PUT/PATCH route to update driver info
@drivers.route("/drivers/<int:id>/", methods=["POST"])
@login_required
def update_driver(id):
    driver = Driver.query.filter_by(driver_id=id)

    if current_user.id != driver.first().user_profile:
        abort(403, "You do not have permission to alter this driver!")

    updated_fields = driver_schema.dump(request.form)
    if updated_fields:
        driver.update(updated_fields)
        db.session.commit()

    data = {
        "page_title": "Driver Detail",
        "driver": driver_schema.dump(driver.first())
    }
    return render_template("driver_detail.html", page_data=data)

@drivers.route("/drivers/<int:id>/enrol/", methods=["POST"])
@login_required
def enrol_in_driver(id):
    driver = Driver.query.get_or_404(id)
    driver.students.append(current_user)
    db.session.commit()
    return redirect(url_for('users.user_detail'))

@drivers.route("/drivers/<int:id>/drop/", methods=["POST"])
@login_required
def drop_driver(id):
    driver = Driver.query.get_or_404(id)
    driver.students.remove(current_user)
    db.session.commit()
    return redirect(url_for('users.user_detail'))

@drivers.route("/drivers/<int:id>/delete/", methods=["POST"])
@login_required
def delete_driver(id):
    driver = Driver.query.get_or_404(id)

    if current_user.id != driver.user_profile:
        abort(403, "You do not have permission to delete this driver!")

    db.session.delete(driver)
    db.session.commit()
    return redirect(url_for('users.user_detail'))