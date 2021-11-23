FROM python:3.9

LABEL maintainer "DataMade <info@datamade.us>"

RUN apt-get update && \
    apt-get install -y curl

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of the current host directory (i.e., our app code) into
# the container.
COPY . /app

ENV DJANGO_SECRET_KEY 'foobar'
RUN python manage.py collectstatic --noinput
