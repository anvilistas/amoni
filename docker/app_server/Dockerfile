# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
#
# __version__ = "0.0.2"
FROM python:3

RUN apt-get -yyy update && apt-get -yyy install \
    software-properties-common \
    postgresql-client \
&&  wget -O- https://apt.corretto.aws/corretto.key | apt-key add - && \
    add-apt-repository 'deb https://apt.corretto.aws stable main'

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    (dpkg -i google-chrome-stable_current_amd64.deb || apt install -y --fix-broken) && \
    rm google-chrome-stable_current_amd64.deb

RUN apt-get -yyy update && apt-get -yyy install java-1.8.0-amazon-corretto-jdk ghostscript

RUN pip install anvil-app-server
RUN anvil-app-server || true

RUN mkdir /anvil_data && useradd anvil && chown -R anvil:anvil /anvil_data
USER anvil
