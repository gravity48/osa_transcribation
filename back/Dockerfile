FROM python:3.8-slim-buster
ENV \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

# System deps:
RUN apt-get update && \
  apt-get install --no-install-recommends -y \
  build-essential \
  gettext \
  libpq-dev \
  wget
  # Cleaning cache:
RUN apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt


COPY ./src /app

RUN mkdir -p /app/media /app/static && \
	chmod +x /app/media/ /app/static/ \
