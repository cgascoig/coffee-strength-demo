FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8 as base

FROM base as builder
RUN mkdir /install
WORKDIR /install

RUN apk add build-base build-base linux-headers jpeg-dev zlib-dev python3-dev libffi-dev openssl-dev

COPY requirements.txt /requirements.txt

RUN pip install --install-option="--prefix=/install" -r /requirements.txt


FROM base

COPY --from=builder /install /usr/local

COPY ./app /app