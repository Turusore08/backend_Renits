import os
import pickle
import pandas as pd
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest
from datetime import datetime
from app import db
from app.models import PatchDataModel, PredictionHistoryModel

# --- Memuat Model ---
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, '..', '..', 'model.pkl') 
    with open(model_path, 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    print("Model berhasil dimuat dari resource.")
except Exception as e:
    print(f"ERROR memuat model dari resource: {e}")
    loaded_model = None

# --- Parser ---
predict_parser = reqparse.RequestParser()
predict_parser.add_argument('patch_id', type=str, required=True, help='ID unik dari patch tidak boleh kosong')
predict_parser.add_argument('age', type=float, required=True, help='Nilai age tidak boleh kosong')
predict_parser.add_argument('appetite', type=bool, required=True, help='Nilai appetite tidak boleh kosong')
predict_parser.add_argument('hypertension', type=bool, required=True, help='Nilai hypertension tidak boleh kosong')
predict_parser.add_argument('diabetes_mellitus', type=bool, required=True, help='Nilai diabetes_mellitus tidak boleh kosong')
predict_parser.add_argument('coronary_artery_disease', type=bool, required=True, help='Nilai coronary_artery_disease tidak boleh kosong')
predict_parser.add_argument('peda_edema', type=bool, required=True, help='Nilai peda_edema tidak boleh kosong')

patch_parser = reqparse.RequestParser()
patch_parser.add_argument('patch_id', type=str, required=True, help='ID unik dari patch tidak boleh kosong')
patch_parser.add_argument('sugar', type=int, required=True, help='Nilai sugar dari patch tidak boleh kosong')
patch_parser.add_argument('potassium', type=float, required=True, help='Nilai potassium dari patch tidak boleh kosong')

# --- Resources ---

# --- KELAS YANG HILANG DITAMBAHKAN KEMBALI DI SINI ---
class PatchDataResource(Resource):
    @jwt_required()
    def post(self):
        args = patch_parser.parse_args()
        patch_id = args['patch_id']
        patch_data = PatchDataModel.query.get(patch_id)
        if patch_data:
            patch_data.sugar = args['sugar']
            patch_data.potassium = args['potassium']
            patch_data.timestamp = datetime.utcnow()
        else:
            patch_data = PatchDataModel(patch_id=patch_id, sugar=args['sugar'], potassium=args['potassium'])
            db.session.add(patch_data)
        db.session.commit()
        return {'status': 'success', 'message': f'Data untuk patch {patch_id} berhasil diperbarui di database.'}, 201

class PredictionResource(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        
        if loaded_model is None:
            return {'status': 'error', 'message': 'Model tidak tersedia'}, 500
        try:
            args = predict_parser.parse_args()
            patch_id = args['patch_id']
            patch_data = PatchDataModel.query.get(patch_id)
            
            if not patch_data:
                return {'status': 'error', 'message': f'Data untuk patch ID {patch_id} belum diterima.'}, 404
            
            input_df = pd.DataFrame([{'age': args['age'], 'sugar': patch_data.sugar, 'potassium': patch_data.potassium, 'appetite': args['appetite'], 'hypertension': args['hypertension'], 'diabetes_mellitus': args['diabetes_mellitus'], 'coronary_artery_disease': args['coronary_artery_disease'], 'peda_edema': args['peda_edema']}])
            
            print("\n--- BUKTI DARI SERVER ---", flush=True)
            print("Isi Data (DataFrame):", flush=True)
            print(input_df.to_string(), flush=True)
            print("-------------------------\n", flush=True)

            prediction_result = loaded_model.predict(input_df)
            result_text = "Terindikasi Penyakit Ginjal" if prediction_result[0] == 1 else "Tidak Terindikasi Penyakit Ginjal"
            
            new_history = PredictionHistoryModel(
                user_id=current_user_id,
                prediction_result=result_text,
                age=args['age'],
                sugar=patch_data.sugar,
                potassium=patch_data.potassium,
                hypertension=args['hypertension'],
                diabetes_mellitus=args['diabetes_mellitus']
            )
            db.session.add(new_history)
            db.session.commit()

            return {'status': 'success', 'prediction': result_text, 'used_patch_data': {'sugar': patch_data.sugar, 'potassium': patch_data.potassium}}, 200
        except Exception as e:
            print(f"--- DEBUG: TERJADI ERROR SAAT PREDIKSI: {e} ---", flush=True)
            return {'status': 'error', 'message': f'Terjadi kesalahan tak terduga di server: {str(e)}'}, 500

class GetPatchDataResource(Resource):
    def get(self, patch_id):
        patch_data = PatchDataModel.query.get(patch_id)
        if patch_data:
            return {'status': 'success', 'data': {'sugar': patch_data.sugar, 'potassium': patch_data.potassium, 'timestamp': patch_data.timestamp.isoformat() + "Z"}}, 200
        else:
            return {'status': 'error', 'message': f'Tidak ada data real-time untuk patch ID {patch_id}'}, 404

class HistoryResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        history_records = PredictionHistoryModel.query.filter_by(user_id=current_user_id).order_by(PredictionHistoryModel.timestamp.desc()).all()
        history_list = []
        for record in history_records:
            history_list.append({
                'id': record.id,
                'timestamp': record.timestamp.isoformat() + "Z",
                'prediction_result': record.prediction_result,
                'age': record.age,
                'sugar': record.sugar,
                'potassium': record.potassium,
                'hypertension': record.hypertension,
                'diabetes_mellitus': record.diabetes_mellitus
            })
        return {'status': 'success', 'history': history_list}, 200
