from main import db
from flask_login import UserMixin
from models.riders import Rider
from models.drivers import Driver
from werkzeug.security import check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "flasklogin-users"
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    
    email = db.Column(db.String(40), unique=True, nullable=False)
    
    password = db.Column(db.String(200), nullable=False)
    
    is_rider = db.Column(db.Boolean(), nullable=False, server_default="True")

    is_driver = db.Column(db.Boolean(), nullable=False, server_default="True")

    riders = db.relationship(
        'Rider',
        backref="user_id",
        lazy="joined"
    )
    drivers = db.relationship(
        'Driver',
        backref="user_id",
        lazy="joined"
    )
    
    # To access the list of riders created by Oliver, we call Oliver.riders
    # = [<Rider 1>, <Rider 2>, ...]

    # To access the user_id of CCC, we call CCC.user_id
    # = <User Oliver>

    def check_password(self, password):
        return check_password_hash(self.password, password)

