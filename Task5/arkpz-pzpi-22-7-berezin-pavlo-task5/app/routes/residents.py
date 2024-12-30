from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.resident import Resident
from app import db

ns_residents = Namespace('residents', description='Операції з мешканцями')

resident_model = ns_residents.model('Resident', {
    'name': fields.String(required=True, description='Ім’я мешканця'),
    'email': fields.String(required=True, description='Електронна адреса'),
    'password': fields.String(required=True, description='Пароль'),
    'building_id': fields.Integer(required=True, description='ID будинку')
})

login_model = ns_residents.model('Login', {
    'email': fields.String(required=True, description='Електронна адреса'),
    'password': fields.String(required=True, description='Пароль')
})

@ns_residents.route('/register')
class ResidentRegister(Resource):
    @ns_residents.expect(resident_model)
    def post(self):
        """Реєстрація нового мешканця"""
        data = request.json

        # Перевірка, чи email вже існує
        if Resident.query.filter_by(email=data['email']).first():
            return {"error": "Мешканець із таким email вже існує"}, 400

        # Створення нового мешканця
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_resident = Resident(
            name=data['name'],
            email=data['email'],
            password=hashed_password,
            building_id=data['building_id']
        )
        db.session.add(new_resident)
        db.session.commit()

        return {"message": "Реєстрація успішна"}, 201


@ns_residents.route('/login')
class ResidentLogin(Resource):
    @ns_residents.expect(login_model)
    def post(self):
        """Авторизація мешканця"""
        data = request.json
        resident = Resident.query.filter_by(email=data['email']).first()

        if not resident or not check_password_hash(resident.password, data['password']):
            return {"error": "Невірний email або пароль"}, 401

        # Створення токена доступу
        access_token = create_access_token(identity=resident.id)
        return {"access_token": access_token}, 200


@ns_residents.route('/profile')
class ResidentProfile(Resource):
    @jwt_required()
    def get(self):
        """Отримати профіль поточного мешканця"""
        resident_id = get_jwt_identity()
        resident = Resident.query.get(resident_id)

        if not resident:
            return {"error": "Мешканця не знайдено"}, 404

        return {
            "id": resident.id,
            "name": resident.name,
            "email": resident.email,
            "building_id": resident.building_id
        }, 200