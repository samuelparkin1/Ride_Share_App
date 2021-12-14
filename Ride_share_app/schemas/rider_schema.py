from sqlalchemy.orm import load_only
from main import ma 
from models.rider import Rider
from schemas.user_schema import UserSchema
from marshmallow_sqlalchemy import auto_field
from marshmallow import fields, exceptions, validate


class RiderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Rider
        load_instance=True
    
    rider_id = auto_field(dump_only=True)

    user_profile = ma.Nested(
        "UserSchema",
        only=("id", "name", "email",)
    )


rider_schema = RiderSchema()
riders_schema = RiderSchema(many=True) 
rider_update_schema = RiderSchema(partial=True)