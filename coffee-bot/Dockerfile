FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

RUN apk add --no-cache --virtual .build-deps build-base linux-headers 
RUN apk add --no-cache jpeg-dev zlib-dev

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./app /app