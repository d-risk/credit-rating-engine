FROM alpine:3.11.3

RUN apk add --no-cache --update \
        python3 \
        uwsgi \
    	uwsgi-python3

ARG user=app
ARG workdir=/${user}
ARG requirements=requirements.freeze.txt
ARG venv=.venv

RUN addgroup -S ${user} && adduser -G ${user} -h ${workdir} -S ${user}

USER ${user}
WORKDIR ${workdir}

# only copy the requirements.freeze.txt file so that the
# next run command to install python packages is not executed unless
# the requirements.freeze.txt file changes
COPY --chown=app:app ${requirements} ${workdir}

RUN python3 -m venv ${venv} \
    && source ${venv}/bin/activate \
    && python -m pip install --upgrade pip setuptools \
    && pip install --no-cache-dir --requirement ${requirements}

COPY --chown=app:app . ${workdir}

ENV APP_PRODUCTION "false"

CMD ["uwsgi", "--yaml", "uwsgi.yaml"]

EXPOSE 8080
