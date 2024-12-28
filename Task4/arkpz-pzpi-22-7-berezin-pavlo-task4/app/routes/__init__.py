from .buildings import ns_buildings
from .elevators import ns_elevators
from .maintenances import ns_maintenances
from .technicians import ns_technicians
from .sensors import ns_sensors
from .residents import ns_residents

def init_routes(api):
    api.add_namespace(ns_buildings)
    api.add_namespace(ns_elevators)
    api.add_namespace(ns_maintenances)
    api.add_namespace(ns_technicians)
    api.add_namespace(ns_sensors)
    api.add_namespace(ns_residents)