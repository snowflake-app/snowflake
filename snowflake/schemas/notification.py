from .base import BaseSQLAlchemyAutoSchema
from ..models import Notification


class NotificationSchema(BaseSQLAlchemyAutoSchema):
    class Meta:
        model = Notification
