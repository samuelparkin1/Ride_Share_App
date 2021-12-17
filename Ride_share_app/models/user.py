from main import db
from flask_login import UserMixin
from models.riders import Rider
from models.drivers import Driver
from werkzeug.security import check_password_hash

class User(UserMixin, db.Model):
    """USER CLASS. 
    
    Lists the variables needed including the ONE to ONE 
    relationships with drivers table and riders table.

    Also utilise werkzeug.security to check user passwords.
    
    """

    __tablename__ = "flasklogin-users"
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    
    email = db.Column(db.String(40), unique=True, nullable=False)
    
    password = db.Column(db.String(200), nullable=False)
    

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
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

