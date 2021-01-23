from dataclasses import dataclass

from flask import current_app
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token

request = requests.Request()


@dataclass
class UserInfo:
    id: str
    name: str
    email: str
    picture: str


def get_user_info(id_token):
    client_id = current_app.config['GOOGLE_CLIENT_ID']
    id_info = verify_oauth2_token(id_token, request, client_id)

    user_id = id_info["sub"]

    return UserInfo(id=user_id,
                    name=id_info["given_name"],
                    email=id_info["email"],
                    picture=id_info["picture"])
