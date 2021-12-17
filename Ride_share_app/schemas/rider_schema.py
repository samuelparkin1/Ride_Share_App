from main import ma 
from models.riders import Rider
from marshmallow_sqlalchemy import auto_field 
from marshmallow.validate import Length, Range

class RiderSchema(ma.SQLAlchemyAutoSchema):
    """RIDER SCHEMAS. 

     Calls on user schema to retrieve variables as part of its one to one 
     relationship with the 'users table'   
    """
    rider_id = auto_field(dump_only=True)

    user_id = ma.Nested(
        "UserSchema",
        only=("id", "name", "email",)
    )

    class Meta:
        model = Rider
        load_instance = True

rider_schema = RiderSchema()
riders_schema = RiderSchema(many=True)
