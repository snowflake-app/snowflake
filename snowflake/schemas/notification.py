from marshmallow_sqlalchemy.fields import Nested

from .user import UserSchema
from ..marshmallow import marshmallow
from ..models import Notification


class NotificationSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Notification

    user = Nested(UserSchema)
