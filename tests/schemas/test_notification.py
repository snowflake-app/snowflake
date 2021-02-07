from datetime import datetime

import pytest

from snowflake import app as flask_app
from snowflake.models import User, Notification
from snowflake.models.notification import TYPE_APPRECIATION
from snowflake.schemas.notification import NotificationSchema


@pytest.fixture(scope="module", autouse=True)
def app():
    yield flask_app


def test_notification_schema_dumps_json_correctly():
    created_at = datetime.now()
    user = User(id='12345', name='Hello', designation='Developer',
                team_name='Engineering', username='hello',
                email='hello@example.com',
                profile_pic='https://example.com/picture.jpg')
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
    }

    assert schema.dump(notification) == expected
