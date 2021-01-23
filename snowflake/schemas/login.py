from marshmallow.fields import String, DateTime, Nested

from .user import UserSchema
from ..marshmallow import marshmallow


class LoginSchema(marshmallow.Schema):
    token = String()


class LoginResponseSchema(marshmallow.Schema):
    token = String()
    expiry = DateTime()
    refresh_token = String()

    user = Nested(UserSchema)
