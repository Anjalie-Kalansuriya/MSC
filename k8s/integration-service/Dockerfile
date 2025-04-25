# Use a lightweight Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for MySQL
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app runs on
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
