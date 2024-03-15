FROM python:3.13.0a4-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

#RUN apk add --no-cache --virtual .build-deps gcc musl-dev

RUN pip3 install -r requirements.txt

#RUN apk del .build-deps gcc musl-dev

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "openapi_server"]
