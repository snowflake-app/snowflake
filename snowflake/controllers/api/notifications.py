from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from .request import requires_json
from .response import not_found
from ...db import db
from ...models import Notification
from ...schemas.notification import NotificationSchema, UpdateNotificationSchema

blueprint = Blueprint('api.notifications', __name__)

schema = NotificationSchema()
update_notification_schema = UpdateNotificationSchema()


@blueprint.route('/_count')
@login_required
def notification_count():
    return jsonify(Notification.count_unread_by_user(current_user))


@blueprint.route('/<_id>', methods=['PATCH'])
@login_required
@requires_json
def update_notification(_id):
    notification = Notification.get(_id)
    if not notification:
        return not_found()

    req_body = update_notification_schema.load(request.json)

    notification.read = req_body['read']

    db.session.add(notification)
    db.session.commit()

    return schema.jsonify(notification)


@blueprint.route('/', methods=['GET'])
@login_required
def get_all_notifications():
    return schema.jsonify(Notification.get_by_user(current_user), many=True)
