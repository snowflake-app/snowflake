# snowflake

Snowflake

## Building

### Requirements

1. Python 3.7+
2. Pipenv
2. NodeJS
3. Docker and docker-compose

### Steps

1. Copy `.env.example` to `.env` and supply the values as instructed.
2. Using the included `docker-compose.yml` use `docker-compose up` to start a database instance for development and
   leave it running.
3. Active a Pipenv shell using `pipenv shell`
4. Install dependencies `pipenv install && npm install`
5. Run migrations using `python migration.py`
6. Start asset pipeline with `npm start` and leave it running.
7. Start the application with `flask run`
8. Run tests with `make`
