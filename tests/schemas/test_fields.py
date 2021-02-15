from unittest.mock import patch

import pytest
from marshmallow import ValidationError

from snowflake.models import User
from snowflake.schemas.base import BaseSchema
from snowflake.schemas.fields import UserByUsername


class ExampleSchema(BaseSchema):
    user = UserByUsername()


@patch('snowflake.schemas.fields.User.get_by_username')
def test_user_by_username_should_deserialize_user(mock_get_by_username):
    user = User(id='1', username="example")
    mock_get_by_username.return_value = user

    schema = ExampleSchema()

    assert schema.load({'user': "example"}) == {'user': user}
    assert mock_get_by_username.is_called_with("example")


@patch('snowflake.schemas.fields.User.get_by_username')
def test_user_by_username_should_rise_error_if_user_not_found(mock_get_by_username):
    mock_get_by_username.return_value = None

    schema = ExampleSchema()

    with pytest.raises(ValidationError) as ex_info:
        assert schema.load({'user': "example"})

    assert ex_info.value.messages == {'user': ["User example not found"]}
    assert mock_get_by_username.is_called_with("example")
