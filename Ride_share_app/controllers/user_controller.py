from flask import Blueprint, request, render_template, redirect, url_for, abort
from main import db, lm 
from sqlalchemy import func, exc
from models.user import User
from models.trips import Trip
from schemas.user_schema import users_schema, user_schema, user_update_schema
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError


@lm.user_loader
def load_user(user):
    return User.query.get(user)


@lm.unauthorized_handler
def unauthorized():
    """If the user is not logged in when the function requires '@login_required' it 
    will redirect the user to the login page """
    return redirect('/users/login/')


user = Blueprint("users", __name__)
 
@user.route('/')
@login_required
def homepage():
    """This will display the home page when called. """
    return render_template("homepage.html")


@user.route("/users/", methods=["GET"])
@login_required
def get_user():
    """This will display a list of registered users."""
    data = {
        "page_title": "User Index",
        "users": users_schema.dump(User.query.all())
    }
    return render_template("user_index.html", page_data=data)

#This will display a signup page for the users.
@user.route("/users/signup/", methods=["GET", "POST"])
def user_sign_up():
    """This will display a signup page for the users.

    args: Takes in both GET and POST requests

    returns: Loads user input to the User Schema to create a new account.
    
    Raises: If user has inputted an email address that is already existing in the database,
            it will redirect the user back to the signin page notifying them the email is already in use. 
    """
    
    data = {"page_tite": "Sign Up"}

    if request.method == "GET":
        return render_template("user_signup.html", page_data=data)
    try:    
        new_user = user_schema.load(request.form)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("users.user_detail"))
    except exc.IntegrityError:
        db.session.rollback()
        error = {"email_error": "Email is already in use. Please enter different email address "}
        return render_template ("user_signup.html", page_data=error)

@user.route("/users/login/", methods=["GET", "POST"])
def log_in():
    """USER lOGIN. 
    
    This will display a login page for the users.

    args: Takes in both GET and POST requests. 
            It will takin the users email and password and check if they match those in already 
            in the database. 

    returns:    GET = generate the login page.
                POST = If credentials are correct will login user and redirect them to their user profile.  

    Raises: If user has inputted an incorrect email address or password, it will call a 401 error. 
    """
    data = {"page_title": "Log In"}

    if request.method == "GET":
        return render_template("user_login.html", page_data = data)

    user = User.query.filter_by(email=request.form["email"]).first()
    if user and user.check_password(password=request.form["password"]):
        login_user(user)
        return redirect(url_for("users.user_detail"))

    abort(401, "Login unsuccessful. Did you supply the correct username and password?")

@user.route("/users/account/", methods = ["GET", "POST"])
@login_required
def user_detail():
    """USER DETAILS. 
    
    This will display the users datails.

    Args: Takes in both GET and POST requests. 
        will update information on a POST request.

    Returns: will call upon the trip schema to find the total costs the riders and drivers have made 
    and received. 

    Raises:  A Validation Errorwith the error message.
    """
    if request.method == "GET":
        if current_user.riders:
            rider_cost = db.session.query(func.sum(Trip.cost)).filter(Trip.rider_id==current_user.riders[0].rider_id).scalar()
        else:
            rider_cost = 0
        
        if current_user.drivers:
            driver_cost = db.session.query(func.sum(Trip.cost)).filter(Trip.driver_id==current_user.drivers[0].driver_id).scalar()
        else:
            driver_cost = 0
        data = {
            "page_title": "Account Details",
            "rider_cost" : rider_cost,
            "driver_cost" : driver_cost,
        }

        return render_template("user_details.html", page_data = data)

    user = User.query.filter_by(id = current_user.id)
    updated_fields = user_schema.dump(request.form)
    errors = user_update_schema.validate(updated_fields)

    if errors:
        raise ValidationError(message = errors)

    user.update(updated_fields)
    db.session.commit()
    return redirect(url_for("users.user_detail"))

@user.route("/users/logout/", methods=["POST"])
@login_required
def log_out():
    """USER LOGOUT. 
    
    When called it will log the user out.
    """
    logout_user()
    return redirect(url_for("users.log_in"))

@user.route("/users/<int:id>/delete/", methods=["POST"])
@login_required
def delete_user(id):
    """USER DELETE. 
    
    When called it will log the user out and delete their accout from the User data base.
    """
    user = User.query.get_or_404(id)
    logout_user()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.log_in'))