from marshmallow.fields import Boolean
from marshmallow_sqlalchemy.fields import Nested

from .base import BaseSQLAlchemyAutoSchema, BaseSchema
from .object import ObjectSchema
from ..models import Notification


class NotificationSchema(BaseSQLAlchemyAutoSchema):
    class Meta:
        model = Notification

    object = Nested(ObjectSchema)


class UpdateNotificationSchema(BaseSchema):
    read: Boolean()
