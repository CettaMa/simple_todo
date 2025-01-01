# Gunakan image Python sebagai base image
FROM python:3.8-slim

# Set working directory di dalam container
WORKDIR /app

# Menyalin semua file dari direktori lokal ke dalam container
COPY . /app

# Install dependensi aplikasi
RUN pip install --no-cache-dir -r requirements.txt

# Menentukan perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]
