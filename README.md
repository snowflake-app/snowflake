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
5. Run migrations using `flask db upgrade`
6. Configure included MinIO with `minio/stable/mc` (`brew install minio/stable/mc`)
   ```shell
   mc alias set local http://localhost:9000 root snowflake
   mc mb local/user-content
   mc policy set-json scripts/minio-policy.json local/user-content
   ```
7. Start asset pipeline with `npm start` and leave it running.
8. Start the application with `flask run`
9. Run tests with `make`
