FROM docker.io/python:3.7-slim as base

RUN apt-get update \
    && apt-get -y install ffmpeg libsm6 libxext6 xvfb --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt || echo no requirements.txt file

CMD streamlit run app.py --server.port=8000 --browser.serverAddress="0.0.0.0"
