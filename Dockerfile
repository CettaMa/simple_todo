FROM python:3.9-slim-buster

# Set working directory
WORKDIR /apps/

# Debug dan install dependensi sistem
RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Salin file dan folder yang diperlukan
COPY requirements.txt /apps/
COPY app.py /apps/
COPY test_app.py /apps/
COPY static /apps/static
COPY templates /apps/templates

RUN python -m pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Tentukan entrypoint dan command default
ENTRYPOINT ["python"]
CMD ["app.py"]
