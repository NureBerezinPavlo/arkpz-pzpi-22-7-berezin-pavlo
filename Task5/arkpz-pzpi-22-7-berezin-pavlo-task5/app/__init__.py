from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

db = SQLAlchemy()
api = Api(title="Elevator Monitoring API", version="1.0", description="API для управління ліфтами")

def create_app():
    app = Flask(__name__)
    
    # Налаштування
    app.config.from_object('app.config.Config')
    
    # Ініціалізація розширень
    db.init_app(app)
    api.init_app(app)
    
    # Реєстрація моделей
    from app.models import init_models
    init_models(app)
    
    # Реєстрація роутів
    from app.routes import init_routes
    init_routes(api)
    
    return app