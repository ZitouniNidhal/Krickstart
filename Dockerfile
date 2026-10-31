FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the entire project first (including krickstart and devspeed folders)
COPY pyproject.toml README.md ./
COPY krickstart/ krickstart/

# Install the package
RUN pip install --no-cache-dir .

# Create a non-root user for security
RUN useradd -m -u 1000 appuser
USER appuser

ENTRYPOINT ["krickstart"]
CMD ["--help"] 
