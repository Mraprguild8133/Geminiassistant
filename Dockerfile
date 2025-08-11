# Advanced Telegram Bot with Gemini AI - Docker Configuration
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml uv.lock* ./

# Install UV package manager
RUN pip install uv

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Expose webhook port
EXPOSE 5000

# Health check for both services (webhook server responds when both are running)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the application (starts both webhook server and bot simultaneously)
CMD ["python", "main.py"]