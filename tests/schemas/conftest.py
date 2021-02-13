import pytest

from snowflake import app as flask_app


@pytest.fixture(scope="module", autouse=True)
def app():
    yield flask_app
