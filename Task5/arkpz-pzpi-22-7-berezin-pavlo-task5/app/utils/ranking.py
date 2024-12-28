from sqlalchemy import func
from app.models.sensor import SensorLog
from app.models.elevator import Elevator
from app import db

def get_elevator_usage_ranking():
    """
    Розрахунок рейтингу ліфтів за інтенсивністю використання.
    :return: Список ліфтів із кількістю використань, відсортований за інтенсивністю.
    """
    try:
        # Групування логів за ліфтами та підрахунок кількості записів
        ranking = (
            db.session.query(
                Elevator.id,
                Elevator.serial_number,
                func.count(SensorLog.id).label('usage_count')
            )
            .join(SensorLog, Elevator.id == SensorLog.elevator_id)
            .group_by(Elevator.id, Elevator.serial_number)
            .order_by(func.count(SensorLog.id).desc())
            .all()
        )

        result = [
            {
                "elevator_id": elevator_id,
                "serial_number": serial_number,
                "usage_count": usage_count
            }
            for elevator_id, serial_number, usage_count in ranking
        ]
        return result
    except Exception as e:
        return {"error": str(e)}