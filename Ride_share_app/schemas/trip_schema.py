from main import ma 
from models.trips import Trip
from marshmallow_sqlalchemy import auto_field 
from marshmallow.validate import Length, Range

class TripSchema(ma.SQLAlchemyAutoSchema):
    trip_id = auto_field(dump_only=True)
    pick_up = auto_field(required=True, validate=Length(min=1))
    destination = auto_field(validate=Length(min=1))
    cost = auto_field(required = False, validate=Range(0, 500))
    user_id = ma.Nested(
        "UserSchema",
        only=("id", "name", "email",)
    )
    students = ma.Nested(
        "UserSchema",
        only=("id", "name", "email",)
    )

    class Meta:
        model = Trip
        load_instance = True

trip_schema = TripSchema()
trips_schema = TripSchema(many=True)
