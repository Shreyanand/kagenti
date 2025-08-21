FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY pyproject.toml ./

# Install Python dependencies using pip
RUN pip install --no-cache-dir \
    streamlit>=1.45.1 \
    streamlit-mermaid>=0.3.0 \
    kubernetes>=32.0.1 \
    acp-sdk>=0.10.1 \
    a2a-sdk>=0.2.5 \
    python-keycloak>=5.5.1 \
    "mcp[cli]>=1.3.0"

# Copy the application code
COPY . .

# Set environment variables
ENV PRODUCTION_MODE=True
ENV HOME=/tmp

# Expose port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "--server.address", "0.0.0.0", "Home.py"]
