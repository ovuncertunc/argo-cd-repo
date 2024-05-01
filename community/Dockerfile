# syntax=docker/dockerfile:1
FROM python:3.10.12
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY .env-container .env
COPY . .
RUN pip install -r requirements.txt