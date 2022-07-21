FROM python:3.10.4-alpine

ENV APP_DIR=/home/app
ENV SERVER_DIR=/home/app/server

RUN mkdir $APP_DIR
RUN mkdir $APP_DIR/static
RUN mkdir $APP_DIR/uploads
RUN mkdir $SERVER_DIR

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add libpq postgresql-dev gcc python3-dev musl-dev \
    && pip install --upgrade pip

WORKDIR $APP_DIR
COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR $SERVER_DIR
COPY server .

ENTRYPOINT ["/home/app/server/entrypoint.sh"]