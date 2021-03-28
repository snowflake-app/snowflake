from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from snowflake import db
from snowflake.controllers.api.response import not_found
from snowflake.models.notification import Notification, TYPE_APPRECIATION, \
    TYPE_COMMENT_ON_APPRECIATION_RECEIVED, TYPE_COMMENT_ON_APPRECIATION_GIVEN, \
    TYPE_ONE_ON_ONE_SETUP, TYPE_ONE_ON_ONE_ACTION_ITEM_ADDED

blueprint = Blueprint('notifications', __name__)


def build_redirect(notification: Notification):
    if notification.type == TYPE_APPRECIATION:
        return url_for('index.index') + f"#appreciation-{notification.object_id}"

    if notification.type in [TYPE_COMMENT_ON_APPRECIATION_RECEIVED,
                             TYPE_COMMENT_ON_APPRECIATION_GIVEN]:
        return url_for('index.index') + f"#appreciation-{notification.object.appreciation.id}"

    if notification.type in [TYPE_ONE_ON_ONE_SETUP, TYPE_ONE_ON_ONE_ACTION_ITEM_ADDED]:
        return url_for('one_on_one.one_on_one', _id=notification.object.id)

    raise ValueError("Unknown notification type: " + notification.typel)


@login_required
@blueprint.route('/<_id>/open', methods=['GET'])
def open_notification(_id):
    notification = Notification.get(_id)
    if not notification:
        return not_found()

    notification.read = True

    with db.transaction():
        db.persist(notification)

    return redirect(build_redirect(notification))


@login_required
@blueprint.route('')
def notifications():
    return render_template('notifications.html',
                           notifications=Notification.get_by_user(current_user))
