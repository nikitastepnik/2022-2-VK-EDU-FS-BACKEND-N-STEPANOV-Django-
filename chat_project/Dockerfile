FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LISTEN_PORT=9000
EXPOSE 9000

ADD /requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD / /chat_project

WORKDIR /chat_project

