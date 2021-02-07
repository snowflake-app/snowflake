from .base import BaseSQLAlchemyAutoSchema
from ..models import User


class UserSchema(BaseSQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("id",)
