# Menggunakan base image Python versi 3.9
FROM python:3.9-slim

# Set working directory
WORKDIR /apps/

# Install alat build tambahan
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Salin file dan folder yang diperlukan
COPY requirements.txt /apps/
COPY app.py /apps/
COPY test_app.py /apps/
COPY static /apps/static
COPY templates /apps/templates

RUN pip install -U pip setuptools && pip install -r requirements.txt

EXPOSE 5000

# Tentukan entrypoint dan command default
ENTRYPOINT ["python"]
CMD ["app.py"]
