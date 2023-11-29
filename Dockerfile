# syntax=docker/dockerfile:1

FROM ghcr.io/linuxserver/baseimage-ubuntu:jammy

# set version label
ARG BUILD_DATE
ARG VERSION
ARG WHISPER_VERSION
LABEL build_version="Linuxserver.io version:- ${VERSION} Build-date:- ${BUILD_DATE}"
LABEL maintainer="thespad"

ARG DEBIAN_FRONTEND=noninteractive

RUN \
  apt-get update && \
  apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-venv && \
  if [ -z ${WHISPER_VERSION+x} ]; then \
    WHISPER_VERSION=$(curl -sL  https://pypi.python.org/pypi/wyoming-faster-whisper/json |jq -r '. | .info.version'); \
  fi && \
  python3 -m venv /lsiopy && \
  pip install -U --no-cache-dir \
    pip \
    wheel && \
  pip install -U --no-cache-dir --find-links https://wheel-index.linuxserver.io/ubuntu/ \
    "wyoming-faster-whisper==${WHISPER_VERSION}" && \
  apt-get purge -y --auto-remove \
    build-essential \
    python3-dev && \
  rm -rf \
    /var/lib/apt/lists/* \
    /tmp/*

COPY root/ /

VOLUME /config

EXPOSE 10300
