from main import ma 
from models.trips import Trip
from marshmallow_sqlalchemy import auto_field 
from marshmallow.validate import Length, Range

class TripSchema(ma.SQLAlchemyAutoSchema):
    """TRIP SCHEMAS. 

     Calls on user schema to retrieve variables as part of its one to one 
     relationship with the 'riders table' and 'drivers table'  
    """
    trip_id = auto_field(dump_only=True)
    pick_up = auto_field(required=True, validate=Length(min=1))
    destination = auto_field(validate=Length(min=1))
    cost = auto_field(required = False, validate=Range(0, 500))
    creator = ma.Nested(
        "RiderSchema",
    )
    acceptor = ma.Nested(
        "DriverSchema",
    )   
    class Meta:
        model = Trip
        load_instance = True

trip_schema = TripSchema()
trips_schema = TripSchema(many=True)
