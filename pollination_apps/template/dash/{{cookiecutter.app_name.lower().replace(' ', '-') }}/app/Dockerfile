FROM docker.io/python:3.12-slim as base

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt || echo no requirements.txt file

CMD gunicorn app:server --workers=1 --bind=0.0.0.0:8000