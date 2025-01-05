FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN pip install docx2txt

RUN pip install gunicorn

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

COPY ./ragdir /ragdir

RUN chmod +x use_model.sh

ENTRYPOINT ["sh", "-c", "./use_model.sh && gunicorn app:app"]


