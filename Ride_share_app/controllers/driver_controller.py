from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.drivers import Driver
from controllers.user_controller import user_detail
from schemas.driver_schema import drivers_schema, driver_schema
from flask_login import login_required, current_user
import boto3
from random import randint

drivers = Blueprint('drivers', __name__)


@drivers.route("/drivers/", methods=["GET"])
@login_required
def get_drivers():
    """This will display a list of registered Drivers.

    args: Takes in GET requests

    returns: Displays a list of registered drivers.
    
    Raises: None
    """
    data = {
        "page_title": "Driver Index",
        "drivers": drivers_schema.dump(Driver.query.all())
    }
    return render_template("driver_index.html", page_data=data)


@drivers.route("/drivers/", methods=["POST"])
@login_required
def create_driver():
    """This will allows users to become drivers.

        args: Takes in POST requests

        returns: Loads user input to the Driver Schema to create a new account.
        
        Raises: If users driver account already existing in the database,
                it will reload the page notifying them they are already a driver. 
        
                Will also verify that user editing the account is the owner of 
                the account prior to execution. 
        """
    if current_user.drivers:
        data = {
            "page_title": "Driver Index",
            "drivers": drivers_schema.dump(Driver.query.all()),
            "existing_driver_error": "You are already a registered driver"
            }
        return render_template("driver_index.html", page_data=data)   
    new_driver=driver_schema.load(request.form)
    new_driver.user_id = current_user
    db.session.add(new_driver)
    db.session.commit()
    return redirect(url_for('users.user_detail'))


@drivers.route("/drivers/<int:id>/", methods = ["GET"])
@login_required
def get_driver(id):
    """This will Display the drivers information.

    args: Takes in GET requests

    returns: Loads user detail's page with the selected users details.
    """
    driver = Driver.query.get_or_404(id)
    data = {
        "page_title": "Driver Detail",
        "driver": driver_schema.dump(driver),
    }
    return render_template("driver_detail.html", page_data=data)


@drivers.route("/drivers/<int:id>/delete/", methods=["POST"])
@login_required
def delete_driver(id):
    """This will delete drivers information from database.

    args:   Take in the dirvers ID number that is being requested to be deleted. 
            will verify that the driver deleting the account is the owner of the accout. 

    returns: Loads user detail's page with the selected users details.

    Raises: If the account does not belong to the driver, it will bring up a 403 page 
    notifying the user they do not have permission to delete the account 
    """
    driver = Driver.query.get_or_404(id)

    if current_user.id != driver.user_profile:
        abort(403, "You do not have permission to delete this driver!")

    db.session.delete(driver)
    db.session.commit()
    return redirect(url_for('users.user_detail'))