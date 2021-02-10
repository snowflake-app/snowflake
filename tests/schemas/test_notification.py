from datetime import datetime
from unittest.mock import patch

from snowflake import app
from snowflake.models import User, Notification, Appreciation
from snowflake.models.notification import TYPE_APPRECIATION
from snowflake.schemas.notification import NotificationSchema


def test_notification_schema_dumps_json_correctly():
    created_at = datetime.now()
    user = User(id='12345', name='Hello', designation='Developer',
                team_name='Engineering', username='hello',
                email='hello@example.com',
                created_at=created_at,
                profile_pic='https://example.com/picture.jpg')
    appreciation = Appreciation(content="blah", id=1, created_at=created_at, created_by=user)
    with app.app_context():
        with patch('snowflake.models.notification.Appreciation.get') as get_func:
            get_func.return_value = appreciation

            notification = Notification(
                id=1,
                created_at=created_at,
                user=user,
                type=TYPE_APPRECIATION,
                object_id='1',
                read=False,
            )

            schema = NotificationSchema()

            expected = {
                'id': 1,
                'createdAt': created_at.isoformat(),
                'type': TYPE_APPRECIATION,
                'objectId': '1',
                'read': False,
                'object': {
                    'id': '1',
                    'created_at': created_at.isoformat(),
                    'created_by': {
                        'createdAt': created_at.isoformat(),
                        'designation': 'Developer',
                        'email': 'hello@example.com',
                        'name': 'Hello',
                        'profilePic': 'https://example.com/picture.jpg',
                        'teamName': 'Engineering',
                        'username': 'hello'
                    }
                },
            }

            actual = schema.dump(notification)
            assert actual == expected
