FROM python:3.13-alpine

WORKDIR /app

COPY .env /app/
COPY requirements.txt /app/
COPY src/ /app/

RUN pip install --no-cache-dir --upgrade -r requirements.txt