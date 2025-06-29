# backend/app/models/user_profile.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import datetime

class UserProfile(Base):
    """
    Model untuk menyimpan profil psikologis pengguna yang dianalisis.
    Ini adalah 'memori' jangka panjang sistem tentang pengguna.
    """
    __tablename__ = "user_profiles" # Nama tabel eksplisit

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)

    # Menghubungkan kembali ke model User
    user = relationship("User")

    # Kolom untuk menyimpan hasil 'pembelajaran'
    emerging_themes = Column(JSON, comment="Tema dominan dari jurnal & chat pengguna. Cth: {'pekerjaan': 0.8}")
    sentiment_trend = Column(String, comment="Tren sentimen pengguna. Cth: 'meningkat', 'menurun', 'stabil'")

    last_analyzed = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

