# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
#
# __version__ = "0.0.1"
FROM python:3

COPY docker/test_runner/requirements.txt ./
RUN pip install -r requirements.txt
RUN anvil-app-server || true

RUN mkdir /code
COPY docker/test_runner/pyproject.toml /code
WORKDIR /code
