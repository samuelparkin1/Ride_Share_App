from main import db
from models.trips import Trip
from models.vehicles import Vehicle


class Driver(db.Model):
    # The tablename attribute specifies what the name of the table should be
    __tablename__ = "drivers"

    # These attributes specify what columns the table should have
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

    @property
    def image_filename(self):
        return f"driver_images/{self.driver_id}.png"



