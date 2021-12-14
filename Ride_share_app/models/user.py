from sqlalchemy.orm import backref
from main import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "flasklogin-users"
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    
    email = db.Column(db.String(40), unique=True, nullable=False)
    
    password = db.Column(db.String(200), nullable=False)
    
    is_rider = db.Column(db.Boolean(), nullable=True, server_default="True")

    rider_profile = db.relationship('Rider', backref = 'user_profile', lazy="joined")

    def check_password(self, password):
        return check_password_hash(self.password, password)


    # To access the list of trips created by Oliver, we call Oliver.trips
    # = [<Trip 1>, <Trip 2>, ...]

    # To access the creator of CCC, we call CCC.creator
    # = <User Oliver>
