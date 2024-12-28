from flask import request
from flask_restx import Namespace, Resource, fields
from app.models.threshold import Threshold
from app import db
from app.utils.auth import admin_required

ns_thresholds = Namespace('thresholds', description='Керування пороговими значеннями')

threshold_model = ns_thresholds.model('Threshold', {
    'parameter': fields.String(required=True, description='Назва параметра (temperature, humidity, weight)'),
    'value': fields.Float(required=True, description='Порогове значення параметра')
})

@ns_thresholds.route('/')
class ThresholdListResource(Resource):
    @ns_thresholds.marshal_list_with(threshold_model)
    @admin_required
    def get(self):
        """Отримати список усіх порогових значень"""
        thresholds = Threshold.query.all()
        return thresholds

    @ns_thresholds.expect(threshold_model)
    @admin_required
    def post(self):
        """Додати нове порогове значення"""
        data = request.json
        new_threshold = Threshold(
            parameter=data['parameter'],
            value=data['value']
        )
        db.session.add(new_threshold)
        db.session.commit()
        return {"message": "Порогове значення створено"}, 201

@ns_thresholds.route('/<string:parameter>')
@ns_thresholds.param('parameter', 'Назва параметра (temperature, humidity, weight)')
class ThresholdResource(Resource):
    @ns_thresholds.expect(threshold_model)
    @admin_required
    def put(self, parameter):
        """Оновити порогове значення"""
        data = request.json
        threshold = Threshold.query.filter_by(parameter=parameter).first()
        if not threshold:
            return {"error": "Параметр не знайдено"}, 404

        threshold.value = data['value']
        db.session.commit()
        return {"message": "Порогове значення оновлено"}, 200

    @admin_required
    def delete(self, parameter):
        """Видалити порогове значення"""
        threshold = Threshold.query.filter_by(parameter=parameter).first()
        if not threshold:
            return {"error": "Параметр не знайдено"}, 404

        db.session.delete(threshold)
        db.session.commit()
        return {"message": "Порогове значення видалено"}, 200