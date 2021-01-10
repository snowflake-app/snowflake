from flask import Blueprint, request

from .response import bad_request
from ...models import User
from ...schemas.user import UserSchema

blueprint = Blueprint('users', __name__)

schema = UserSchema()


@blueprint.route('/_autocomplete')
def autocomplete():
    term = request.args.get('q')

    if term is None:
        return bad_request("missing search term 'q'")

    users = User.find_by_name_prefix(term)

    return schema.jsonify(users, many=True)
