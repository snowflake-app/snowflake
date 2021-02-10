import json

import requests
from flask import Blueprint, request, url_for, session, redirect, render_template, current_app, \
    flash
from flask_login import login_user
from oauthlib.oauth2 import WebApplicationClient

from snowflake.models import User

blueprint = Blueprint('login', __name__)


@blueprint.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    google_provider_cfg = current_app.config['GOOGLE_PROVIDER_CONFIG']
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    callback_url = current_app.config['BASE_URL'] + url_for('login.callback')
    client = WebApplicationClient(current_app.config['GOOGLE_CLIENT_ID'])

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=callback_url,
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@blueprint.route("/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = current_app.config['GOOGLE_PROVIDER_CONFIG']
    token_endpoint = google_provider_cfg["token_endpoint"]

    callback_url = current_app.config['BASE_URL'] + url_for('login.callback')
    client = WebApplicationClient(current_app.config['GOOGLE_CLIENT_ID'])

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
        auth=(current_app.config['GOOGLE_CLIENT_ID'], current_app.config['GOOGLE_CLIENT_SECRET']),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    uri, headers, body = client.add_token(google_provider_cfg["userinfo_endpoint"])
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        user = User.get(unique_id)
        if not user:
            session['unique_id'] = unique_id
            session['users_email'] = userinfo_response.json()["email"]
            session['picture'] = userinfo_response.json()["picture"]
            session['users_name'] = userinfo_response.json()["given_name"]
            return redirect(url_for("register.register"))

        login_user(user)

        return redirect(url_for("index.index"))

    flash("User email not available or not verified by Google.", category="danger")
    return redirect(url_for("login.login"))
