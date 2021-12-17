from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.riders import Rider
from controllers.user_controller import user_detail
from schemas.rider_schema import riders_schema, rider_schema
from flask_login import login_required, current_user
import boto3
from random import randint

riders = Blueprint('riders', __name__)


@riders.route("/riders/", methods=["GET"])
@login_required
def get_riders():
    """This will display a list of registered Riders.

    args: Takes in GET requests

    returns: Displays a list of registered riders.
    
    Raises: None
    """
    data = {
        "page_title": "Rider Index",
        "riders": riders_schema.dump(Rider.query.all())
    }
    return render_template("rider_index.html", page_data=data)

@riders.route("/riders/", methods=["POST"])
@login_required
def create_rider():
    """This will allows users to become riders.

    args: Takes in POST requests

    returns: Loads user input to the Rider Schema to create a new account.
    
    Raises: If users rider account already existing in the database,
            it will reload the page notifying them they are already a rider. 
    
            Will also verify that user editing the account is the owner of 
            the account prior to execution. 
    """
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


@riders.route("/riders/<int:id>/", methods = ["GET"])
@login_required
def get_rider(id):
    """This will Display the riders information.

    args: Takes in GET requests

    returns: Loads user detail's page with the selected users details.
    """
    rider = Rider.query.get_or_404(id)
    data = {
        "page_title": "Rider Detail",
        "rider": rider_schema.dump(rider),
    }
    return render_template("rider_detail.html", page_data=data)


@riders.route("/riders/<int:id>/delete/", methods=["POST"])
@login_required
def delete_rider(id):
    """This will delete riders information from database.

    args:   Take in the dirvers ID number that is being requested to be deleted. 
            will verify that the rider deleting the account is the owner of the accout. 

    returns: Loads user detail's page with the selected users details.

    Raises: If the account does not belong to the rider, it will bring up a 403 page 
    notifying the user they do not have permission to delete the account 
    """
    rider = Rider.query.get_or_404(id)
    if current_user.id != rider.user_profile:
        abort(403, "You do not have permission to delete this rider!")

    db.session.delete(rider)
    db.session.commit()
    return redirect(url_for('users.user_detail'))