FROM python:2.7.18-slim-buster
RUN mkdir /myapp
WORKDIR /myapp
ADD . /myapp
ENV PYTHONUNBUFFERED=0
RUN apt-get clean && apt-get update && apt-get install -y python-pip \
python-gevent \
python-pip && \
pip install -r /myapp/requirements.txt