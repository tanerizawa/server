# backend/app/celery_app.py

import os
from celery import Celery

# Ambil URL Redis dari environment variable
redis_url = f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', '6379')}/0"

# Inisialisasi Celery
celery_app = Celery(
    "tasks",
    broker=redis_url,
    backend=redis_url,
    include=["app.tasks"] # Tunjuk ke file tempat task didefinisikan
)