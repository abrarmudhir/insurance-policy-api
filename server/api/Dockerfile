ARG IMAGE_VARIANT=slim-buster
ARG PYTHON_VERSION=3.11.0

FROM python:${PYTHON_VERSION}-${IMAGE_VARIANT} AS dependencies

ARG PROJECT_DIR=.
ARG POETRY_VERSION=1.8.3

RUN useradd --create-home api

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=${POETRY_VERSION}

RUN pip install --upgrade pip

COPY ${PROJECT_DIR}/server/api/install-poetry.py .
RUN python ./install-poetry.py
ENV PATH="$POETRY_HOME/bin:$PATH"

COPY ${PROJECT_DIR}/pyproject.toml ${PROJECT_DIR}/poetry.lock ./

RUN poetry install --no-root --no-cache --no-ansi


COPY ${PROJECT_DIR}/app ./app

RUN poetry install --only main

EXPOSE 8050

CMD ["uvicorn", "app.main:api", "--host", "0.0.0.0", "--port", "8050", "--proxy-headers", "--forwarded-allow-ips", "*", "--log-level", "debug"]
