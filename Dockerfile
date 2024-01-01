FROM python:3.10-bullseye


RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

copy . /code/app

USER 1001

CMD ["poetry","run", "python", "/code/app/main.py"]