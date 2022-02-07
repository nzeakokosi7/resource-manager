 # pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apk update \
    && apk add --virtual build-essential gcc python3-dev musl-dev

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

RUN python manage.py makemigrations --no-input
RUN python manage.py migrate --no-input
RUN python manage.py initadmin
# add and run as non-root user
USER root

RUN chown -R root /app
RUN chmod 755 /app

# run gunicorn
CMD gunicorn resourceManager.wsgi:application --bind 0.0.0.0:$PORT