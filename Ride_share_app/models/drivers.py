from main import db
from models.trips import Trip
from models.vehicles import Vehicle


class Driver(db.Model):
    """USER CLASS. 
    
    Lists the variables needed including:
    ONE to ONE relationship the user table.
    ONE to ONE relationship the vehicles table.
    ONE to MANY relationship the trips table.
    """
    __tablename__ = "drivers"
    driver_id = db.Column(db.Integer, primary_key=True)
    user_profile = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'), unique=True)
    vehicles = db.relationship(
        'Vehicle',
        backref="vehicle_driver",
        lazy="joined"
    )    

    trips = db.relationship(
        'Trip',
        backref="acceptor",
        lazy="joined"
    )




