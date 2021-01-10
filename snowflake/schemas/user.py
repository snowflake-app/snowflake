from ..marshmallow import marshmallow
from ..models import User


class UserSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("id",)
