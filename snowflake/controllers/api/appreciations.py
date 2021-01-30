import re
from datetime import datetime

from flask import Blueprint, request
from flask_login import login_required, current_user

from .response import bad_request, not_found, unauthorized
from ... import acl
from ...models import Appreciation, Like, User, Mention
from ...schemas.appreciation import AppreciationSchema, CreateAppreciationSchema
from ...services import notification

blueprint = Blueprint('api.appreciations', __name__)

appreciation_schema = AppreciationSchema()
create_appreciation_schema = CreateAppreciationSchema()


def get_appreciation_viewer_like(appreciation: Appreciation):
    return Like.get_by_appreciation_and_user(appreciation, current_user)


def appreciation_view(appreciation: Appreciation):
    return {
        'id': appreciation.id,
        'content': appreciation.content,
        'created_at': appreciation.created_at,
        'created_by': appreciation.created_by,
        'like_count': appreciation.like_count,
        'comment_count': appreciation.comment_count,
        'mentions': appreciation.mentions,

        'viewer_like': get_appreciation_viewer_like(appreciation),
    }


@login_required
@blueprint.route('', methods=['GET'])
def list_all_appreciations():
    if not acl.can_view_appreciations():
        return unauthorized()

    formatted_appreciations = [appreciation_view(a) for a in Appreciation.get_all()]
    return appreciation_schema.jsonify(formatted_appreciations, many=True)


@login_required
@blueprint.route('', methods=['PUT'])
def create_appreciation():
    if not request.is_json:
        return bad_request()

    if not acl.can_create_appreciations():
        return unauthorized()

    appreciation: Appreciation = create_appreciation_schema.load(request.json)

    appreciation.created_by = current_user
    appreciation.created_at = datetime.now()

    Appreciation.create(appreciation)

    mentions = re.findall(r'@[a-zA-Z0-9._]+', appreciation.content)

    for mention_text in mentions:
        user = User.get_by_username(mention_text[1:])
        if user is None:
            continue
        mention = Mention(user=user, appreciation=appreciation)
        Mention.create(mention)

    notification.notify_appreciation(appreciation)

    return appreciation_schema.jsonify(appreciation)


@login_required
@blueprint.route('/<_id>', methods=['GET'])
def get_appreciation(_id):
    appreciation = Appreciation.get(_id)

    if not appreciation:
        return not_found()

    if not acl.can_view_appreciation(appreciation):
        return unauthorized()

    return appreciation_schema.jsonify(appreciation)


@login_required
@blueprint.route('/<_id>', methods=['PATCH'])
def update_appreciation(_id):
    return not_found()


@login_required
@blueprint.route('/<_id>', methods=['DELETE'])
def delete_appreciation(_id):
    pass


@login_required
@blueprint.route('/<appreciation_id>/likes', methods=['GET'])
def get_appreciation_likes(appreciation_id):  # pylint: disable=unused-argument
    pass


@login_required
@blueprint.route('/<appreciation_id>/likes', methods=['PUT'])
def like(appreciation_id):  # pylint: disable=unused-argument
    pass


@login_required
@blueprint.route('/<appreciation_id>/likes/<like_id>', methods=['DELETE'])
def delete_like(appreciation_id, like_id):  # pylint: disable=unused-argument
    pass


@login_required
@blueprint.route('/<appreciation_id>/comments', methods=['GET'])
def get_comments(appreciation_id):  # pylint: disable=unused-argument
    pass


@login_required
@blueprint.route('/<appreciation_id>/comments', methods=['GET'])
def create_comment(appreciation_id):  # pylint: disable=unused-argument
    pass


@login_required
@blueprint.route('/<appreciation_id>/comments/<comment_id>', methods=['GET'])
def update_comment(appreciation_id, comment_id):  # pylint: disable=unused-argument
    pass


@login_required
@blueprint.route('/<appreciation_id>/comments/<comment_id>', methods=['GET'])
def delete_comment(appreciation_id, comment_id):  # pylint: disable=unused-argument
    pass
