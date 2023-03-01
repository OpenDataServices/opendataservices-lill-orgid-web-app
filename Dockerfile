FROM python:3.9-bullseye

# Setup

WORKDIR /app
COPY . .


RUN apt-get update
RUN apt-get --assume-yes install gettext nginx libpq-dev

# Python

RUN pip install -r requirements.txt

# Webserver

COPY docker/nginx.conf /etc/nginx/sites-available/default

# Run

EXPOSE 80

CMD /bin/bash -c "/etc/init.d/nginx start && gunicorn --bind 0.0.0.0:8000 lillorgid.webapp.app:app"
