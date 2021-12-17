from main import ma 
from models.vehicles import Vehicle
from marshmallow_sqlalchemy import auto_field 
from marshmallow.validate import Length, Range

class VehicleSchema(ma.SQLAlchemyAutoSchema):
    """VEHICLE SCHEMAS. 

     Calls on the vehicle schema to retrieve variables as part of its one to one 
     relationship with the 'drivers table'  
    """
    vehicle_id = auto_field(dump_only=True)

    make = auto_field(required=True, validate=Length(min=1))

    model = auto_field(required=True, validate=Length(min=1))

    rego = auto_field(required=True, validate=Length(min=1))

    year = auto_field(validate=Range(0, 9999))

    vehicle_driver = ma.Nested(
        "DriverSchema",
        # only=("driver_id","user_id")
    ) 

    class Meta:
        model = Vehicle
        load_instance = True

vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)
