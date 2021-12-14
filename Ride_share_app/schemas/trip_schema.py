from models.trips import Trip
from main import ma 
from models.trips import Trip
from marshmallow_sqlalchemy import auto_field 
from marshmallow.validate import Length, Range
from schemas.rider_schema import RiderSchema
from schemas.driver_schema import DriverSchema

class TripSchema(ma.SQLAlchemyAutoSchema):
    trip_id = auto_field(dump_only=True)
    pick_up = auto_field(required=True, validate=Length(min=1))
    drop_off = auto_field(required=True, validate=Length(min=1))
    cost = auto_field(required = False, validate=Range(0, 500))
    rider_id = ma.Nested(
        "RiderSchema",
        only=("id", "name", "email",)
    )
    rider_id = ma.Nested(
        "DriverSchema",
        only=("id", "name", "email",)
    )

    class Meta:
        model = Trip
        load_instance = True

trip_schema = TripSchema()
trips_schema = TripSchema(many=True)

