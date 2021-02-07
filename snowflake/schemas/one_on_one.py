from marshmallow.fields import List
from marshmallow_sqlalchemy.fields import Nested

from .base import BaseSQLAlchemySchema
from .fields import UserByUsername
from .user import UserSchema
from ..marshmallow import marshmallow
from ..models import OneOnOne, OneOnOneActionItem


class OneOnOneActionItemSchema(BaseSQLAlchemySchema):
    class Meta:
        model = OneOnOneActionItem

    id = marshmallow.auto_field()
    state = marshmallow.auto_field()
    content = marshmallow.auto_field()

    created_by = Nested(UserSchema)


class CreateOrEditOneOnOneActionItemSchema(BaseSQLAlchemySchema):
    class Meta:
        model = OneOnOneActionItem
        load_instance = True

    state = marshmallow.auto_field()
    content = marshmallow.auto_field()


class OneOnOneSchema(BaseSQLAlchemySchema):
    class Meta:
        model = OneOnOne

    id = marshmallow.auto_field()
    created_at = marshmallow.auto_field()
    created_by = Nested(UserSchema)
    user = Nested(UserSchema)


class GetOneOnOneSchema(OneOnOneSchema):
    action_items = List(Nested(OneOnOneActionItemSchema))


class CreateOneOnOneSchema(BaseSQLAlchemySchema):
    class Meta:
        model = OneOnOne
        load_instance = True

    user = UserByUsername()
