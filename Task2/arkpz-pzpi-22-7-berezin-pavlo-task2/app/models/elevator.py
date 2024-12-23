from app import db

class Elevator(db.Model):
    __tablename__ = 'elevators'
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    serial_number = db.Column(db.Unicode(50), unique=True, nullable=False)
    status = db.Column(db.Unicode(50), nullable=False)
    install_date = db.Column(db.Date, nullable=False)