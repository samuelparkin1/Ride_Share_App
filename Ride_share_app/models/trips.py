from main import db
from models.rider import Rider
from models.driver import Driver

class Trip(db.Model):

    __tablename__ = "courses"

    trip_id = db.Column(db.Integer, primary_key=True)
    pick_up = db.Column(db.String(80), unique=True, nullable=False)
    drop_off = db.Column(db.String(80), unique=True, nullable=False)
    cost = db.Column(db.Integer, nullable=False, server_default="0")
    rider_id = db.Column(db.Integer, db.ForeignKey('flasklogin-riders.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('flasklogin-drivers.id'))





