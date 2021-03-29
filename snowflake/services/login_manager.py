from flask import Request, abort, g, request, flash, redirect, Flask
from flask_login import LoginManager, user_loaded_from_header, login_url

from . import token_manager
from ..controllers.api.response import bad_request, unauthorized
from ..models import User

login_manager = LoginManager()
login_manager.login_view = "login.login"
login_manager.login_message_category = "danger"
login_manager.needs_refresh_message_category = "danger"


@login_manager.request_loader
def load_user_from_header(incoming_request: Request):
    authorization_value = incoming_request.headers.get('Authorization')
    if not authorization_value:
        return None

    parts = authorization_value.split(' ', 1)

    if len(parts) != 2:
        abort(400, bad_request('Malformed authorization'))

    scheme, token = parts

    if scheme != 'Bearer':
        return None

    return token_manager.load_user(token)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    if request.path.startswith("/api"):
        return unauthorized()

    flash(login_manager.login_message, category='danger')
    return redirect(login_url(login_manager.login_view, request.url))


@user_loaded_from_header.connect
def on_user_loaded_from_header(*_):
    g.login_via_header = True


def init_app(app: Flask):
    login_manager.init_app(app)
