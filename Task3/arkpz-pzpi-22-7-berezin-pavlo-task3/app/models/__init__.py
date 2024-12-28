from .building import Building
from .elevator import Elevator
from .maintenance import MaintenanceRecord
from .sensor import SensorLog
from .technician import Technician
from .resident import Resident

def init_models(app):
    from app import db
    with app.app_context():
        db.create_all()