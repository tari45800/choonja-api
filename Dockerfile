FROM python:3.11-slim

WORKDIR /code

COPY ./app /code/app
COPY requirements.txt /code/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
