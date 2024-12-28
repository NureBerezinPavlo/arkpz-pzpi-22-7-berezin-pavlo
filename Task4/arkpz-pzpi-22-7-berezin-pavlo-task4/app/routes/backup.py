from flask import jsonify, request, send_file
from flask_restx import Namespace, Resource, fields
import os
import json
from app import db
from app.models.sensor import SensorLog
from app.models.elevator import Elevator
from app.models.building import Building
from app.models.maintenance import MaintenanceRecord
from app.models.admin import Admin
from app.models.technician import Technician
from app.models.threshold import Threshold
from app.utils.auth import admin_required

ns_backup = Namespace('backup', description='Операції з резервними копіями (лише для адміністраторів)')

backup_model = ns_backup.model('BackupOperation', {
    'file_path': fields.String(description='Шлях до резервної копії')
})

@ns_backup.route('/export')
class BackupExport(Resource):
    @ns_backup.response(200, 'Резервна копія відновлена')
    @ns_backup.response(403, 'Доступ заборонено')
    @ns_backup.response(400, 'Некоректний файл')
    @ns_backup.doc(security='BearerAuth')
    @admin_required
    def get(self):
        """Експорт даних до резервної копії"""
        file_path = "backup.json"
        data = {
            "sensor_logs": [log.as_dict() for log in SensorLog.query.all()],
            "elevators": [elevator.as_dict() for elevator in Elevator.query.all()],
            "buildings": [building.as_dict() for building in Building.query.all()],
            "maintenances": [maintenance.as_dict() for maintenance in MaintenanceRecord.query.all()],
            "admins": [admin.as_dict() for admin in Admin.query.all()],
            "technicians": [technician.as_dict() for technician in Technician.query.all()],
            "thresholds": [threshold.as_dict() for threshold in Threshold.query.all()]
        }
        with open(file_path, "w") as backup_file:
            json.dump(data, backup_file)

        return send_file(file_path, as_attachment=True, download_name="backup.json")

@ns_backup.route('/import')
class BackupImport(Resource):
    @ns_backup.response(200, 'Резервна копія відновлена')
    @ns_backup.response(403, 'Доступ заборонено')
    @ns_backup.response(400, 'Некоректний файл')
    @ns_backup.doc(security='BearerAuth')
    @admin_required
    def post(self):
        """Імпорт даних із резервної копії"""
        if 'file' not in request.files:
            return {"message": "Файл не надано"}, 400

        backup_file = request.files['file']
        if not backup_file.filename.endswith(".json"):
            return {"message": "Некоректний формат файлу. Очікується .json"}, 400

        data = json.load(backup_file)
        SensorLog.query.delete()
        Elevator.query.delete()

        for log in data.get("sensor_logs", []):
            new_log = SensorLog(**log)
            db.session.add(new_log)

        for elevator in data.get("elevators", []):
            new_elevator = Elevator(**elevator)
            db.session.add(new_elevator)

        for building in data.get("buildings", []):
            new_building = Building(**building)
            db.session.add(new_building)

        for maintenance in data.get("maintenances", []):
            new_maintenance = MaintenanceRecord(**maintenance)
            db.session.add(new_maintenance)

        for admin in data.get("admins", []):
            new_admin = Admin(**admin)
            db.session.add(new_admin)
        
        for technician in data.get("technicians", []):
            new_technician = Technician(**technician)
            db.session.add(new_technician)

        for threshold in data.get("thresholds", []):
            new_threshold = Threshold(**threshold)
            db.session.add(new_threshold)

        db.session.commit()
        return {"message": "Дані успішно відновлено"}, 200