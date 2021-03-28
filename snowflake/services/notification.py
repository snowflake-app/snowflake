from datetime import datetime
from typing import Dict

from flask_login import current_user

from .. import db
from ..models import OneOnOneActionItem, Appreciation, Notification, Comment, OneOnOne
from ..models.notification import TYPE_COMMENT_ON_APPRECIATION_GIVEN, \
    TYPE_COMMENT_ON_APPRECIATION_RECEIVED, \
    TYPE_COMMENT_ON_APPRECIATION_COMMENTED, TYPE_ONE_ON_ONE_SETUP, \
    TYPE_ONE_ON_ONE_ACTION_ITEM_ADDED, TYPE_APPRECIATION


def notify_appreciation(appreciation: Appreciation):
    with db.transaction():
        for mention in appreciation.mentions:
            if mention.user.id != current_user.id:
                db.persist(Notification(created_at=datetime.now(), user=mention.user,
                                        type=TYPE_APPRECIATION,
                                        object_id=str(appreciation.id)))


def notify_comment(comment: Comment):
    now = datetime.now()

    users_to_notify: Dict[str, str] = {
        comment.appreciation.created_by_id: TYPE_COMMENT_ON_APPRECIATION_GIVEN
    }

    for mention in comment.appreciation.mentions:
        user_id = mention.user_id

        if user_id not in users_to_notify:
            users_to_notify[user_id] = TYPE_COMMENT_ON_APPRECIATION_RECEIVED

    for existing_comment in comment.appreciation.comments:
        user_id = existing_comment.user_id

        if user_id not in users_to_notify:
            users_to_notify[user_id] = TYPE_COMMENT_ON_APPRECIATION_COMMENTED

    with db.transaction():
        for user_id, notification_type in users_to_notify.items():
            if user_id != current_user.id:
                db.persist(Notification(created_at=now, user_id=user_id, type=notification_type,
                                        object_id=str(comment.id)))


def notify_one_on_one_setup(one_on_one: OneOnOne):
    with db.transaction():
        db.persist(Notification(created_at=datetime.now(),
                                user_id=one_on_one.user_id,
                                type=TYPE_ONE_ON_ONE_SETUP,
                                object_id=str(one_on_one.id)))


def notify_one_on_one_action_item_added(action_item: OneOnOneActionItem):
    with db.transaction():
        user_id = action_item.one_on_one.user_id \
            if action_item.one_on_one.created_by_id == current_user.id else \
            action_item.one_on_one.created_by_id

        db.persist(Notification(created_at=datetime.now(),
                                user_id=user_id,
                                type=TYPE_ONE_ON_ONE_ACTION_ITEM_ADDED,
                                object_id=str(action_item.one_on_one.id)))
