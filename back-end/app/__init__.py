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
    
    # Impor resource di sini
    from app.resources.auth import UserRegister, UserLogin
    from app.resources.prediction import PredictionResource, PatchDataResource, GetPatchDataResource, HistoryResource # <-- Tambahkan HistoryResource

    class Ping(Resource):
        def get(self):
            return {'message': 'pong!'}

    # Daftarkan semua resource
    api.add_resource(Ping, '/ping')
    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(PatchDataResource, '/patch-data')
    api.add_resource(PredictionResource, '/predict')
    api.add_resource(GetPatchDataResource, '/get-patch-data/<string:patch_id>')
    api.add_resource(HistoryResource, '/history') # <-- TAMBAHKAN INI

    # Inisialisasi 'api' dengan 'app'
    api.init_app(app)

    # Terapkan CORS
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    return app
