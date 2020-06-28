# build frontend
FROM node:lts-buster-slim AS frontend-builder

ARG DEBIAN_FRONTEND="noninteractive"
RUN apt-get -y update \
	&& apt-get -y install --no-install-recommends ca-certificates git \
	&& npm install -g @quasar/cli

ARG PCR_FRONTEND_GIT_URL="https://github.com/CJowo/pcr-guild-vue.git"
WORKDIR /srv/pcr/frontend
RUN git clone "$PCR_FRONTEND_GIT_URL" \
	&& cd pcr-guild-vue \
	&& npm install \
	&& quasar build

# backend
FROM python:3-slim-buster

ARG DEBIAN_FRONTEND="noninteractive"
RUN apt-get -y update \
	&& apt-get -y install sqlite3 \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /srv/pcr
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt \
	&& pip3 install gunicorn \
	&& rm /tmp/requirements.txt

COPY . .
COPY --from=frontend-builder /srv/pcr/frontend/pcr-guild-vue/dist/spa vue
RUN mkdir -p data
ENV PCR_DEBUG="0"
ENV PCR_SQLITE3_PATH="/srv/pcr/data/pcr.db"

COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/*
EXPOSE 80
VOLUME [ "/srv/pcr/data" ]
ENTRYPOINT [ "entrypoint.sh" ]

