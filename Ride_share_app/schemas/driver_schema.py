from main import ma 
from models.drivers import Driver
from marshmallow_sqlalchemy import auto_field 
from marshmallow.validate import Length, Range

class DriverSchema(ma.SQLAlchemyAutoSchema):
    driver_id = auto_field(dump_only=True)

    user_id = ma.Nested(
        "UserSchema",
        only=("id", "name", "email",)
    )
    students = ma.Nested(
        "UserSchema",
        only=("id", "name", "email",)
    )

    class Meta:
        model = Driver
        load_instance = True

driver_schema = DriverSchema()
drivers_schema = DriverSchema(many=True)
