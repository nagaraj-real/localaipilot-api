FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl && apt-get install -y build-essential

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN pip install gunicorn

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

ENTRYPOINT ["sh", "-c", "./use_model.sh && gunicorn app:app"]


