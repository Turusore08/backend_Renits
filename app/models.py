from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class PatchDataModel(db.Model):
    # --- PERUBAHAN KRITIS DI SINI ---
    # Mengganti nama atribut dari 'id' menjadi 'patch_id' agar lebih deskriptif
    # dan konsisten dengan penggunaan di seluruh aplikasi.
    id = db.Column(db.String(80), primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    sugar = db.Column(db.Integer, nullable=True)
    potassium = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)

class PredictionHistoryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    prediction_result = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Float, nullable=False)
    sugar = db.Column(db.Integer, nullable=False)
    potassium = db.Column(db.Float, nullable=False)
    hypertension = db.Column(db.Boolean, nullable=False)
    diabetes_mellitus = db.Column(db.Boolean, nullable=False)
    # Anda mungkin ingin menambahkan lebih banyak kolom dari kuesioner di sini
