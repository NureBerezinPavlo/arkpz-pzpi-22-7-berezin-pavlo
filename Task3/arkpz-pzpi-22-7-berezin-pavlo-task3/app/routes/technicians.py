from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.technician import Technician
from app import db
from app.utils.auth import admin_required

ns_technicians = Namespace('technicians', description='Операції з техніками')

technician_model = ns_technicians.model('Technician', {
    'name': fields.String(required=True, description='Ім’я техніка'),
    'phone_number': fields.String(required=True, description='Номер телефону техніка'),
    'email': fields.String(required=True, description='Email техніка'),
    'password': fields.String(required=True, description='Пароль')
})

login_model = ns_technicians.model('Login', {
    'email': fields.String(required=True, description='Email техніка'),
    'password': fields.String(required=True, description='Пароль')
})

@ns_technicians.route('/register')
class TechnicianRegister(Resource):
    @ns_technicians.expect(technician_model)
    @admin_required
    def post(self):
        """Реєстрація нового техніка"""
        data = request.json

        # Перевірка, чи email вже існує
        if Technician.query.filter_by(email=data['email']).first():
            return {"error": "Технік із таким email вже існує"}, 400

        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

        new_technician = Technician(
            name=data['name'],
            phone_number=data['phone_number'],
            email=data['email'],
            password=hashed_password
        )
        db.session.add(new_technician)
        db.session.commit()

        return {"message": "Техніка успішно зареєстровано"}, 201


@ns_technicians.route('/login')
class TechnicianLogin(Resource):
    @ns_technicians.expect(login_model)
    @admin_required
    def post(self):
        """Авторизація техніка"""
        data = request.json
        technician = Technician.query.filter_by(email=data['email']).first()

        if not technician or not check_password_hash(technician.password, data['password']):
            return {"error": "Невірний email або пароль"}, 401

        # Створення токена доступу
        access_token = create_access_token(identity=technician.id)
        return {"access_token": access_token}, 200


@ns_technicians.route('/profile')
class TechnicianProfile(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        """Отримати профіль поточного техніка"""
        technician_id = get_jwt_identity()
        technician = Technician.query.get(technician_id)

        if not technician:
            return {"error": "Техніка не знайдено"}, 404

        return {
            "id": technician.id,
            "name": technician.name,
            "phone_number": technician.phone_number,
            "email": technician.email
        }, 200