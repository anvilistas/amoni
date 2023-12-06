# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
FROM python:3.11-alpine as builder
COPY docker/app_server/requirements.txt .
RUN apk update \
&&  apk add --no-cache build-base linux-headers gcc python3-dev \
&&  python -m venv /opt/venv \
&&  /opt/venv/bin/pip install --upgrade pip \
&&  /opt/venv/bin/pip install --no-cache-dir psutil \
&&  /opt/venv/bin/pip install --extra-index-url=https://www.piwheels.org/simple -r requirements.txt \
&&  /opt/venv/bin/anvil-app-server || true

FROM python:3.11-alpine
ENV PATH="/opt/venv/bin:$PATH"
RUN apk update \
&&  apk add --no-cache postgresql-client openjdk8 \
&&  adduser -D anvil \
&&  mkdir /anvil-data \
&&  chown -R anvil:anvil /anvil-data
COPY --from=builder /opt/venv /opt/venv
