# backend/Dockerfile

# Gunakan base image Python resmi
FROM python:3.11-slim

# Set direktori kerja di dalam kontainer
WORKDIR /app

# Set variabel lingkungan agar output Python tidak di-buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instal dependensi sistem yang mungkin diperlukan
RUN apt-get update && apt-get install -y build-essential

# Instal dependensi Python
# Menyalin requirements.txt terlebih dahulu memanfaatkan cache Docker
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
RUN pip install --no-cache /usr/src/app/wheels/*

# Salin seluruh kode aplikasi ke dalam direktori kerja
COPY . .