# Use a base image with Python 3.13 (compatible with Hugging Face)
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy your code into the container
COPY app /app

# Install system-level dependencies (optional, add if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose the port used by your app (e.g., 7860 for Gradio)
EXPOSE 7860

# Run your app
CMD ["python", "app.py"]
