from main import db

class Vehicle(db.Model):
    """VEHICLE CLASS. 
    
    Lists the columns and their variables that need to be included in the data table:
    ONE to ONE relationship with the driver.
    """  
    __tablename__ = "vehicles"

    # These attributes specify what columns the table should have
    vehicle_id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    rego = db.Column(db.String(80), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False, server_default="0")
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.driver_id'), unique=True)




