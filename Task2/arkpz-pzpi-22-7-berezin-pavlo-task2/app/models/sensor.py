from app import db

# Модель логів даних сенсорів
class SensorLog(db.Model):
    __tablename__ = 'sensor_logs'
    id = db.Column(db.Integer, primary_key=True)
    elevator_id = db.Column(db.Integer, db.ForeignKey('elevators.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Float, nullable=True) 
    humidity = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    event_type = db.Column(db.Unicode(50), nullable=False)
    message = db.Column(db.UnicodeText, nullable=True)  # Опис події або коментар