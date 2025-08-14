<<<<<<< HEAD
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

flask db upgrade
=======
#!/usr/bin/env bash
# exit on error
set -o errexit

# --- PERUBAHAN KRITIS UNTUK DEBUGGING ---
# Tampilkan isi requirements.txt untuk verifikasi
echo "--- Menampilkan isi requirements.txt ---"
cat requirements.txt
echo "------------------------------------"

pip install -r requirements.txt

flask db upgrade
>>>>>>> 842ccc201207f8e5287f310d4f6704aab83210cc
