FROM python:3.8-slim AS base

RUN set -ex \
    && apt-get update && apt-get upgrade -y \
    && apt-get install -y build-essential pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl python3-dev vim \
    && apt-get install gcc musl-dev postgresql-server-dev-11 -y
RUN pip install poetry --no-cache-dir

# Create a group and user to run our app
ARG APP_USER=wellread_user
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

FROM base AS build

WORKDIR /wellread/

# Production build stage
FROM build AS production-build

COPY . /wellread/
RUN poetry install --no-dev --no-interaction --no-ansi

# Post install cleanup
RUN rm -r wellread.egg-info
RUN rm pyproject.toml
RUN rm poetry.lock

EXPOSE 8000

USER ${APP_USER}:${APP_USER}

# ENTRYPOINT ["uvicorn wellread.app:app --host 0.0.0.0 --port 8000"]