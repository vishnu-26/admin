# syntax=docker/dockerfile:1
#!/bin/sh
FROM ubuntu
RUN apt-get update 
RUN apt-get install -y gcc g++ build-essential
RUN apt-get install -y libpq-dev python-dev

FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install -r requirements.txt
COPY . . 

CMD python3 manage.py runserver 0.0.0.0:8000
