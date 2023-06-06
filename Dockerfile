FROM python:3.10

COPY ./api /app


COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app/api

CMD while true; do python fill_db.py; sleep 3600; done