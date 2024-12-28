from app import db

# Модель логів даних сенсорів
class SensorLog(db.Model):
    __tablename__ = 'sensor_logs'
    id = db.Column(db.Integer, primary_key=True)
    elevator_id = db.Column(db.Integer, db.ForeignKey('elevators.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Float, nullable=False) 
    humidity = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    event_type = db.Column(db.Unicode(50), nullable=False)
    message = db.Column(db.UnicodeText, nullable=True)  # Опис події або коментар
    is_power_on = db.Column(db.Boolean, nullable=False, default=True)  # Чи є електропостачання
    is_moving = db.Column(db.Boolean, nullable=False, default=False)   # Чи переміщується ліфт
    is_stuck = db.Column(db.Boolean, nullable=False, default=False)    # Чи застряг ліфт

    def as_dict(self):
        return {
            "id": self.id,
            "elevator_id": self.elevator_id,
            "timestamp": self.timestamp.isoformat(),
            "temperature": self.temperature,
            "humidity": self.humidity,
            "weight": self.weight,
            "event_type": self.event_type,
            "message": self.message,
            "is_power_on": self.is_power_on,
            "is_moving": self.is_moving,
            "is_stuck": self.is_stuck
        }