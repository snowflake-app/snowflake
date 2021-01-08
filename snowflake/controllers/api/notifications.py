from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from snowflake.controllers.api.response import not_found
from snowflake.db import db
from snowflake.models import User
from snowflake.models.notification import Notification

blueprint = Blueprint('api.notifications', __name__)


def user_to_json(user: User):
    return {
        'id': user.id,
        'username': user.username,
        'name': user.name
    }


def to_json(n):
    return {
        'id': n.id,
        'created_at': n.created_at,
        'user': user_to_json(n.user),
        'type': n.type,
        'object_id': n.object_id,
        'read': n.read
    }


@login_required
@blueprint.route('/_count')
def notification_count():
    return jsonify(Notification.count_unread_by_user(current_user))


@login_required
@blueprint.route('/<_id>/mark_as_read', methods=['POST'])
def mark_as_read(_id):
    notification = Notification.get(_id)
    if not notification:
        return not_found()

    notification.read = True
    db.session.add(notification)
    db.session.commit()

    return to_json(notification)


@login_required
@blueprint.route('')
def notification():
    return jsonify([to_json(n) for n in Notification.get_by_user(current_user)])
