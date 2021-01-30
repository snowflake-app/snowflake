from ..marshmallow import marshmallow


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class BaseSchema(marshmallow.Schema):
    # noinspection PyMethodMayBeStatic
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


class BaseSQLAlchemySchema(marshmallow.SQLAlchemySchema, BaseSchema):
    pass


class BaseSQLAlchemyAutoSchema(marshmallow.SQLAlchemyAutoSchema, BaseSchema):
    pass
