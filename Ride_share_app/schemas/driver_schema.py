from main import ma 
from models.drivers import Driver
from marshmallow_sqlalchemy import auto_field 


class DriverSchema(ma.SQLAlchemyAutoSchema):
    """DRIVER SCHEMAS. 

     Calls on user schema to retrieve variables as part of its one to one 
     relationship with the 'users table'

    
    """
    driver_id = auto_field(dump_only=True)

    user_id = ma.Nested(
        "UserSchema",
        only=("id", "name", "email",)
    )

    class Meta:
        model = Driver
        load_instance = True

driver_schema = DriverSchema()
drivers_schema = DriverSchema(many=True)
