from flask_login import current_user

from snowflake.models import OneOnOne, User


def can_view_one_on_one(one_on_one: OneOnOne, user: User = current_user):
    return user.id == one_on_one.user_id or user.id == one_on_one.created_by_id


def can_delete_one_on_one(one_on_one: OneOnOne, user: User = current_user):
    return can_view_one_on_one(one_on_one, user)
