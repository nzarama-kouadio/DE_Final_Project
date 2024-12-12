# # Stage 1: Build dependencies and application
# FROM python:3.9-slim-buster as builder

# # Set working directory
# WORKDIR /app

# # Ensure the static directory is created
# RUN mkdir -p /app/static

# # Install build tools and Python dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     gcc \
#     libc-dev \
#     libffi-dev \
#     libssl-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Copy the requirements and install dependencies
# COPY requirements.txt ./
# RUN pip install --upgrade pip
# RUN pip install --prefix=/python --no-cache-dir -r requirements.txt

# # Copy application code
# COPY . .

# # Stage 2: Use distroless image
# FROM gcr.io/distroless/python3

# # Copy application and Python environment from builder
# COPY --from=builder /python /python
# COPY --from=builder /app /app

# # Set environment variables
# COPY . .

# # Expose the port Flask will use
# EXPOSE 8000

# # Run the Flask app
# CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]

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