FROM python:3.11-slim

# Set working directory to match Django project structure
WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script first and set permissions
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh && \
    sed -i 's/\r$//g' entrypoint.sh

# Copy the rest of the application
COPY . .

# Create directory for static files
RUN mkdir -p staticfiles

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/alerts/ || exit 1
