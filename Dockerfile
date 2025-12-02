FROM python:3.8-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir spleeter flask flask-cors

# Copy server file
COPY simple_separator.py .

# Expose port
EXPOSE 5000

# Run server
CMD ["python", "simple_separator.py"]
