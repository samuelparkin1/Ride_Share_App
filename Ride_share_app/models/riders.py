from main import db
from models.trips import Trip

class Rider(db.Model):
    # The tablename attribute specifies what the name of the table should be
    __tablename__ = "riders"

    # These attributes specify what columns the table should have
    rider_id = db.Column(db.Integer, primary_key=True)

    user_profile = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'), unique=True)

    trips = db.relationship(
        'Trip',
        backref="creator",
        lazy="joined"
    )



    @property
    def image_filename(self):
        return f"rider_images/{self.rider_id}.png"



