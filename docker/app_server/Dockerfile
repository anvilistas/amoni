# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
#
# __version__ = "0.0.12"
FROM python:3

RUN apt-get -yyy update \
&&  apt-get -yyy install software-properties-common postgresql-client \
&&  wget -O- https://apt.corretto.aws/corretto.key | apt-key add - \
&&  add-apt-repository 'deb https://apt.corretto.aws stable main' \
&&  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
&&  dpkg -i google-chrome-stable_current_amd64.deb || apt install -y --fix-broken \
&&  rm google-chrome-stable_current_amd64.deb \
&&  apt-get -yyy update \
&&  apt-get -yyy install java-1.8.0-amazon-corretto-jdk ghostscript \
&&  pip install anvil-app-server \
&&  anvil-app-server || true \
&&  mkdir /anvil_data \
&&  useradd anvil \
&&  chown -R anvil:anvil /anvil_data
