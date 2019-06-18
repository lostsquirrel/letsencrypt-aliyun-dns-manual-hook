FROM certbot/certbot

ADD . /alidns

RUN apk add --no-cache --virtual .build-deps \
    build-base \
    && pip install -r /alidns/requirements.txt \
    && apk del .build-deps

VOLUME /etc/alidns