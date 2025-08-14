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
