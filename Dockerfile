# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages
RUN pip install flask

# Set environment variable for Flask
ENV FLASK_APP=app:app

# Expose the port Flask will run on
EXPOSE 5000

# Define the default command
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
