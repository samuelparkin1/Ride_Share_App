from flask_sqlalchemy import model
from main import db
from flask import Blueprint
import os

db_commands = Blueprint("db-custom", __name__)

@db_commands.cli.command("create")
def create_db():
    """Creates tables in the database based on the models."""
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_db():
    """Drops all tables in the database"""
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted!")


@db_commands.cli.command("reset")
def reset_db():
    """Drops, creates, and seeds tables in one step."""
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted!")
    db.create_all()
    print("Tables created!")
    db.session.commit()


@db_commands.cli.command("export")
def export_db():
    """export tables in the database based."""
    from models.drivers import Driver
    from models.riders import Rider
    from models.user import User
    from models.trips import Trip
    from models.vehicles import Vehicle
    from schemas.driver_schema import drivers_schema, driver_schema
    from schemas.rider_schema import riders_schema
    from schemas.user_schema import users_schema
    from schemas.trip_schema import trips_schema
    from schemas.vehicle_schema import vehicles_schema

    model_list = Driver, Rider, User, Trip, Vehicle
    schema_list = [drivers_schema, riders_schema, users_schema, trips_schema, vehicles_schema]
    for model, schema  in zip (model_list, schema_list):
        new_file = open(f"{model.__tablename__}_database_table.txt", "a")
        new_file.write(str(schema.dump(model.query.all())))
        new_file.close()
        print(f"{model.__tablename__}_database_table.txt Created")

