# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
#
# __version__ = "0.0.13"
FROM python:3.11-slim-bookworm
COPY docker/app_server/requirements.txt ./ 

RUN apt-get -yyy update \
&&  apt-get -yyy install software-properties-common postgresql-client openjdk-17-jdk\
&&  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
&&  dpkg -i google-chrome-stable_current_amd64.deb || apt install -y --fix-broken \
&&  rm google-chrome-stable_current_amd64.deb \
&&  pip install -r requirements.txt \
&&  anvil-app-server || true \
&&  mkdir /anvil_data \
&&  useradd anvil \
&&  chown -R anvil:anvil /anvil_data
