from dotenv import load_dotenv
import os

# --- PERUBAHAN KRITIS DI SINI ---
# Dapatkan path absolut ke direktori root proyek (folder yang berisi file ini)
base_dir = os.path.abspath(os.path.dirname(__file__))

# Muat environment variables dari file .env yang ada di direktori root proyek
load_dotenv(os.path.join(base_dir, '.env'))

class Config:
    """
    Kelas konfigurasi yang membaca nilai dari environment variables.
    Ini adalah pendekatan yang aman dan siap untuk deployment.
    """
    # Ambil SECRET_KEY dari .env. Jika tidak ada, akan error (ini bagus untuk keamanan).
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Ambil DATABASE_URL dari .env.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
