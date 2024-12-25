from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.admin import Admin
from app import db

ns_admins = Namespace('admins', description='Функції адміністрування')

admin_model = ns_admins.model('Admin', {
    'username': fields.String(required=True, description='Ім’я адміністратора'),
    'email': fields.String(required=True, description='Email адміністратора'),
    'password': fields.String(required=True, description='Пароль')
})

@ns_admins.route('/register')
class AdminRegister(Resource):
    @ns_admins.expect(admin_model)
    def post(self):
        """Реєстрація нового адміністратора"""
        data = request.json

        if Admin.query.filter_by(email=data['email']).first():
            return {"error": "Адміністратор із таким email вже існує"}, 400

        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_admin = Admin(
            username=data['username'],
            email=data['email'],
            password=hashed_password
        )
        db.session.add(new_admin)
        db.session.commit()

        return {"message": "Адміністратор успішно зареєстрований"}, 201

@ns_admins.route('/login')
class AdminLogin(Resource):
    @ns_admins.expect(admin_model)
    def post(self):
        """Авторизація адміністратора"""
        data = request.json
        admin = Admin.query.filter_by(email=data['email']).first()

        if not admin or not check_password_hash(admin.password, data['password']):
            return {"error": "Невірний email або пароль"}, 401

        access_token = create_access_token(identity=admin.id)
        return {"access_token": access_token}, 200