from app import db

# Модель записів обслуговування
class MaintenanceRecord(db.Model):
    __tablename__ = 'maintenance_records'
    id = db.Column(db.Integer, primary_key=True)
    elevator_id = db.Column(db.Integer, db.ForeignKey('elevators.id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.id'), nullable=False)
    maintenance_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.UnicodeText, nullable=False)