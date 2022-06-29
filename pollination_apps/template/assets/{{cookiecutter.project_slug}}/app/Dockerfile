FROM python:3.7-slim as base

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt || echo no requirements.txt file
