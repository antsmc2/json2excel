FROM python:2.7-alpine

RUN export LC_ALL=en_US.UTF-8
RUN export LANG=en_US.UTF-8

# Copy in your requirements file
ADD pip-requires.txt /pip-requires.txt

RUN set -ex \
    && apk add  gcc g++
# now install python specific dependencies
RUN  LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "pip install -U pip" \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "pip install -r /pip-requires.txt"

# Copy application code to the container
RUN mkdir /src
COPY . /src
WORKDIR /src

EXPOSE 5000

ENTRYPOINT gunicorn --workers=10 --bind 0.0.0.0:5000 wsgi:app
