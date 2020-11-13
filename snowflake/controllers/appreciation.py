import re
from datetime import datetime

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from snowflake.forms import AppreciationForm, LikeForm, CommentForm
from snowflake.models import Appreciation, User, Mention, Like, Comment

blueprint = Blueprint('appreciation', __name__)


@blueprint.route('/appreciate', methods=['POST'])
def appreciate():
    form = AppreciationForm()
    if form.validate_on_submit():
        appreciation = Appreciation(content=form.content.data, created_by=current_user, created_at=datetime.now())
        Appreciation.create(appreciation)

        mentions = re.findall(r'@[a-zA-Z0-9._]+', form.content.data)
        for mention in mentions:
            user = User.get_by_username(mention[1:])
            if user is None:
                continue
            m = Mention(user=user, appreciation=appreciation)
            Mention.create(m)

        return redirect(url_for('index.index'))
    else:
        return render_template('login.html')


@blueprint.route('/like', methods=['POST'])
def like():
    form = LikeForm()
    if current_user.is_authenticated and form.validate():
        appreciation = Appreciation.get(form.appreciation.data)

        l = Like(appreciation=appreciation, user=current_user)
        Like.create(l)

        return redirect(url_for('index.index'))
    else:
        return render_template('login.html')


@blueprint.route('/comment', methods=['POST'])
@login_required
def comment():
    form = CommentForm()
    if form.validate():
        appreciation = Appreciation.get(form.appreciation.data)

        c = Comment(appreciation=appreciation, user=current_user, content=form.content.data, created_at=datetime.now())
        Comment.create(c)

    return redirect(url_for('index.index'))


@blueprint.route('/dislike', methods=['POST'])
def dislike():
    form = LikeForm()
    if current_user.is_authenticated and form.validate():
        appreciation = Appreciation.get(form.appreciation.data)

        Like.dislike(appreciation=appreciation, user=current_user)

        return redirect(url_for('index.index'))
    else:
        return render_template('login.html')
