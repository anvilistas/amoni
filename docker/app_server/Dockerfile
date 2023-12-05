# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
FROM python:3.11-slim-bookworm
COPY docker/app_server/requirements.txt ./ 
RUN apt-get -yyy update && apt-get -yyy install gcc python3-dev software-properties-common postgresql-client openjdk-17-jdk \
&&  pip install --upgrade pip \
&&  mkdir /anvil-data \
&&  useradd anvil \
&&  chown -R anvil:anvil /anvil-data
RUN pip install --extra-index-url=https://www.piwheels.org/simple -r requirements.txt \
&&  anvil-app-server || true
