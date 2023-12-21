FROM python:3.10-bullseye

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

copy . /code/app

CMD ["python", "/code/app/main.py"]