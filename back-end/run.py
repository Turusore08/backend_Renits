from app import create_app, db
from app.models import UserModel

# Buat instance aplikasi menggunakan factory
app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    Membuat konteks shell agar bisa mengakses db dan UserModel
    saat menggunakan 'flask shell'.
    """
    return {'db': db, 'UserModel': UserModel}

if __name__ == '__main__':
    # Jalankan aplikasi. Gunakan host='0.0.0.0' agar bisa diakses
    # dari luar container jika menggunakan Docker.
    app.run(host='0.0.0.0', port=5000, debug=False)
