from flask import Blueprint, render_template
from flask_login import current_user

from snowflake.models import User, Appreciation, Mention

blueprint = Blueprint('profile', __name__)


@blueprint.route('/', defaults={'username': None})
@blueprint.route('/<username>')
def profile(username):
    user = current_user if username is None else User.get_by_username(username)

    appreciations_given = Appreciation.count_by_user(user)
    appreciations_received = Mention.count_by_user(user)

    return render_template('profile.html', user=user, appreciations_given=appreciations_given,
                           appreciations_received=appreciations_received)
