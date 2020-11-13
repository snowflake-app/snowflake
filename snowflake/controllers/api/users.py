from flask import Blueprint, request, jsonify

from snowflake.models import User
from .response import bad_request

blueprint = Blueprint('users', __name__)


@blueprint.route('/_autocomplete')
def autocomplete_search():
    term = request.args.get('q')

    if term is None:
        return bad_request("missing search term 'q'")

    users = User.find_by_name_prefix(term)

    return jsonify([{
        'name': user.name,
        'username': user.username,
        'avatar': user.profile_pic
    } for user in users])
