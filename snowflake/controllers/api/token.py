from flask import Blueprint, request
from flask_login import login_required, current_user

from .response import forbidden
from ...models import User
from ...schemas.login import LoginSchema, LoginResponseSchema
from ...services import google_auth, token_manager

blueprint = Blueprint('api.token', __name__)

login_schema = LoginSchema()
login_response_schema = LoginResponseSchema()


@blueprint.route('', methods=['POST'])
def login():
    login_request = login_schema.load(request.json)
    user_info = google_auth.get_user_info(login_request['token'])

    user = User.get(user_info.id)

    if not user:
        return forbidden()

    token = token_manager.create(user)

    return login_response_schema.jsonify({
        'token': token,
        'user': user
    })


@blueprint.route('/introspect', methods=['GET'])
@login_required
def introspect():
    _, token = request.headers.get('Authorization').split(' ', 1)
    return login_response_schema.jsonify({
        'token': token,
        'user': current_user
    })
