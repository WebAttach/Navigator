# Use the official Python image from Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Define environment variable to make the app run in production mode
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]
