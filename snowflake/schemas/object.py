from marshmallow import Schema
from marshmallow.fields import Nested, DateTime, Str

from .user import UserSchema


class ObjectSchema(Schema):
    id = Str()
    created_at = DateTime()
    created_by = Nested(UserSchema)
