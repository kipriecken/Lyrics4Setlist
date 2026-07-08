# Use an official, lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Flask or the WSGI server runs on
EXPOSE 8000

# Run the application using Gunicorn for production stability
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

