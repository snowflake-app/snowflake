import os

import requests
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenvb(b"SECRET_KEY") or os.urandom(24)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:5000')


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
