FROM python:3

WORKDIR /app

RUN pip install pipenv
COPY Pipfile* /app/
RUN pipenv install --system

COPY . /app

CMD gunicorn --bind 0.0.0.0:5000 wsgi:app
