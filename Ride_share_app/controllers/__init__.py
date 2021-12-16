from controllers.user_controller import user
from controllers.rider_controller import riders
from controllers.driver_controller import drivers
from controllers.vehicle_controller import vehicles
from controllers.image_controller import rider_images
from controllers.trip_controller import trips

registerable_controllers = [riders, drivers, vehicles, user, trips, rider_images]