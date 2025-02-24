FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Expose port 5000 for Flask
EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install any additional dependencies or troubleshooting packages
RUN echo "Checking dependencies..." && pip list

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
