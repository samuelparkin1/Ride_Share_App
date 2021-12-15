from main import db
from models.user import User

# enrolments = db.Table(
#     'enrolments',
#     db.Column('user_id', db.Integer, db.ForeignKey('flasklogin-users.id'), primary_key=True),
#     db.Column('driver_id', db.Integer, db.ForeignKey('drivers.driver_id'), primary_key=True)
# )

# Our first model! 
# This tells the ORM what tables should exist in the database
# It also lets us retrieve info from those tables
class Driver(db.Model):
    # The tablename attribute specifies what the name of the table should be
    __tablename__ = "drivers"

    # These attributes specify what columns the table should have
    driver_id = db.Column(db.Integer, primary_key=True)

    user_profile = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'), unique=True) 

    # students = db.relationship(
    #     User,
    #     secondary=enrolments,
    #     backref=db.backref('enrolled_drivers'),
    #     lazy="joined"
    # )

    @property
    def image_filename(self):
        return f"driver_images/{self.driver_id}.png"



