from app import db

class Building(db.Model):
    __tablename__ = 'buildings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), nullable=False)
    address = db.Column(db.Unicode(200), nullable=False)
    num_floors = db.Column(db.Integer, nullable=False)