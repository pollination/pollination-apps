FROM python:3.7-slim as base

RUN pip install --upgrade pip

WORKDIR /app

COPY . .

RUN [ -e "./requirements.txt" ] && pip install --no-cache-dir -r requirements.txt || echo no requirements.txt file
