import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource
from flask_cors import CORS
from config import Config

# Inisialisasi ekstensi di luar factory
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api()

def create_app(config_class=Config):
    """
    Application Factory Function.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inisialisasi ekstensi dengan aplikasi
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Daftarkan semua resource ke API
    from app.resources.auth import UserRegister, UserLogin
    from app.resources.prediction import PredictionResource, PatchDataResource, GetPatchDataResource, HistoryResource
    from app.resources.device import DeviceProvisionResource # <-- PASTIKAN IMPOR INI ADA

    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(PatchDataResource, '/patch-data')
    api.add_resource(PredictionResource, '/predict')
    api.add_resource(GetPatchDataResource, '/get-patch-data/<string:patch_id>')
    api.add_resource(DeviceProvisionResource, '/devices/provision') # <-- PASTIKAN PENDAFTARAN INI ADA
    api.add_resource(HistoryResource, '/history')
    # Inisialisasi API dan CORS setelah semua resource terdaftar
    api.init_app(app)
    frontend_url = os.environ.get('FRONTEND_URL') or "http://localhost:3000"
    CORS(app, resources={r"/*": {"origins": frontend_url}})

    # --- Endpoint Ping untuk Debugging ---
    class Ping(Resource):
        def get(self):
            return {'message': 'pong!'}
    api.add_resource(Ping, '/ping')
    # ------------------------------------

    return app
