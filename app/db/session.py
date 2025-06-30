# app/db/session.py - Versi Revisi Final

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# --- Revisi Kritis di Sini ---
# Kita akan membuat argumen koneksi menjadi kondisional.
# Argumen `check_same_thread` hanya diperlukan untuk SQLite.
# Ini akan membuat kode berfungsi di lingkungan lokal (SQLite) dan
# produksi (PostgreSQL) tanpa perlu diubah.

connect_args = {}
# Periksa apakah URL database adalah untuk SQLite
if settings.DATABASE_URL and settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Buat engine dengan argumen yang sudah disesuaikan
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args
)
# --- Akhir Revisi ---


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)