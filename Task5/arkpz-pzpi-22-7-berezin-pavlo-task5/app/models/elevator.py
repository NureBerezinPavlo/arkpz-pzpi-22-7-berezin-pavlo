from app import db

class Elevator(db.Model):
    __tablename__ = 'elevators'
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    serial_number = db.Column(db.Unicode(50), unique=True, nullable=False)
    status = db.Column(db.Unicode(50), nullable=False)
    install_date = db.Column(db.Date, nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "building_id": self.building_id,
            "serial_number": self.serial_number,
            "status": self.status,
            "install_date": self.install_date.isoformat()
        }