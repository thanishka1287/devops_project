# ==========================================================
# Dockerfile: Dockerized Online Bookstore
# Base Image: Python 3.11 Slim (Debian-based minimal image)
# ==========================================================

FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    DATABASE_PATH=/app/data/bookstore.db \
    FLASK_ENV=production

# Set application working directory
WORKDIR /app

# Create a non-privileged user and application data directory for SQLite persistence
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /app

# Copy dependency specifications first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies without caching build artifacts to keep image slim
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Ensure appuser owns the application files and data directory
RUN chown -R appuser:appuser /app

# Switch to non-root user for security best practices
USER appuser

# Expose container port to host
EXPOSE 5000

# Health check to ensure the Flask container is responsive
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Launch application using Gunicorn production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "app:create_app()"]
