# Tahap 1: Base Image
FROM python:3.11-slim AS base

# Mengatur variabel lingkungan
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Tetapkan direktori kerja
WORKDIR /app

# Tahap 2: Instalasi uv dan Ketergantungan
# Instal uv (alat packaging Python baru)
# Menggunakan pip untuk instalasi uv adalah metode yang paling sederhana
RUN pip install uv

# Salin file requirements.txt
COPY requirements.txt .

# Gunakan 'uv pip install' sebagai pengganti 'pip install'
# --system memastikan instalasi ke virtual environment sistem
# --no-cache menghapus cache uv setelah instalasi (Opsional: Jaga ukuran image)
RUN uv pip install --system --no-cache -r requirements.txt

# Tahap 3: Final Image
# Salin sisa kode proyek
COPY . .

# Expose port (uvicorn tetap diperlukan untuk menjalankan FastAPI)
EXPOSE 8000

# Perintah untuk menjalankan aplikasi menggunakan Uvicorn
# Pastikan 'uvicorn' ada di requirements.txt Anda.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]