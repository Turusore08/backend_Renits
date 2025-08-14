from flask_restful import Resource, reqparse
from app.models import UserModel
from app import db
from flask_jwt_extended import create_access_token

# Parser untuk data pengguna
user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True, help='Email tidak boleh kosong')
user_parser.add_argument('password', type=str, required=True, help='Password tidak boleh kosong')

class UserRegister(Resource):
    def post(self):
        args = user_parser.parse_args()
        if UserModel.query.filter_by(email=args['email']).first():
            return {'message': 'Pengguna dengan email ini sudah ada'}, 400
        
        new_user = UserModel(email=args['email'])
        new_user.set_password(args['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Registrasi berhasil'}, 201

class UserLogin(Resource):
    def post(self):
        args = user_parser.parse_args()
        user = UserModel.query.filter_by(email=args['email']).first()
        if user and user.check_password(args['password']):
            # --- PERBAIKAN KRITIS DI SINI ---
            # Pastikan identitas dikonversi menjadi string.
            access_token = create_access_token(identity=str(user.id))
            return {'access_token': access_token}, 200
        return {'message': 'Email atau password salah'}, 401
