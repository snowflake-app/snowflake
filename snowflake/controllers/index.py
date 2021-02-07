from flask import Blueprint, render_template
from flask_login import login_required, current_user

from snowflake.forms import AppreciationForm, LikeForm, CommentForm
from snowflake.models import Appreciation, Mention

blueprint = Blueprint('index', __name__)


@blueprint.route("/")
@login_required
def index():
    form = AppreciationForm()
    appreciations = Appreciation.get_all()
    like_form = LikeForm()
    comment_form = CommentForm()
    appreciations_given = Appreciation.count_by_user(current_user)
    appreciations_received = Mention.count_by_user(current_user)
    most_appreciated = Appreciation.most_appreciated()

    return render_template('home.html', user=current_user, form=form, appreciations=appreciations,
                           like_form=like_form, comment_form=comment_form, appreciations_given=appreciations_given,
                           appreciations_received=appreciations_received, most_appreciated=most_appreciated)
