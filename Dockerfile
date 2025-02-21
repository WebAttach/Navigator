# Start with a slim Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Upgrade pip
RUN python -m pip install --upgrade pip

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -v -r requirements.txt

# Copy the rest of the application files to the container
COPY . /app/

# Expose port 5000 for Flask
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run Flask application
CMD ["flask", "run"]
