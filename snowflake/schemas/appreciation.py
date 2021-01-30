from marshmallow.fields import Integer, String, DateTime, List
from marshmallow_sqlalchemy.fields import Nested

from .base import BaseSQLAlchemySchema, BaseSchema
from ..marshmallow import marshmallow
from ..models import Like
from ..schemas.user import UserSchema


class LikeSchema(BaseSQLAlchemySchema):
    class Meta:
        model = Like

    id = marshmallow.auto_field()
    created_by = Nested(UserSchema)


class MentionSchema(BaseSchema):
    user = Nested(UserSchema)


class AppreciationSchema(BaseSchema):
    id = Integer()
    content = String()
    created_at = DateTime()

    created_by = Nested(UserSchema)

    like_count = Integer()
    comment_count = Integer()
    viewer_like = Nested(LikeSchema, exclude=("user",))

    mentions = List(Nested(MentionSchema))


class CreateAppreciationSchema(BaseSchema):
    class Meta:
        model = True
        load_instance = True

    content = String()
