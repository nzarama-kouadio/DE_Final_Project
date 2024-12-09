# Use Python Distroless Image
FROM gcr.io/distroless/python3

# Set the working directory
WORKDIR /app

# Copy application dependencies
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . ./

# Expose port
EXPOSE 5000

# Run the application
CMD ["app.py"]