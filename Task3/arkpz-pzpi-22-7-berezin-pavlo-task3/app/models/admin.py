from app import db

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(100), unique=True, nullable=False)
    email = db.Column(db.Unicode(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Хешований пароль

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }