import os

# Dapatkan path absolut ke direktori proyek
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Kelas konfigurasi dasar.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Kunci_ini_Hanya_Diketahui_Oleh_Aku'
    
    # --- PERUBAHAN KRITIS DI SINI ---
    # Alamat koneksi ke database PostgreSQL.
    # Format: postgresql://<user>:<password>@<host>:<port>/<database_name>
    POSTGRES_URL = "postgresql://postgres:Kunci_ini_Hanya_Diketahui_Oleh_Aku@localhost:5432/renits_db"

    # Prioritaskan DATABASE_URL dari environment variable untuk deployment.
    # Jika tidak ada, gunakan konfigurasi PostgreSQL lokal.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or POSTGRES_URL
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
