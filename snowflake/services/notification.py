from datetime import datetime

from snowflake.models.notification import Notification


def notify_appreciation(appreciation):
    for mention in appreciation.mentions:
        notification = Notification(created_at=datetime.now(), user=mention.user, type="appreciation",
                                    object_id=str(appreciation.id))
        Notification.create(notification)

