FROM python:3

COPY docker/test_runner/requirements.txt ./
RUN pip install -r requirements.txt
RUN anvil-app-server || true

RUN mkdir /code
COPY docker/test_runner/pyproject.toml /code
WORKDIR /code
