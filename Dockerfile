# Use official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Don't write .pyc files, and don't buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies needed for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 120 --retries 5 -r requirements.txt

# Copy all project files into the container
COPY . .

# Create media folder so uploaded files have somewhere to go
RUN mkdir -p /app/media

# Expose Django port
EXPOSE 8000

# Start Daphne (ASGI server) — handles both HTTP and WebSocket
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "nostalgia.asgi:application"]
