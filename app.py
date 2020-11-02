import json
import re
from datetime import datetime

import requests
from flask import Flask, redirect, request, url_for, render_template, session
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required)
from markupsafe import Markup
from oauthlib.oauth2 import WebApplicationClient

import filters
import settings
from forms import RegistrationForm, AppreciationForm, LikeForm, CommentForm, OneOnOneForm, OneOnOneActionItemForm, \
    OneOnOneActionItemStateChange
from models.appreciation import Appreciation
from models.comment import Comment
from models.like import Like
from models.mention import Mention
from models.one_on_one import OneOnOne, OneOnOneActionItem
from models.user import User

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

client = WebApplicationClient(settings.GOOGLE_CLIENT_ID)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


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


def get_google_provider_cfg():
    return requests.get(settings.GOOGLE_DISCOVERY_URL).json()


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


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    callback_url = settings.BASE_URL + url_for('callback')
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=callback_url,
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    callback_url = settings.BASE_URL + url_for('callback')
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=callback_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]

        # Doesn't exist? Add it to the database.
        user = User.get(unique_id)
        if not user:
            session['unique_id'] = unique_id
            session['users_email'] = users_email
            session['picture'] = picture
            session['users_name'] = users_name
            return redirect(url_for("register"))
        # Create a user in your db with the information provided
        # by Google

        # Begin user session by logging the user in
        login_user(user)

        # Send user back to homepage
        return redirect(url_for("index"))
    else:
        return "User email not available or not verified by Google.", 400


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate():
        unique_id = session['unique_id']
        users_email = session['users_email']
        picture = session['picture']
        full_name = session['users_name']
        username = users_email.split("@")[0]

        user = User(id_=unique_id, email=users_email, name=full_name, profile_pic=picture,
                    team_name=form.team_name.data, designation=form.designation.data, username=username)

        User.create(user)

        login_user(user)

        return redirect(url_for('index'))

    return render_template('welcome.html', form=form, user_name=session['users_name'], picture=session['picture'])


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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
