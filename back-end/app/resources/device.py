from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from app.models import UserModel, PatchDataModel
from app import db

# Parser untuk permintaan provisioning
provision_parser = reqparse.RequestParser()
provision_parser.add_argument('patch_id', type=str, required=True, help='Patch ID tidak boleh kosong')

class DeviceProvisionResource(Resource):
    @jwt_required() # Wajib: Hanya pengguna yang sudah login yang bisa mendaftarkan perangkat
    def post(self):
        """
        Endpoint untuk membuat token JWT berumur panjang khusus untuk sebuah perangkat.
        """
        user_id = get_jwt_identity()
        args = provision_parser.parse_args()
        patch_id = args['patch_id']

        # Opcional tapi direkomendasikan: Cek apakah patch_id sudah terdaftar
        # Ini mencegah satu patch digunakan oleh banyak orang.
        existing_patch = PatchDataModel.query.get(patch_id)
        if existing_patch and existing_patch.owner_id != int(user_id):
            return {'message': 'Patch ID ini sudah terdaftar oleh pengguna lain.'}, 409 # 409 Conflict

        # Buat token baru dengan identitas berupa patch_id dan waktu kedaluwarsa yang panjang
        # timedelta(days=365) berarti token ini valid selama 1 tahun.
        device_token = create_access_token(identity=patch_id, expires_delta=timedelta(days=365))

        # Simpan hubungan antara pengguna dan patch_id ke database
        if not existing_patch:
            patch_record = PatchDataModel.query.get(patch_id)
            if patch_record:
                patch_record.owner_id = int(user_id)
            # Jika Anda ingin membuat record baru saat provisioning, lakukan di sini.
            # Namun, arsitektur kita saat ini membuat record saat data pertama kali dikirim.
            # Kita hanya akan menetapkan pemiliknya.
            # Ini memerlukan modifikasi pada PatchDataModel.
        
        print(f"Pengguna ID {user_id} membuat token untuk Patch ID {patch_id}")
        
        return {'status': 'success', 'device_token': device_token}, 200
