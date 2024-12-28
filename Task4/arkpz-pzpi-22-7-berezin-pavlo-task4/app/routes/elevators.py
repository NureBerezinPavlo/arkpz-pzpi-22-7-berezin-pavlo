from flask import request
from flask_restx import Namespace, Resource, fields
from app.models.elevator import Elevator
from app import db
from app.utils.auth import admin_required

ns_elevators = Namespace('elevators', description='Операції з ліфтами')

# Опис моделі для Swagger-документації
elevator_model = ns_elevators.model('Elevator', {
    'building_id': fields.Integer(required=True, description='ID будівлі, до якої належить ліфт'),
    'serial_number': fields.String(required=True, description='Серійний номер ліфта'),
    'status': fields.String(required=True, description='Статус ліфта (наприклад, "active", "maintenance")'),
    'install_date': fields.String(required=False, description='Дата встановлення ліфта (у форматі YYYY-MM-DD)')
})

@ns_elevators.route('/')
class ElevatorListResource(Resource):
    @ns_elevators.marshal_list_with(elevator_model)
    @admin_required
    def get(self):
        """Отримати список усіх ліфтів"""
        elevators = Elevator.query.all()
        return elevators

    @ns_elevators.expect(elevator_model)
    @admin_required
    def post(self):
        """Створити новий ліфт"""
        data = request.json
        new_elevator = Elevator(
            building_id=data['building_id'],
            serial_number=data['serial_number'],
            status=data['status'],
            install_date=data.get('install_date')  # Перевірка наявності дати
        )
        db.session.add(new_elevator)
        db.session.commit()
        return {"message": "Ліфт створено"}, 201


@ns_elevators.route('/<int:elevator_id>')
@ns_elevators.param('elevator_id', 'Унікальний ідентифікатор ліфта')
class ElevatorResource(Resource):
    @ns_elevators.marshal_with(elevator_model)
    @admin_required
    def get(self, elevator_id):
        """Отримати інформацію про конкретний ліфт"""
        elevator = Elevator.query.get_or_404(elevator_id)
        return elevator

    @ns_elevators.expect(elevator_model)
    @admin_required
    def put(self, elevator_id):
        """Оновити інформацію про ліфт"""
        data = request.json
        elevator = Elevator.query.get_or_404(elevator_id)

        elevator.status = data.get('status', elevator.status)
        elevator.serial_number = data.get('serial_number', elevator.serial_number)
        elevator.install_date = data.get('install_date', elevator.install_date)

        db.session.commit()
        return {"message": "Ліфт оновлено"}, 200

    @admin_required
    def delete(self, elevator_id):
        """Видалити ліфт"""
        elevator = Elevator.query.get_or_404(elevator_id)
        db.session.delete(elevator)
        db.session.commit()
        return {"message": "Ліфт видалено"}, 200