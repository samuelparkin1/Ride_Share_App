from main import db
from models.trips import Trip


# enrolments = db.Table(
#     'enrolments',
#     db.Column('user_id', db.Integer, db.ForeignKey('flasklogin-users.id'), primary_key=True),
#     db.Column('rider_id', db.Integer, db.ForeignKey('riders.rider_id'), primary_key=True)
# )

# Our first model! 
# This tells the ORM what tables should exist in the database
# It also lets us retrieve info from those tables
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

    # students = db.relationship(
    #     User,
    #     secondary=enrolments,
    #     backref=db.backref('enrolled_riders'),
    #     lazy="joined"
    # )

    @property
    def image_filename(self):
        return f"rider_images/{self.rider_id}.png"



