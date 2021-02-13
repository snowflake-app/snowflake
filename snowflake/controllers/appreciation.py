import re
from datetime import datetime

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from snowflake.forms import AppreciationForm, LikeForm, CommentForm
from snowflake.models import Appreciation, User, Mention, Like, Comment
from snowflake.services import notification

blueprint = Blueprint('appreciation', __name__)


@blueprint.route('/appreciate', methods=['POST'])
def appreciate():
    form = AppreciationForm()
    if form.validate_on_submit():
        appreciation = Appreciation(content=form.content.data, created_by=current_user,
                                    created_at=datetime.now())
        Appreciation.create(appreciation)

        mentions = re.findall(r'@[a-zA-Z0-9._]+', form.content.data)
        for mention_text in mentions:
            user = User.get_by_username(mention_text[1:])
            if user is None:
                continue
            mention = Mention(user=user, appreciation=appreciation, created_by=current_user)
            Mention.create(mention)

        notification.notify_appreciation(appreciation)

        return redirect(url_for('index.index'))

    return render_template('login.html')


@blueprint.route('/like', methods=['POST'])
@login_required
def like():
    form = LikeForm()
    if form.validate_on_submit():
        appreciation = Appreciation.get(form.appreciation.data)

        new_like = Like(appreciation=appreciation, created_by=current_user)
        Like.create(new_like)

        return redirect(url_for('index.index'))

    return render_template('login.html')


@blueprint.route('/comment', methods=['POST'])
@login_required
def comment():
    form = CommentForm()
    if form.validate_on_submit():
        appreciation = Appreciation.get(form.appreciation.data)

        new_comment = Comment(appreciation=appreciation,
                              created_by=current_user,
                              content=form.content.data,
                              created_at=datetime.now())
        Comment.create(new_comment)

        notification.notify_comment(new_comment)

    return redirect(url_for('index.index'))


@blueprint.route('/dislike', methods=['POST'])
@login_required
def dislike():
    form = LikeForm()
    if form.validate_on_submit():
        appreciation = Appreciation.get(form.appreciation.data)

        Like.dislike(appreciation=appreciation, user=current_user)

        return redirect(url_for('index.index'))

    return render_template('login.html')
