FROM certbot/cerbot

ADD . /alidns

RUN pip install -r /alidns/requirements.txt

VOLUME /etc/alidns