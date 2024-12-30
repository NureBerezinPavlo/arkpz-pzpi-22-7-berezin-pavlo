from app import db
from app.utils.clean_old_data import clean_old_data
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app.routes.buildings import ns_buildings
from app.routes.elevators import ns_elevators
from app.routes.maintenances import ns_maintenances
from app.routes.technicians import ns_technicians
from app.routes.sensors import ns_sensors
from app.routes.residents import ns_residents
from app.routes.reports import ns_reports
from app.routes.thresholds import ns_thresholds
from app.routes.admins import ns_admins
from app.routes.backup import ns_backup

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
    title='Elevator Monitoring API',
    description='API для масового обслуговування та моніторінгу стану ліфтів в житлових комплексах',
    doc='/docs',  # URL для документації Swagger
    security='BearerAuth',  # Використовувати BearerAuth для всієї документації
    authorizations={
        'BearerAuth': {
            'type': 'apiKey',
            'in': 'header',  # Token передається в заголовку
            'name': 'Authorization',  # Назва заголовка для токена
            'description': 'Введіть токен у форматі Bearer <Ваш_Token>'
        }
    }
)

# Підключення Namespace
api.add_namespace(ns_buildings, path='/buildings')
api.add_namespace(ns_elevators, path='/elevators')
api.add_namespace(ns_maintenances, path='/maintenances')
api.add_namespace(ns_technicians, path='/technicians')
api.add_namespace(ns_sensors, path='/sensors')
api.add_namespace(ns_residents, path='/residents')
api.add_namespace(ns_reports, path='/reports')
api.add_namespace(ns_thresholds, path='/thresholds')
api.add_namespace(ns_admins, path='/admins')
api.add_namespace(ns_backup, path='/backup')

# Головна сторінка
@app.route('/')
def index():
    return jsonify({"message": "Ласкаво просимо до API для управління будинками та ліфтами!"})

def schedule_tasks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=clean_old_data, trigger="interval", days=1)  # Щоденне очищення
    scheduler.start()

# Запуск застосунку
if __name__ == '__main__':
    with app.app_context():
        print("Starting Flask server...")
        db.create_all()  # Створення таблиць, якщо їх ще немає
        schedule_tasks()
    app.run(debug=True)