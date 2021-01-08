from datetime import datetime

from snowflake.models import Appreciation, Comment
from snowflake.models.notification import Notification, TYPE_COMMENT, TYPE_APPRECIATION


def notify_appreciation(appreciation: Appreciation):
    for mention in appreciation.mentions:
        notification = Notification(created_at=datetime.now(), user=mention.user, type=TYPE_APPRECIATION,
                                    object_id=str(appreciation.id))
        Notification.create(notification)


def notify_comment(c: Comment):
    notification = Notification(created_at=datetime.now(), user=c.user, type=TYPE_COMMENT,
                                object_id=str(c.id))
    Notification.create(notification)
