import json

import requests
from flask import Blueprint, request, url_for, session, redirect, render_template
from flask_login import login_user
from oauthlib.oauth2 import WebApplicationClient

from snowflake import settings
from snowflake.models import User

blueprint = Blueprint('login', __name__)

client = WebApplicationClient(settings.GOOGLE_CLIENT_ID)


@blueprint.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    google_provider_cfg = settings.get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    callback_url = settings.BASE_URL + url_for('login.callback')
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=callback_url,
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@blueprint.route("/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = settings.get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    callback_url = settings.BASE_URL + url_for('login.callback')
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
