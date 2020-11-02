# snowflake

Snowflake

## Building

### Requirements

1. Python 3.7+
2. Pipenv
2. NodeJS
3. Docker and docker-compose

### Steps

1. Using the included `docker-compose.yml` use `docker-compose up` to start a
database instance for development and leave it running.
2. Active a Pipenv shell using `pipenv shell`
3. Install dependencies `pipenv install && npm install`
4. Run migrations using `python migration.py`
5. Start asset pipeline with `npm start` and leave it running.
6. Start the application with `python -m snowflake`
