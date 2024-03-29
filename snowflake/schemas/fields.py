from marshmallow import ValidationError
from marshmallow.fields import Field

from ..models import User


class UserByUsername(Field):
    def _deserialize(self, value: str, attr, data, **kwargs):
        user = User.get_by_username(value)

        if not user:
            raise ValidationError(f"User {value} not found")

        return user
