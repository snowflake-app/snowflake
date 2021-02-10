from datetime import datetime

from snowflake.models import User
from snowflake.schemas.user import UserSchema


def test_user_schema_dumps_json_correctly():
    time = datetime.now()
    user = User(id='12345', name='Hello', designation='Developer',
                team_name='Engineering', username='hello',
                email='hello@example.com',
                created_at=time,
                profile_pic='https://example.com/picture.jpg')

    schema = UserSchema()

    expected = {
        'name': 'Hello',
        'designation': 'Developer',
        'teamName': 'Engineering',
        'username': 'hello',
        'email': 'hello@example.com',
        'profilePic': 'https://example.com/picture.jpg',
        'createdAt': time.isoformat()
    }

    assert expected == schema.dump(user)
