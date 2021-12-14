from sqlalchemy.orm import load_only
from main import ma 
from models.driver import Driver
from marshmallow_sqlalchemy import auto_field
from marshmallow import fields, exceptions, validate
from werkzeug.security import generate_password_hash

class DriverSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Driver
        load_instance=True
    
    id = auto_field(dump_only=True)
    name = auto_field(required=True, validate=validate.Length(1))
    email = auto_field(required=True, validate=validate.Email())
    is_driver = auto_field(required=False, default=False)
    password = fields.Method(
        required=True,
        load_only=True,
        deserialize="load_password"
    )
    
    def load_password(self, password):
        if len(password)>6:
            return generate_password_hash(password, method='sha256')
        raise exceptions.ValidationError("Password must be at least 6 characters.")

driver_schema = DriverSchema()
drivers_schema = DriverSchema(many=True) 
driver_update_schema = DriverSchema(partial=True)