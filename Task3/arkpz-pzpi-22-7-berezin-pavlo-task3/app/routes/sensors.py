from flask import request
from flask_restx import Namespace, Resource, fields
from app.models.sensor import SensorLog
from app import db

ns_sensors = Namespace('sensors', description='Операції з сенсорами')

# Модель для Swagger-документації
sensor_log_model = ns_sensors.model('SensorLog', {
    'elevator_id': fields.Integer(required=True, description='ID ліфта'),
    'timestamp': fields.String(required=True, description='Час запису (у форматі YYYY-MM-DD HH:MM:SS)'),
    'temperature': fields.Float(required=False, description='Температура'),
    'humidity': fields.Float(required=False, description='Вологість'),
    'weight': fields.Float(required=False, description='Вага'),
    'event_type': fields.String(required=True, description='Тип події (наприклад, normal, error)'),
    'message': fields.String(required=False, description='Додаткове повідомлення')
})

@ns_sensors.route('/')
class SensorLogListResource(Resource):
    @ns_sensors.marshal_list_with(sensor_log_model)
    def get(self):
        """Отримати список усіх записів сенсорів"""
        logs = SensorLog.query.all()
        return logs

    @ns_sensors.expect(sensor_log_model)
    def post(self):
        """Додати новий запис сенсора"""
        data = request.json
        new_log = SensorLog(
            elevator_id=data['elevator_id'],
            timestamp=data['timestamp'],
            temperature=data.get('temperature'),
            humidity=data.get('humidity'),
            weight=data.get('weight'),
            event_type=data['event_type'],
            message=data.get('message')
        )
        db.session.add(new_log)
        db.session.commit()
        return {"message": "Запис сенсора створено"}, 201


@ns_sensors.route('/<int:log_id>')
@ns_sensors.param('log_id', 'Унікальний ідентифікатор запису сенсора')
class SensorLogResource(Resource):
    @ns_sensors.marshal_with(sensor_log_model)
    def get(self, log_id):
        """Отримати деталі запису сенсора"""
        log = SensorLog.query.get_or_404(log_id)
        return log

    def delete(self, log_id):
        """Видалити запис сенсора"""
        log = SensorLog.query.get_or_404(log_id)
        db.session.delete(log)
        db.session.commit()
        return {"message": "Запис сенсора видалено"}, 200
    
@ns_sensors.route('/analyze')
class SensorDataAnalyzer(Resource):
    @ns_sensors.expect(sensor_log_model)  # Додаємо очікувану модель
    def post(self):
        """Аналіз даних сенсорів"""
        from app.utils.sensor_analysis import analyze_sensor_data
        data = request.json
        alerts = analyze_sensor_data(data)

        if alerts:
            # Збереження критичних подій у базі даних
            new_log = SensorLog(
                elevator_id=data["elevator_id"],
                timestamp=data["timestamp"],
                temperature=data.get("temperature"),
                humidity=data.get("humidity"),
                weight=data.get("weight"),
                event_type="critical",
                message=", ".join(alerts)
            )
            db.session.add(new_log)
            db.session.commit()

            return {"alerts": alerts, "message": "Критичні події збережено"}, 201
        else:
            return {"message": "Дані у межах норми"}, 200