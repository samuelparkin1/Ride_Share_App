from main import db



# Our first model! 
# This tells the ORM what tables should exist in the database
# It also lets us retrieve info from those tables
class Vehicle(db.Model):
    # The tablename attribute specifies what the name of the table should be
    __tablename__ = "vehicles"

    # These attributes specify what columns the table should have
    vehicle_id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    rego = db.Column(db.String(80), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False, server_default="0")

    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.driver_id'), unique=True)
    


    @property
    def image_filename(self):
        return f"vehicle_images/{self.vehicle_id}.png"



