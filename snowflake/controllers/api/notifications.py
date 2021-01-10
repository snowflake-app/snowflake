from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from .response import not_found
from ...db import db
from ...models import Notification
from ...schemas.notification import NotificationSchema

blueprint = Blueprint('api.notifications', __name__)

schema = NotificationSchema()


@login_required
@blueprint.route('/_count')
def notification_count():
    return jsonify(Notification.count_unread_by_user(current_user))


@login_required
@blueprint.route('/<_id>/mark_as_read', methods=['POST'])
def mark_as_read(_id):
    n = Notification.get(_id)
    if not n:
        return not_found()

    n.read = True
    db.session.add(n)
    db.session.commit()

    return schema.jsonify(n)


@login_required
@blueprint.route('')
def notification():
    return schema.jsonify(Notification.get_by_user(current_user), many=True)
