FROM alpine:3.7

RUN apk add --no-cache --update \
        python3 \
    	uwsgi \
    	uwsgi-python3

RUN mkdir /app

WORKDIR /app

COPY requirements.freeze.txt /app

RUN python3 -m venv venv-app \
    && source venv-app/bin/activate \
    && pip --version \
    && pip install --no-cache-dir --requirement requirements.freeze.txt

COPY . /app

CMD ["uwsgi", "--yaml", "uwsgi.yml"]

EXPOSE 80
