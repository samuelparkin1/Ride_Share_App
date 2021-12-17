from main import db

class Trip(db.Model):
    """DRIVER CLASS. 
    
    Lists the variables needed including:
    ONE to MANY relationship with the riders.
    ONE to MANY relationship with the driver.
.
    """
    __tablename__ = "trips"
    trip_id = db.Column(db.Integer, primary_key=True)
    pick_up = db.Column(db.String(80), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    cost = db.Column(db.Integer, nullable=False, server_default="0")

    rider_id = db.Column(db.Integer, db.ForeignKey('riders.rider_id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.driver_id'))




