from flask import request
from flask_restx import Namespace, Resource, fields
from app.models.sensor import SensorLog
from app import db
from app.utils.auth import admin_required

ns_sensors = Namespace('sensors', description='Операції з сенсорами')

# Модель для Swagger-документації
sensor_log_model = ns_sensors.model('SensorLog', {
    'elevator_id': fields.Integer(required=True, description='ID ліфта'),
    'timestamp': fields.String(required=True, description='Час запису (у форматі YYYY-MM-DD HH:MM:SS)'),
    'temperature': fields.Float(required=False, description='Температура'),
    'humidity': fields.Float(required=False, description='Вологість'),
    'weight': fields.Float(required=False, description='Вага'),
    'event_type': fields.String(required=True, description='Тип події (normal або critical)'),
    'message': fields.String(required=False, description='Додаткове повідомлення'),
    'is_power_on': fields.Boolean(required=True, description='Чи є електропостачання'),
    'is_moving': fields.Boolean(required=True, description='Чи переміщується ліфт'),
    'is_stuck': fields.Boolean(required=True, description='Чи застряг ліфт')
})

@ns_sensors.route('/')
class SensorLogListResource(Resource):
    @ns_sensors.marshal_list_with(sensor_log_model)
    @admin_required
    def get(self):
        """Отримати список усіх записів сенсорів"""
        logs = SensorLog.query.all()
        return logs

    @ns_sensors.expect(sensor_log_model, validate=False)
    @admin_required
    def post(self):
        """Додати новий запис сенсора"""
        from app.utils.sensor_analysis import analyze_sensor_data

        data = request.json

        # Аналіз даних для визначення типу події та генерації повідомлень
        alerts, event_type = analyze_sensor_data(data)

        new_log = SensorLog(
            elevator_id=data['elevator_id'],
            timestamp=data['timestamp'],
            temperature=data.get('temperature'),
            humidity=data.get('humidity'),
            weight=data.get('weight'),
            event_type=event_type,
            message=", ".join(alerts) if alerts else None,
            is_power_on=data['is_power_on'],
            is_moving=data['is_moving'],
            is_stuck=data['is_stuck']
        )
        db.session.add(new_log)
        db.session.commit()

        if event_type == "critical":
            return {"alerts": alerts, "event_type": event_type, "message": "Критичні події збережено"}, 201
        else:
            return {"event_type": event_type, "message": "Дані у межах норми"}, 200

@ns_sensors.route('/<int:log_id>')
@ns_sensors.param('log_id', 'Унікальний ідентифікатор запису сенсора')
class SensorLogResource(Resource):
    @ns_sensors.marshal_with(sensor_log_model)
    @admin_required
    def get(self, log_id):
        """Отримати деталі запису сенсора"""
        log = SensorLog.query.get_or_404(log_id)
        return log
    
    @admin_required
    def delete(self, log_id):
        """Видалити запис сенсора"""
        log = SensorLog.query.get_or_404(log_id)
        db.session.delete(log)
        db.session.commit()
        return {"message": "Запис сенсора видалено"}, 200


@ns_sensors.route('/analyze')
class SensorDataAnalyzer(Resource):
    @ns_sensors.expect(sensor_log_model)
    @admin_required
    def post(self):
        """Аналіз даних сенсорів"""
        from app.utils.sensor_analysis import analyze_sensor_data
        data = request.json

        # Аналіз даних сенсора
        alerts, event_type = analyze_sensor_data(data)

        # Збереження результату в базу даних
        new_log = SensorLog(
            elevator_id=data["elevator_id"],
            timestamp=data["timestamp"],
            temperature=data.get("temperature"),
            humidity=data.get("humidity"),
            weight=data.get("weight"),
            event_type=event_type,
            message=", ".join(alerts) if alerts else None
        )
        db.session.add(new_log)
        db.session.commit()

        if event_type == "critical":
            return {
                "alerts": alerts,
                "event_type": event_type,
                "message": "Критичні події збережено"
            }, 201
        else:
            return {
                "event_type": event_type,
                "message": "Дані у межах норми"
            }, 200