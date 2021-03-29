FROM node:15 as static

WORKDIR /app

COPY package*.json /app/
RUN npm install

COPY .babelrc /app/
COPY webpack.config.js/ /app/
COPY _frontend/ /app/_frontend


RUN mkdir -p snowflake/static/assets && npm run build

FROM python:3.9

WORKDIR /app

EXPOSE 5000

RUN pip install pipenv
COPY Pipfile* /app/
RUN pipenv install --system

COPY . /app
COPY --from=static /app/snowflake/static/assets /app/snowflake/static/assets

CMD gunicorn --bind 0.0.0.0:5000 snowflake.wsgi:app
