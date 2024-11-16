# Use an official Python runtime as a base image
FROM python:3.9-slim

# Install necessary system dependencies for Playwright (for Chromium, Firefox, Webkit)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libx11-6 \
    libxcomposite1 \
    libxrandr2 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libdbus-1-3 \
    libxtst6 \
    ca-certificates \
    wget \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browser binaries (Chromium)
RUN python -m playwright install chromium

# Expose the port the app will run on
EXPOSE 5000

# Start the Flask app with Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
