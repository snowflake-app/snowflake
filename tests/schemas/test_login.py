from datetime import datetime

from snowflake.models import User
from snowflake.schemas.login import LoginSchema, LoginResponseSchema


def test_login_schema_reads_correct_json():
    schema = LoginSchema()

    json = r'{ "token": "12345" }'

    login = schema.loads(json)

    expected = {"token": "12345"}

    assert login == expected


def test_login_response_schema_dumps_correct_json():
    time = datetime.now()
    schema = LoginResponseSchema()
    user = User(id='12345', name='Hello', designation='Developer',
                team_name='Engineering', username='hello',
                email='hello@example.com',
                created_at=time,
                profile_pic='https://example.com/picture.jpg')

    login = schema.dump({
        'token': '12345',
        'expiry': time,
        'refresh_token': '12345',
        'user': user
    })

    expected = {
        "token": "12345",
        "refreshToken": "12345",
        "expiry": time.isoformat(),
        "user": {
            'name': 'Hello',
            'designation': 'Developer',
            'teamName': 'Engineering',
            'username': 'hello',
            'email': 'hello@example.com',
            'profilePic': 'https://example.com/picture.jpg',
            'createdAt': time.isoformat()
        }
    }

    assert login == expected
