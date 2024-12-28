from flask import request
from flask_restx import Namespace, Resource, fields
from app.models.maintenance import MaintenanceRecord
from app.models.elevator import Elevator
from app import db
from flask_restx import Namespace, Resource
from datetime import datetime
from app.utils.clean_old_data import clean_old_data
from app.utils.get_pending_maintenance import get_pending_maintenance
from app.utils.auth import admin_required

ns_maintenances = Namespace('maintenance', description='Операції технічного обслуговування')

# Модель для Swagger-документації
maintenance_model = ns_maintenances.model('MaintenanceRecord', {
    'elevator_id': fields.Integer(required=True, description='ID ліфта'),
    'technician_id': fields.Integer(required=True, description='ID техніка'),
    'maintenance_date': fields.String(required=True, description='Дата обслуговування (у форматі YYYY-MM-DD)'),
    'description': fields.String(required=True, description='Опис обслуговування'),
})

@ns_maintenances.route('/')
class MaintenanceListResource(Resource):
    @ns_maintenances.marshal_list_with(maintenance_model)
    @admin_required
    def get(self):
        """Отримати список усіх записів обслуговування"""
        records = MaintenanceRecord.query.all()
        return records

    @ns_maintenances.expect(maintenance_model)
    @admin_required
    def post(self):
        """Додати новий запис обслуговування"""
        data = request.json
        new_record = MaintenanceRecord(
            elevator_id=data['elevator_id'],
            technician_id=data['technician_id'],
            maintenance_date=datetime.now().date(),
            description=data['description'],
        )
        db.session.add(new_record)
        db.session.commit()
        return {"message": "Запис обслуговування створено"}, 201

@ns_maintenances.route('/<int:record_id>')
@ns_maintenances.param('record_id', 'Унікальний ідентифікатор запису обслуговування')
class MaintenanceResource(Resource):
    @ns_maintenances.marshal_with(maintenance_model)
    @admin_required
    def get(self, record_id):
        """Отримати деталі запису обслуговування"""
        record = MaintenanceRecord.query.get_or_404(record_id)
        return record

    @admin_required
    def delete(self, record_id):
        """Видалити запис обслуговування"""
        record = MaintenanceRecord.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()
        return {"message": "Запис обслуговування видалено"}, 200


@ns_maintenances.route('/schedule/<int:elevator_id>')
@ns_maintenances.param('elevator_id', 'Унікальний ідентифікатор ліфта')
class MaintenanceScheduler(Resource):
    @admin_required
    def post(self, elevator_id):
        """Планування профілактичного обслуговування"""
        try:
            elevator = Elevator.query.get(elevator_id)
            if not elevator:
                return {"error": "Ліфт не знайдено"}, 404

            # Перевірка дати останнього обслуговування
            last_maintenance = MaintenanceRecord.query.filter_by(elevator_id=elevator_id).order_by(
                MaintenanceRecord.maintenance_date.desc()
            ).first()

            if last_maintenance:
                days_since_last = (datetime.now().date() - last_maintenance.maintenance_date).days
                if days_since_last < 180:  # Профілактика кожні 6 місяців
                    return {"message": "Профілактичне обслуговування ще не потрібне"}, 200

            # Створення нового запису обслуговування
            new_record = MaintenanceRecord(
                elevator_id=elevator_id,
                technician_id=None,  # Технік призначається пізніше
                maintenance_date=datetime.now().date(),
                description="Автоматично заплановане профілактичне обслуговування",
            )
            db.session.add(new_record)
            db.session.commit()

            return {"message": "Профілактичне обслуговування заплановано"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

@ns_maintenances.route('/cleanup')
class DataCleanup(Resource):
    @admin_required
    def delete(self):
        """Видалити застарілі дані"""
        result = clean_old_data(retention_days=365*5)
        if "error" in result:
            return {"error": result["error"]}, 500
        return result, 200

@ns_maintenances.route('/pending-maintenance')
class PendingMaintenanceByTechnician(Resource):
    @admin_required
    def get(self):
        """Отримати записи обслуговування, які очікують на техніка"""
        try:
            pending_records = get_pending_maintenance()
            if not pending_records:
                return {"message": "Немає записів, що очікують на техніка"}, 200
            return {"pending_maintenances": pending_records}, 200
        except RuntimeError as e:
            return {"error": str(e)}, 500