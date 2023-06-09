FROM ubuntu:22.04

ENV \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \

  #tzdata
  DEBIAN_FRONTEND=noninteractive\
  TZ=Europe/Moscow

RUN apt-get update && apt-get install --no-install-recommends -y  \
    software-properties-common \
    gnupg

RUN add-apt-repository ppa:deadsnakes/ppa -y
# Install Python-devs:
RUN apt-get update && \
  apt-get install --no-install-recommends -y \
  build-essential \
  python3.8 \
  python3.8-dev \
  python3.8-venv \
  python3.8-distutils \
  python3-pip \
  gettext

RUN python3.8 -m venv /venv
ENV PATH=/venv/bin:$PATH

#Install c++ devs
RUN apt-get install --no-install-recommends -y \
  libpq-dev \
  wget \
  cmake \
  openssl\
  libssl-dev \
  g++ \
  ffmpeg
  # Cleaning cache:
RUN apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app/src/replica_decoder

RUN  cmake . && cmake -S . -B build  && cmake --build .


WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt


WORKDIR /app/src

CMD python main.py