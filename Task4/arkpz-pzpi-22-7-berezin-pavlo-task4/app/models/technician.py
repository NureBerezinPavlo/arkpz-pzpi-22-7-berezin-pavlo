from app import db

# Модель технічного персоналу
class Technician(db.Model):
    __tablename__ = 'technicians'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), nullable=False)
    phone_number = db.Column(db.Unicode(15), unique=True, nullable=False)
    email = db.Column(db.Unicode(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Для збереження хешованого пароля
    maintenance_records = db.relationship('MaintenanceRecord', backref='technician', lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "password": self.password
        }