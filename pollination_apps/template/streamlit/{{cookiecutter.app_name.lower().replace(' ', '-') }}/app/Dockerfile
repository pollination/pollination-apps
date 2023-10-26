FROM docker.io/python:3.7-slim as base

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt || echo no requirements.txt file

CMD streamlit run app.py --server.port=8000 --browser.serverAddress="0.0.0.0"