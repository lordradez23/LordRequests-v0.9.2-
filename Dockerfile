# For development purposes
# Use a python base image
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the library
COPY . .

# Install the library and its dependencies
RUN pip install .[all]

# Run a sample script or the dashboard
CMD ["python", "-m", "hrequests", "dashboard"]
