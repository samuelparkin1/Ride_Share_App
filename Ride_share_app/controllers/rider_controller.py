from flask import Blueprint, request, render_template, redirect, url_for, abort
from main import db, lm 
from models.rider import Rider
from schemas.rider_schema import riders_schema, rider_schema, rider_update_schema
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError

@lm.user_loader
def load_user(rider):
    return Rider.query.get(rider)

@lm.unauthorized_handler
def unauthorized():
    return redirect('/riders/login/')

rider = Blueprint("riders", __name__)

@rider.route("/riders/", methods=["GET"])
def get_rider():
    """Displays a list of riders from the database"""
    data = {
        "page_title": "Rider Index",
        "riders": riders_schema.dump(Rider.query.all())
    }
    return render_template("rider_index.html", page_data=data)


@rider.route("/riders/signup/", methods=["GET", "POST"])
def rider_sign_up():
    """Displays the signup form/creates a new rider when the form is submitted"""
    
    data = {"page_title": "Sign Up"}

    if request.method == "GET":
        return render_template("rider_signup.html", page_data=data)
    
    new_rider = rider_schema.load(request.form)
    db.session.add(new_rider)
    db.session.commit()
    login_user(new_rider)
    return redirect(url_for("riders.get_rider"))

@rider.route("/riders/login/", methods=["GET", "POST"])
def log_in():
    data = {"page_title": "Log In"}

    if request.method == "GET":
        return render_template("rider_login.html", page_data = data)

    rider = Rider.query.filter_by(email=request.form["email"]).first()
    if rider and rider.check_password(password=request.form["password"]):
        login_user(rider)
        return redirect(url_for("courses.get_courses"))

    abort(401, "Login unsuccessful. Did you supply the correct username and password?")

@rider.route("/riders/account/", methods = ["GET", "POST"])
@login_required
def rider_detail():
    if request.method == "GET":
        data = {"page_title": "Account Details"}
        return render_template("rider_details.html", page_data = data)

    rider = Rider.query.filter_by(id = current_user.id)
    updated_fields = rider_schema.dump(request.form)
    errors = rider_update_schema.validate(updated_fields)

    if errors:
        raise ValidationError(message = errors)

    rider.update(updated_fields)
    db.session.commit()
    return redirect(url_for("riders.get_rider"))

@rider.route("/riders/logout/", methods=["POST"])
@login_required
def log_out():
    logout_user()
    return redirect(url_for("riders.log_in"))