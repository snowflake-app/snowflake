from datetime import datetime
from typing import Dict

from flask_login import current_user

from ..db import transaction
from ..models.notification import *


def notify_appreciation(appreciation: Appreciation):
    with transaction():
        for mention in appreciation.mentions:
            if mention.user.id != current_user.id:
                db.session.add(Notification(created_at=datetime.now(), user=mention.user, type=TYPE_APPRECIATION,
                                            object_id=str(appreciation.id)))


def notify_comment(c: Comment):
    now = datetime.now()

    users_to_notify: Dict[str, str] = {
        c.appreciation.created_by_id: TYPE_COMMENT_ON_APPRECIATION_GIVEN
    }

    for mention in c.appreciation.mentions:
        user_id = mention.user_id

        if user_id not in users_to_notify:
            users_to_notify[user_id] = TYPE_COMMENT_ON_APPRECIATION_RECEIVED

    for comment in c.appreciation.comments:
        user_id = comment.user_id

        if user_id not in users_to_notify:
            users_to_notify[user_id] = TYPE_COMMENT_ON_APPRECIATION_COMMENTED

    with transaction():
        for user_id, notification_type in users_to_notify.items():
            if user_id != current_user.id:
                db.session.add(Notification(created_at=now, user_id=user_id, type=notification_type,
                                            object_id=str(c.id)))
