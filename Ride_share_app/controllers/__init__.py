from controllers.user_controller import user
from controllers.rider_controller import riders
from controllers.driver_controller import drivers
from controllers.vehicle_controller import vehicles
from controllers.trip_controller import trips

# A list of controllers needed for the app to be able to execute command functions
registerable_controllers = [riders, drivers, vehicles, user, trips,]