from flask import request
from flask_restx import Namespace, Resource, fields
from app.models.maintenance import MaintenanceRecord
from app.models.elevator import Elevator
from app.models.technician import Technician
from app import db

ns_maintenances = Namespace('maintenances', description='Операції з обслуговування ліфтів')

# Модель для Swagger-документації
maintenance_model = ns_maintenances.model('MaintenanceRecord', {
    'elevator_id': fields.Integer(required=True, description='ID ліфта'),
    'technician_id': fields.Integer(required=True, description='ID техніка'),
    'maintenance_date': fields.String(required=True, description='Дата обслуговування (у форматі YYYY-MM-DD)'),
    'description': fields.String(required=True, description='Опис обслуговування')
})

@ns_maintenances.route('/')
class MaintenanceListResource(Resource):
    @ns_maintenances.marshal_list_with(maintenance_model)
    def get(self):
        """Отримати список усіх записів обслуговування"""
        records = MaintenanceRecord.query.all()
        return records

    @ns_maintenances.expect(maintenance_model)
    def post(self):
        """Додати новий запис обслуговування"""
        data = request.json
        new_record = MaintenanceRecord(
            elevator_id=data['elevator_id'],
            technician_id=data['technician_id'],
            maintenance_date=data['maintenance_date'],
            description=data['description']
        )
        db.session.add(new_record)
        db.session.commit()
        return {"message": "Запис обслуговування створено"}, 201


@ns_maintenances.route('/<int:record_id>')
@ns_maintenances.param('record_id', 'Унікальний ідентифікатор запису обслуговування')
class MaintenanceResource(Resource):
    @ns_maintenances.marshal_with(maintenance_model)
    def get(self, record_id):
        """Отримати деталі запису обслуговування"""
        record = MaintenanceRecord.query.get_or_404(record_id)
        return record

    def delete(self, record_id):
        """Видалити запис обслуговування"""
        record = MaintenanceRecord.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()
        return {"message": "Запис обслуговування видалено"}, 200
