from flask_restful import Resource, reqparse
from app.models import PatchDataModel
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

# Parser untuk data provisioning
provision_parser = reqparse.RequestParser()
provision_parser.add_argument('patch_id', type=str, required=True, help='Patch ID tidak boleh kosong')

class DeviceProvisionResource(Resource):
    @jwt_required()
    def post(self):
        try:
            args = provision_parser.parse_args()
            patch_id = args['patch_id']
            current_user_id = get_jwt_identity()

            # Cek apakah patch sudah ada, jika tidak, buat baru
            patch = PatchDataModel.query.get(patch_id)
            if not patch:
                patch = PatchDataModel(id=patch_id, owner_id=current_user_id)
                db.session.add(patch)
            else:
                # Pastikan pengguna yang meminta adalah pemilik patch
                if patch.owner_id != int(current_user_id):
                    return {'message': 'Anda tidak memiliki izin untuk perangkat ini'}, 403

            # Buat token dengan waktu kedaluwarsa yang sangat panjang (misal: 1 tahun)
            expires = datetime.timedelta(days=365)
            device_token = create_access_token(identity=patch_id, expires_delta=expires)
            
            db.session.commit()
            
            return {'status': 'success', 'device_token': device_token}, 200

        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': f'Terjadi kesalahan: {str(e)}'}, 500

