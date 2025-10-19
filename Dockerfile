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

# Copy the application code to the working directory
COPY . .

# Command for stating the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
