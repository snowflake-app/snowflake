from flask import Blueprint, request
from flask_login import login_required

from .response import bad_request, not_found
from ...models import User
from ...schemas.user import UserSchema

blueprint = Blueprint('users', __name__)

schema = UserSchema()


@blueprint.route('/_autocomplete')
@login_required
def autocomplete():
    term = request.args.get('q')

    if term is None:
        return bad_request("missing search term 'q'")

    users = User.find_by_name_prefix(term)

    return schema.jsonify(users, many=True)


@blueprint.route('/<username>')
@login_required
def get_user_by_id(username):
    user = User.get_by_username(username)

    if not user:
        return not_found()

    return schema.jsonify(user)
