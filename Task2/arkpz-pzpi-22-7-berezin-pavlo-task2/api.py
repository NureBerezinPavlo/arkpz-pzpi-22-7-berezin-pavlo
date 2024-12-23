from flask import Flask, jsonify
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app.routes.buildings import ns_buildings
from app.routes.elevators import ns_elevators
from app.routes.maintenances import ns_maintenances
from app.routes.technicians import ns_technicians
from app.routes.sensors import ns_sensors
from app.routes.residents import ns_residents
from app import db

app = Flask(__name__)

server = "."
database = "ElevatorMonitoring"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://@{server}/{database}"
    f"?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes"
    f"&Encrypt=Yes&TrustServerCertificate=Yes&charset=utf8"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.config['JWT_SECRET_KEY'] = '1337mysupersecretanddifficultkey1337'
jwt = JWTManager(app)

api = Api(
    app,
    version='1.0',
    title='Building & Elevator API',
    description='API для управління будинками та ліфтами',
    doc='/docs'  # URL для документації Swagger
)

# Підключення Namespace
api.add_namespace(ns_buildings, path='/buildings')
api.add_namespace(ns_elevators, path='/elevators')
api.add_namespace(ns_maintenances, path='/maintenances')
api.add_namespace(ns_technicians, path='/technicians')
api.add_namespace(ns_sensors, path='/sensors')
api.add_namespace(ns_residents, path='/residents')

# Головна сторінка
@app.route('/')
def index():
    return jsonify({"message": "Ласкаво просимо до API для управління будинками та ліфтами!"})


# Запуск застосунку
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Створення таблиць, якщо їх ще немає
    app.run(debug=True)