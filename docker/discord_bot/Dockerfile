# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUNBUFFERED=1;
ENV RABBIT_HOST=192.168.0.123;
ENV RABBIT_PORT=5672;
ENV DISCORD_TOKEN=OTM5NDgzMDQyMzQ1NTE3MTI2.Yf5fxA.R4v-Z8cIRqLX6QUGUOda6R7msLk

WORKDIR /code
COPY requirements.txt /code/

RUN pip install discord
RUN pip install pika
RUN pip install json

COPY . /code/

CMD [ "python", "./discord_bot_main.py" ]