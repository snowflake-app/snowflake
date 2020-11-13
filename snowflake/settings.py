import os

import requests
from flask import Flask

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


def init_app(app: Flask):
    app.secret_key = os.getenvb(b"SECRET_KEY") or os.urandom(24)

    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI'),
        GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID"),
        GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET"),
        GOOGLE_PROVIDER_CONFIG=requests.get(GOOGLE_DISCOVERY_URL).json(),
        BASE_URL=os.getenv('BASE_URL', 'http://127.0.0.1:5000'),
    )
