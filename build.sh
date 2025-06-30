#!/usr/bin/env bash
# exit on error
set -o errexit

# Instal dependensi Python
pip install -r requirements.txt

# Jalankan migrasi database Alembic
alembic upgrade head