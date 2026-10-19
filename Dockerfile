# Use a slim Python image for a smaller footprint
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

WORKDIR $APP_HOME

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install the project
COPY pyproject.toml .
COPY devspeed/ devspeed/
RUN pip install --no-cache-dir .

# Create a non-root user for security
RUN useradd -m devspeeduser
USER devspeeduser

# Default command
ENTRYPOINT ["devspeed"]
CMD ["--help"]
