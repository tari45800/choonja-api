FROM python:3.11-slim

# Install dockerize (waits for MySQL to be ready)
RUN apt-get update && apt-get install -y wget
RUN wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz
RUN tar -xvf dockerize-linux-amd64-v0.6.1.tar.gz && mv dockerize /usr/local/bin/

# Set working directory
WORKDIR /code

# Copy app and requirements
COPY ./app /code/app
COPY requirements.txt /code/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Use dockerize to wait for MySQL and then run the app
CMD ["dockerize", "-wait", "tcp://db:3306", "-timeout", "30s", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
