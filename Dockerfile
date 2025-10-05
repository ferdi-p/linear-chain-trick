# Minimal Dockerfile for NiceGUI on Fly.io
FROM python:3.11-slim

# System deps for SciPy & matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gfortran libatlas-base-dev liblapack-dev libfreetype6-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# NiceGUI serves on 8080 below
EXPOSE 8080
CMD ["python", "main.py"]
