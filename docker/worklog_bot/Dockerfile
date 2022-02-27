FROM python:3.9

WORKDIR /app

USER root

COPY requirements.txt ./

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
