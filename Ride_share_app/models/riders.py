from main import db
from models.trips import Trip

class Rider(db.Model):
    """RIDER CLASS. 
    
    Lists the variables needed including:
    ONE to ONE relationship the user table.
    ONE to MANY relationship the trips table.
    """
    __tablename__ = "riders"
    rider_id = db.Column(db.Integer, primary_key=True)
    user_profile = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'), unique=True)
    trips = db.relationship(
        'Trip',
        backref="creator",
        lazy="joined"
    )




