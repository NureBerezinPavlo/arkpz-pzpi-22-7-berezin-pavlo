from app import db

class Threshold(db.Model):
    __tablename__ = 'thresholds'
    id = db.Column(db.Integer, primary_key=True)
    parameter = db.Column(db.String(50), unique=True, nullable=False)  # Наприклад, temperature, humidity
    value = db.Column(db.Float, nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "parameter": self.parameter,
            "value": self.value,
        }