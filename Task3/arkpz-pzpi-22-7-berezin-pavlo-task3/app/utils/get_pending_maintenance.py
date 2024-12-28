from app.models.maintenance import MaintenanceRecord

def get_pending_maintenance():
    """
    Отримати список записів обслуговування, які очікують на призначення техніка.
    
    :return: Список словників із записами обслуговування або порожній список, якщо таких немає.
    """
    try:
        # Запити записи, де technician_id є NULL
        pending_records = MaintenanceRecord.query.filter(MaintenanceRecord.technician_id.is_(None)).all()
        
        # Форматування результатів
        result = [
            {
                "id": record.id,
                "elevator_id": record.elevator_id,
                "maintenance_date": record.maintenance_date.isoformat(),
                "description": record.description
            }
            for record in pending_records
        ]
        return result
    except Exception as e:
        raise RuntimeError(f"Не вдалося отримати записи обслуговування: {str(e)}")