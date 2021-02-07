from marshmallow import Schema
from marshmallow.fields import Nested, DateTime

from .user import UserSchema
from ..marshmallow import marshmallow


class ObjectSchema(Schema):
    id: marshmallow.auto_field()
    created_at = DateTime()
    created_by = Nested(UserSchema)
