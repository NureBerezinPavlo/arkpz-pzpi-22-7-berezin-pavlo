from datetime import datetime, timedelta
from app.models.sensor import SensorLog
from app import db

def clean_old_data(retention_days=90):
    """
    Видалення застарілих записів із бази даних.
    :param retention_days: Кількість днів, після яких дані вважаються застарілими.
    """
    try:
        # Дата до якої видаляємо дані
        cutoff_date = datetime.now() - timedelta(days=retention_days)

        # Видалення старих даних сенсорів
        deleted_sensors = SensorLog.query.filter(SensorLog.timestamp < cutoff_date).delete()

        # Підтвердження змін у базі
        db.session.commit()

        return {
            "message": "Старі дані успішно видалено",
            "deleted_sensors": deleted_sensors
        }
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}