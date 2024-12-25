from app.models.maintenance import MaintenanceRecord
from app.models.threshold import Threshold
from datetime import datetime
from app import db

def analyze_sensor_data(sensor_data):
    """Аналіз даних сенсорів та генерація сповіщень"""
    thresholds = {t.parameter: t.value for t in Threshold.query.all()}

    alerts = []

    if sensor_data.get("temperature") > thresholds.get("temperature", 40):
        alerts.append(f"Температура перевищила {thresholds['temperature']}°C.")

    if sensor_data.get("humidity") > thresholds.get("humidity", 90):
        alerts.append(f"Вологість перевищила {thresholds['humidity']}%.")

    if sensor_data.get("weight") > thresholds.get("weight", 1000):
        alerts.append(f"Вага перевищила {thresholds['weight']} кг.")

    # Якщо є критичні події, створити заявку на обслуговування
    if alerts:
        elevator_id = sensor_data["elevator_id"]
        existing_maintenance = MaintenanceRecord.query.filter_by(
            elevator_id=elevator_id, 
            description="pending"
        ).first()

        if not existing_maintenance:
            new_maintenance = MaintenanceRecord(
                elevator_id=elevator_id,
                maintenance_date=datetime.now().date(),
                description="; ".join(alerts),
            )
            db.session.add(new_maintenance)
            db.session.commit()

    return alerts