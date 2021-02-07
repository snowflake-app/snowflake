import pytest

from snowflake import app as flask_app
from snowflake.models import User
from snowflake.schemas.user import UserSchema


@pytest.fixture(scope="module", autouse=True)
def app():
    yield flask_app


def test_user_schema_dumps_json_correctly():
    user = User(id='12345', name='Hello', designation='Developer',
                team_name='Engineering', username='hello',
                email='hello@example.com',
                profile_pic='https://example.com/picture.jpg')

    schema = UserSchema()

    expected = {
        'name': 'Hello',
        'designation': 'Developer',
        'teamName': 'Engineering',
        'username': 'hello',
        'email': 'hello@example.com',
        'profilePic': 'https://example.com/picture.jpg'
    }

    assert expected == schema.dump(user)
