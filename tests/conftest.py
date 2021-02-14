import os

import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from snowflake.app import create_app
from snowflake.migrations import migrate


@pytest.fixture(scope="session", autouse=True)
def app():
    with PostgresContainer('postgres:13') as postgres, RedisContainer('redis:6') as redis:
        redis_url = f'redis://{redis.get_container_host_ip()}:{redis.get_exposed_port(6379)}/0'
        os.environ['DATABASE_URI'] = postgres.get_connection_url()
        os.environ['REDIS_URI'] = redis_url

        migrate()
        flask_app = create_app()
        flask_app.config['TESTING'] = True
        yield flask_app
