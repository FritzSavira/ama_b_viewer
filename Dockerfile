# Use the official Python image
FROM python:3.11-slim

# Set environment variables for Python .
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1        

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]