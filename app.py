import json
import os
import re
import time
from datetime import datetime

import requests
# Third-party libraries
from flask import Flask, redirect, request, url_for, render_template, session
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient

from forms import RegistrationForm, AppreciationForm, LikeForm, CommentForm
# Internal imports
from models.appreciation import Appreciation
from models.comment import Comment
from models.like import Like
from models.mention import Mention
from models.user import User

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def index():
    if current_user.is_authenticated:
        form = AppreciationForm(request.form)
        appreciations = Appreciation.get_all()
        like_form = LikeForm(request.form)
        appreciations_given = Appreciation.count_by_user(current_user)
        appreciations_received = Mention.count_by_user(current_user)
        most_appreciated = Appreciation.most_appreciated()

        return render_template('home.html', user=current_user, form=form, appreciations=appreciations,
                               like_form=like_form, appreciations_given=appreciations_given,
                               appreciations_received=appreciations_received, most_appreciated=most_appreciated)
    else:
        return render_template('login.html')


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route('/appreciate', methods=['POST'])
def appreciate():
    form = AppreciationForm(request.form)
    if current_user.is_authenticated and form.validate():
        appreciation = Appreciation(content=form.content.data, creator=current_user, created_at=int(time.time()))
        Appreciation.create(appreciation)

        mentions = re.findall(r'@[a-zA-Z0-9\._]+', form.content.data)
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
    form = LikeForm(request.form)
    if current_user.is_authenticated and form.validate():
        appreciation = Appreciation.get(form.appreciation.data)

        like = Like(appreciation=appreciation, user=current_user)
        Like.create(like)

        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/comment', methods=['POST'])
def comment():
    form = CommentForm(request.form)
    if current_user.is_authenticated and form.validate():
        appreciation = Appreciation.get(form.appreciation.data)

        c = Comment(appreciation=appreciation, user=current_user, content=form.content.data, created_at=datetime.now())
        Comment.create(c)

        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/dislike', methods=['POST'])
def dislike():
    form = LikeForm(request.form)
    if current_user.is_authenticated and form.validate():
        appreciation = Appreciation.get(form.appreciation.data)

        Like.dislike(appreciation=appreciation, user=current_user)

        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
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

        # Doesn't exist? Add it to the database.

        # Begin user session by logging the user in
        login_user(user)

        # Send user back to homepage
        return redirect(url_for("index"))
    else:
        return "User email not available or not verified by Google.", 400


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

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


if __name__ == "__main__":
    app.run(debug=True)
