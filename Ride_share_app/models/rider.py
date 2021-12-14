from main import db
from flask_login import UserMixin
from models.user import User
from werkzeug.security import check_password_hash

class Rider(UserMixin, db.Model):
    __tablename__ = "riders"
    rider_id = db.Column(db.Integer, primary_key=True)

    user_profile = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'))
    
    trips = db.relationship(
        'Trip',
        backref="rider",
        lazy="joined"
    )

    def check_password(self, password):
        return check_password_hash(self.password, password)

