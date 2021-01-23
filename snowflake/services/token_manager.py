from uuid import uuid4

from . import token_repository
from .. import settings
from ..models import User


def create(user: User):
    token = str(uuid4())
    token_repository.save(token, user.id, settings.TOKEN_VALIDITY_SECS)

    return token


def load_user(token: str):
    user_id = token_repository.get(token)

    if not user_id:
        return None

    return User.get(user_id)
