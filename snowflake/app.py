import json
import re
from datetime import datetime

from flask import Flask, redirect, url_for, render_template
from flask_login import (
    LoginManager,
    current_user,
    logout_user,
    login_required)
from markupsafe import Markup

from . import api, filters, settings
from .controllers import login, register
from .forms import AppreciationForm, LikeForm, CommentForm, OneOnOneForm, OneOnOneActionItemForm, \
    OneOnOneActionItemStateChange
from .models import Appreciation, Comment, Like, Mention, OneOnOne, OneOnOneActionItem, User

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.login"


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


app.register_blueprint(api.users.blueprint, url_prefix="/api/users")
app.register_blueprint(login.blueprint, url_prefix="/login")
app.register_blueprint(register.blueprint, url_prefix="/register")


@app.route("/")
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


@app.route('/profile', defaults={'username': None})
@app.route('/profile/<username>')
def profile(username):
    user = current_user if username is None else User.get_by_username(username)

    appreciations_given = Appreciation.count_by_user(user)
    appreciations_received = Mention.count_by_user(user)

    return render_template('profile.html', user=user, appreciations_given=appreciations_given,
                           appreciations_received=appreciations_received)


@app.route('/1-on-1s', methods=['POST', 'GET'], defaults={'_id': None})
@app.route('/1-on-1s/<_id>', methods=['POST', 'GET'])
@login_required
def one_on_one(_id):
    form = OneOnOneForm()
    action_item_form = OneOnOneActionItemForm()
    action_item_state_change_form = OneOnOneActionItemStateChange()

    if form.validate_on_submit():
        user = User.get_by_username(form.user.data)
        o = OneOnOne(user=user, created_by=current_user)
        OneOnOne.create(o)
        return redirect(url_for("one_on_one"))

    one_on_ones = OneOnOne.get_by_user(current_user)
    o = OneOnOne.get(_id) if _id is not None else one_on_ones[0] if len(one_on_ones) else None
    return render_template('1-on-1s.html',
                           one_on_ones=one_on_ones,
                           form=form,
                           action_item_form=action_item_form,
                           action_item_state_change_form=action_item_state_change_form,
                           one_on_one=o)


@app.route('/1-on-1s/action-items', methods=['POST'])
@login_required
def one_on_one_action_item():
    form = OneOnOneActionItemForm()

    if form.validate():
        o = OneOnOne.get(form.one_on_one.data)
        action_item = OneOnOneActionItem(content=form.content.data, one_on_one=o, created_by=current_user, state=0)

        OneOnOneActionItem.create(action_item)

    return redirect(f'/1-on-1s/{form.one_on_one.data}')


@app.route('/1-on-1s/action-items/done', methods=['POST'])
@login_required
def one_on_one_action_item_done():
    form = OneOnOneActionItemStateChange()
    if form.validate_on_submit():
        action_item_data = form.action_item.data
        action_item = OneOnOneActionItem.get(action_item_data)
        action_item.state = 1
        action_item.update()

        return redirect(f'/1-on-1s/{action_item.one_on_one.id}')

    return url_for('one_on_one')


@app.route('/appreciate', methods=['POST'])
def appreciate():
    form = AppreciationForm()
    if form.validate_on_submit():
        appreciation = Appreciation(content=form.content.data, creator=current_user, created_at=datetime.now())
        Appreciation.create(appreciation)

        mentions = re.findall(r'@[a-zA-Z0-9._]+', form.content.data)
        for mention in mentions:
            user = User.get_by_username(mention[1:])
            if user is None:
                continue
            m = Mention(user=user, appreciation=appreciation)
            Mention.create(m)

        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/like', methods=['POST'])
def like():
    form = LikeForm()
    if current_user.is_authenticated and form.validate():
        appreciation = Appreciation.get(form.appreciation.data)

        l = Like(appreciation=appreciation, user=current_user)
        Like.create(l)

        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/comment', methods=['POST'])
@login_required
def comment():
    form = CommentForm()
    if form.validate():
        appreciation = Appreciation.get(form.appreciation.data)

        c = Comment(appreciation=appreciation, user=current_user, content=form.content.data, created_at=datetime.now())
        Comment.create(c)

    return redirect(url_for('index'))


@app.route('/dislike', methods=['POST'])
def dislike():
    form = LikeForm()
    if current_user.is_authenticated and form.validate():
        appreciation = Appreciation.get(form.appreciation.data)

        Like.dislike(appreciation=appreciation, user=current_user)

        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.template_filter()
def add_mentions(text: str):
    mentions = set(re.findall(r'@[a-zA-Z0-9._]+', text))

    replacement = {}
    for mention in mentions:
        username = mention[1:]
        user = User.get_by_username(username)
        if user is None:
            continue

        replacement[mention] = f'<a href="/profile/{username}">{mention}</a>'

    for k, v in replacement.items():
        text = text.replace(k, v)

    return Markup(text)


app.add_template_filter(filters.humanize_time)
app.add_template_filter(filters.iso_time)


@app.context_processor
def setup():
    def entrypoint(file: str):
        with open(app.static_folder + "/assets/manifest.json") as f:
            manifest = json.load(f)
            chunk = manifest[file]

            if app.debug:
                return 'http://localhost:8080/' + chunk
            else:
                return url_for('static', filename='assets/' + chunk)

    return {
        'entrypoint': entrypoint
    }
