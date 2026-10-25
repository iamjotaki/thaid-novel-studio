# Use official Playwright Python image (comes with all browser dependencies pre-installed)
FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    TZ=Asia/Bangkok \
    DEBIAN_FRONTEND=noninteractive

# Install additional fonts for Thai language rendering and timezone data
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    fonts-thai-tlwg \
    fonts-noto-cjk \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specifications
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium browser
RUN playwright install chromium

# Copy application source code
COPY . .

# Create persistent storage directories
RUN mkdir -p /app/data /app/user_sessions /app/data/covers

# Expose server port
EXPOSE 8080

# Run SaaS Server
CMD ["python", "server_saas.py"]
