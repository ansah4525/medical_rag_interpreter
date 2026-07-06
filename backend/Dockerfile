# --------------------------------------------------
# Use an official lightweight Python image
# This image already has Python 3.11 installed.
# --------------------------------------------------
FROM python:3.11-slim

# --------------------------------------------------
# Set the working directory inside the container.
# Every following command runs inside /app.
# --------------------------------------------------
WORKDIR /app

# --------------------------------------------------
# Install system packages required by the project.
#
# tesseract-ocr : OCR engine used by pytesseract
# libgl1        : Required by Pillow/OpenCV on Linux
# --------------------------------------------------
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------
# Copy requirements first.
#
# We do this before copying the project because Docker
# caches this layer. If your code changes but the
# requirements don't, Docker won't reinstall packages.
# This speeds up future builds.
# --------------------------------------------------
COPY requirements.txt .

# --------------------------------------------------
# Install Python dependencies.
# --------------------------------------------------
RUN pip install --no-cache-dir -r requirements.txt

# --------------------------------------------------
# Copy the entire project into the container.
# --------------------------------------------------
COPY . .

# --------------------------------------------------
# Tell Docker this application listens on port 8000.
# --------------------------------------------------
EXPOSE 8000

# --------------------------------------------------
# Start the Flask application.
# --------------------------------------------------
CMD ["python", "-m", "backend.app"]