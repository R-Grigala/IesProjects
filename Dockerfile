FROM python:3.11.1-slim-buster

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN apt-get update && apt-get -y install python3-dev gcc build-essential
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uwsgi", "uwsgi.ini"]