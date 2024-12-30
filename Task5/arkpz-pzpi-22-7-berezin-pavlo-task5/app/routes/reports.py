from datetime import datetime, timedelta
from flask_restx import Namespace, Resource
from app.models.sensor import SensorLog
from app.utils.ranking import get_elevator_usage_ranking
from app.utils.auth import admin_required

ns_reports = Namespace('reports', description='Формування звітів')

@ns_reports.route('/summary/<int:elevator_id>')
class SummaryReport(Resource):
    @admin_required
    def get(self, elevator_id):
        """Отримати зведений звіт для ліфта"""
        one_month_ago = datetime.now() - timedelta(days=30)
        logs = SensorLog.query.filter(
            SensorLog.elevator_id == elevator_id,
            SensorLog.timestamp >= one_month_ago
        ).all()

        total_logs = len(logs)
        critical_logs = len([log for log in logs if log.event_type == "critical"])

        return {
            "elevator_id": elevator_id,
            "total_logs": total_logs,
            "critical_logs": critical_logs,
            "report_date": datetime.now().strftime("%Y-%m-%d")
        }, 200

@ns_reports.route('/ranking')
class ElevatorUsageRanking(Resource):
    @admin_required
    def get(self):
        """Отримати рейтинг ліфтів за інтенсивністю використання"""
        result = get_elevator_usage_ranking()
        if "error" in result:
            return {"error": result["error"]}, 500
        return result, 200