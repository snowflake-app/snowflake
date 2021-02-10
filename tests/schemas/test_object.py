from datetime import datetime

from snowflake.models import Appreciation, User
from snowflake.schemas.object import ObjectSchema


def test_object_schema_should_return_integer_ids_as_string():
    created_at = datetime.now()
    user = User(id='12345', name='Hello', designation='Developer',
                team_name='Engineering', username='hello',
                email='hello@example.com',
                created_at=created_at,
                profile_pic='https://example.com/picture.jpg')
    obj = Appreciation(id=1, content="blah", created_at=created_at, created_by=user)

    expected = {
        'created_at': created_at.isoformat(),
        'created_by': {
            'createdAt': created_at.isoformat(),
            'designation': 'Developer',
            'email': 'hello@example.com',
            'name': 'Hello',
            'profilePic': 'https://example.com/picture.jpg',
            'teamName': 'Engineering',
            'username': 'hello'
        },
        'id': '1'
    }

    schema = ObjectSchema()

    assert schema.dump(obj) == expected
