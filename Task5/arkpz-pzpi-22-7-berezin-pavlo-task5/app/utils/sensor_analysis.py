from app.models.maintenance import MaintenanceRecord
from app.models.threshold import Threshold
from datetime import datetime
from app import db

def analyze_sensor_data(sensor_data):
    """Аналіз даних сенсорів та генерація сповіщень"""
    thresholds = {t.parameter: t.value for t in Threshold.query.all()}

    alerts = []

    # Перевірка температури, вологості та ваги
    if sensor_data.get("temperature") is not None and sensor_data.get("temperature") > thresholds.get("temperature", 40):
        alerts.append(f"Температура перевищила {thresholds['temperature']}°C.")

    if sensor_data.get("humidity") is not None and sensor_data.get("humidity") > thresholds.get("humidity", 90):
        alerts.append(f"Вологість перевищила {thresholds['humidity']}%.")

    if sensor_data.get("weight") is not None and sensor_data.get("weight") > thresholds.get("weight", 1000):
        alerts.append(f"Вага перевищила {thresholds['weight']} кг.")

    if not sensor_data.get("is_power_on", True):
        alerts.append("Відсутнє електропостачання.")

    if sensor_data.get("is_stuck", False):
        alerts.append("Ліфт застряг.")

    # Визначення типу події
    event_type = determine_event_type(alerts)

    # Якщо є критичні події, створити заявку на обслуговування
    if event_type == "critical":
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

    return alerts, event_type

def determine_event_type(alerts):
    """
    Визначає тип події (event_type) на основі списку сповіщень (alerts).
    
    :param alerts: Список сповіщень. Якщо список порожній — тип normal, 
                   якщо є сповіщення — critical.
    :return: Рядок "normal" або "critical".
    """
    return "critical" if alerts else "normal"
