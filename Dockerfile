# Use Python 3.10 slim
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy source code
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libglib2.0-0 \
    libgthread-2.0-0 \
    libgl1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, wheel
RUN pip install --upgrade pip setuptools wheel

# Install compatible PyTorch + torchvision (CPU)
RUN pip install torch==2.0.1+cpu torchvision==0.15.2+cpu --extra-index-url https://download.pytorch.org/whl/cpu

# Install pytorch-grad-cam
RUN pip install grad-cam==1.4.6

# Install other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for model caching
RUN mkdir -p /app/models/pytorch

# Expose FastAPI port (port 5000 for consistency)
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the FastAPI app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]
