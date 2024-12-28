from app import db

# Модель мешканця
class Resident(db.Model):
    __tablename__ = 'residents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), nullable=False)
    email = db.Column(db.Unicode(100), unique=True, nullable=False)
    password = db.Column(db.Unicode(200), nullable=False)  # Зберігати хеш пароля!
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "building_id": self.building_id
        }