from flask import Blueprint, request, render_template, redirect, url_for, abort
from main import db, lm 
from models.driver import Driver
from schemas.driver_schema import drivers_schema, driver_schema, driver_update_schema
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError

@lm.user_loader
def load_user(driver):
    return Driver.query.get(driver)

@lm.unauthorized_handler
def unauthorized():
    return redirect('/drivers/login/')

driver = Blueprint("drivers", __name__)

@driver.route("/drivers/", methods=["GET"])
def get_driver():
    """Displays a list of drivers from the database"""
    data = {
        "page_title": "User Index",
        "drivers": drivers_schema.dump(Driver.query.all())
    }
    return render_template("driver_index.html", page_data=data)


@driver.route("/drivers/signup/", methods=["GET", "POST"])
def driver_sign_up():
    """Displays the signup form/creates a new driver when the form is submitted"""
    
    data = {"page_tite": "Sign Up"}

    if request.method == "GET":
        return render_template("driver_signup.html", page_data=data)
    
    new_driver = driver_schema.load(request.form)
    db.session.add(new_driver)
    db.session.commit()
    login_user(new_driver)
    return redirect(url_for("drivers.get_driver"))

@driver.route("/drivers/login/", methods=["GET", "POST"])
def log_in():
    data = {"page_title": "Log In"}

    if request.method == "GET":
        return render_template("driver_login.html", page_data = data)

    driver = Driver.query.filter_by(email=request.form["email"]).first()
    if driver and driver.check_password(password=request.form["password"]):
        login_user(driver)
        return redirect(url_for("courses.get_courses"))

    abort(401, "Login unsuccessful. Did you supply the correct username and password?")

@driver.route("/drivers/account/", methods = ["GET", "POST"])
@login_required
def driver_detail():
    if request.method == "GET":
        data = {"page_title": "Account Details"}
        return render_template("driver_details.html", page_data = data)

    driver = Driver.query.filter_by(id = current_user.id)
    updated_fields = driver_schema.dump(request.form)
    errors = driver_update_schema.validate(updated_fields)

    if errors:
        raise ValidationError(message = errors)

    driver.update(updated_fields)
    db.session.commit()
    return redirect(url_for("drivers.get_driver"))

@driver.route("/drivers/logout/", methods=["POST"])
@login_required
def log_out():
    logout_user()
    return redirect(url_for("drivers.log_in"))