from datetime import datetime
from unittest.mock import patch

from snowflake.models import User, OneOnOneActionItem, OneOnOne
from snowflake.schemas.one_on_one import OneOnOneActionItemSchema, \
    CreateOrEditOneOnOneActionItemSchema, \
    OneOnOneSchema, GetOneOnOneSchema, CreateOneOnOneSchema

time = datetime.now()
user = User(id='12345', name='Hello', designation='Developer',
            team_name='Engineering', username='hello',
            email='hello@example.com',
            created_at=time,
            profile_pic='https://example.com/picture.jpg')

one_on_one = OneOnOne(
    id=1,
    created_by=user,
    created_at=time,
    user=user,
)

one_on_one.action_items = [
    OneOnOneActionItem(id=1, content="hello", created_by=user, one_on_one=one_on_one, state=True),
    OneOnOneActionItem(id=2, content="world", created_by=user, one_on_one=one_on_one, state=False),
]


def test_one_on_one_action_item_schema():
    action_item = one_on_one.action_items[0]

    schema = OneOnOneActionItemSchema()

    expected = {
        'content': 'hello',
        'createdBy': {
            'designation': 'Developer',
            'email': 'hello@example.com',
            'name': 'Hello',
            'profilePic': 'https://example.com/picture.jpg',
            'teamName': 'Engineering',
            'username': 'hello',
            'createdAt': time.isoformat(),
        },
        'id': 1,
        'state': True
    }

    assert schema.dump(action_item) == expected


def test_create_or_edit_one_on_one_action_item_schema():
    json = {"state": False, "content": "Hello World"}
    schema = CreateOrEditOneOnOneActionItemSchema()

    action_item = schema.load(json)

    assert not action_item.state
    assert action_item.content == "Hello World"


def test_one_on_one_schema():
    schema = OneOnOneSchema()

    expected = {
        'createdAt': time.isoformat(),
        'createdBy': {
            'createdAt': time.isoformat(),
            'designation': 'Developer',
            'email': 'hello@example.com',
            'name': 'Hello',
            'profilePic': 'https://example.com/picture.jpg',
            'teamName': 'Engineering',
            'username': 'hello'
        },
        'id': 1,
        'user': {
            'createdAt': time.isoformat(),
            'designation': 'Developer',
            'email': 'hello@example.com',
            'name': 'Hello',
            'profilePic': 'https://example.com/picture.jpg',
            'teamName': 'Engineering',
            'username': 'hello'
        }
    }
    assert schema.dump(one_on_one) == expected


def test_get_one_on_one_schema():
    schema = GetOneOnOneSchema()

    expected = {
        'actionItems': [
            {
                'content': 'hello',
                'createdBy': {
                    'createdAt': time.isoformat(),
                    'designation': 'Developer',
                    'email': 'hello@example.com',
                    'name': 'Hello',
                    'profilePic': 'https://example.com/picture.jpg',
                    'teamName': 'Engineering',
                    'username': 'hello'
                },
                'id': 1,
                'state': True},
            {
                'content': 'world',
                'createdBy': {
                    'createdAt': time.isoformat(),
                    'designation': 'Developer',
                    'email': 'hello@example.com',
                    'name': 'Hello',
                    'profilePic': 'https://example.com/picture.jpg',
                    'teamName': 'Engineering',
                    'username': 'hello'
                },
                'id': 2,
                'state': False
            }
        ],
        'createdAt': time.isoformat(),
        'createdBy': {
            'designation': 'Developer',
            'email': 'hello@example.com',
            'name': 'Hello',
            'profilePic': 'https://example.com/picture.jpg',
            'teamName': 'Engineering',
            'username': 'hello',
            'createdAt': time.isoformat(),
        },
        'id': 1,
        'user': {
            'createdAt': time.isoformat(),
            'designation': 'Developer',
            'email': 'hello@example.com',
            'name': 'Hello',
            'profilePic': 'https://example.com/picture.jpg',
            'teamName': 'Engineering',
            'username': 'hello'
        }
    }

    assert schema.dump(one_on_one) == expected


@patch('snowflake.schemas.fields.User.get_by_username')
def test_create_one_on_one_schema(mock_user_get):
    mock_user_get.return_value = user

    schema = CreateOneOnOneSchema()
    json = {"user": "hello"}

    assert schema.load(json).user == user
