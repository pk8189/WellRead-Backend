FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN set -ex \
    && apt-get update && apt-get upgrade -y \
    && apt-get install -y build-essential pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl python3-dev vim \
    && apt-get install gcc musl-dev postgresql-server-dev-11 -y
# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /wellread/

COPY ./app /wellread/app/
COPY ./pyproject.toml ./poetry.lock* /wellread/

RUN poetry install --no-dev --no-interaction --no-ansi --no-root
