# Use the official Python image as the base image
FROM python:3.11.2

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install setuptools and pip (ensure they are up-to-date)
RUN pip install --no-cache-dir --upgrade pip setuptools

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright system dependencies
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxkbcommon0 \
    libasound2 \
    libatspi2.0-0 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Playwright browsers (Chromium)
RUN python -m playwright install chromium

# Copy the application code to the working directory
COPY . .

# Command for stating the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
