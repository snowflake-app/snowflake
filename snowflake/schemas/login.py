from marshmallow.fields import String, DateTime, Nested

from .base import BaseSchema
from .user import UserSchema


class LoginSchema(BaseSchema):
    token = String()


class LoginResponseSchema(BaseSchema):
    token = String()
    expiry = DateTime()
    refresh_token = String()

    user = Nested(UserSchema)
