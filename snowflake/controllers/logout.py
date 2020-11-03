from flask import Blueprint, redirect, url_for
from flask_login import login_required, logout_user

blueprint = Blueprint('logout', __name__)


@blueprint.route("/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index.index"))
