# Menggunakan base image Python resmi yang ringan
FROM python:3.11-slim

# Install system dependencies, Node.js, dan pustaka untuk Puppeteer/whatsapp-web.js
RUN apt-get update && apt-get install -y \
    curl \
    git \
    chromium \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Tentukan direktori kerja di dalam container Railway
WORKDIR /app

# Salin file konfigurasi dependensi terlebih dahulu
COPY package*.json ./
COPY requirements.txt ./

# Install dependensi Node.js dan Python
RUN npm install
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh sisa file proyek ke dalam container
COPY . .

# Perintah untuk menjalankan launcher utama Anda
CMD ["python", "launcher/launcher.py"]