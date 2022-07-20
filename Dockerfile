# pull official base image
FROM python:3.9.4-alpine
MAINTAINER PCTeam pcteam@bahag.com

# set work directory
WORKDIR /usr/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/:/usr/src/"

# copy requirements file
COPY ./requirements.txt ./requirements.txt

#setting up the virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install dependencies of alpine image
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
        postgresql-dev bash

RUN python -m pip install --upgrade pip

# requirements
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# M1 arm64e architecture
RUN pip install PyHyphen==4.0.3 --no-binary :all:

RUN rm -rf /root/.cache/pip

# copy project
COPY . /usr/

EXPOSE 8000
CMD exec uvicorn app.main:app --host 0.0.0.0 --port 8000

