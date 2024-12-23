FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Ensure the static directory is created
RUN mkdir -p /app/static

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libc-dev \
    libffi-dev \
    libssl-dev

ENV PYTHONPATH=/app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port Flask will use
EXPOSE 8000

# Run the Flask app
# CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2", "app:app"]
