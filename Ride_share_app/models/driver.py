from main import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class Driver(UserMixin, db.Model):
    __tablename__ = "flasklogin-drivers"
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)

    last_name = db.Column(db.String(100), nullable=False)
    
    DOB = db.Column(db.String(100), nullable=False)

    gender = db.Column(db.String(50))

    email = db.Column(db.String(40), unique=True, nullable=False)
    
    password = db.Column(db.String(200), nullable=False)    
    is_driver = db.Column(db.Boolean(), nullable=False, server_default="True")

    # courses = db.relationship(
    #     'Course',
    #     backref="creator",
    #     lazy="joined"
    # )
    # To access the list of courses created by Oliver, we call Oliver.courses
    # = [<Course 1>, <Course 2>, ...]

    # To access the creator of CCC, we call CCC.creator
    # = <User Oliver>

    def check_password(self, password):
        return check_password_hash(self.password, password)

