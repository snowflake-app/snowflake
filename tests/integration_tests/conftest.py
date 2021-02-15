import pytest


@pytest.fixture
def client(flask_app):
    with flask_app.test_client() as flask_client:
        yield flask_client
