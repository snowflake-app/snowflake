from unittest.mock import patch
from uuid import uuid4

from snowflake import settings
from snowflake.models import User
from snowflake.services import token_manager

user = User(id='12345', name="John done")
token = uuid4()


@patch('snowflake.services.token_repository.redis')
@patch('snowflake.services.token_manager.uuid4')
def test_create_should_issue_new_token(mock_uuid4, mock_redis):
    mock_uuid4.return_value = token

    assert token_manager.create(user) == str(token)
    assert mock_redis.setex.called_with(f"token:{token}", "12345", settings.TOKEN_VALIDITY_SECS)


@patch('snowflake.services.token_repository.redis')
@patch('snowflake.services.token_manager.User.get')
def test_load_user_should_fetch_key_with_prefix(mock_user_get, mock_redis):
    mock_redis.get.return_value = b"12345"
    mock_user_get.return_value = user

    assert token_manager.load_user(str(token)) == user
    assert mock_redis.get.called_with(f"token:{token}")


@patch('snowflake.services.token_repository.redis')
def test_load_user_should_return_none_if_token_not_found(mock_redis):
    mock_redis.get.return_value = None

    assert token_manager.load_user(str(token)) is None
    assert mock_redis.get.called_with(f"token:{token}")


@patch('snowflake.services.token_repository.redis')
def test_revoke_should_delete_token(mock_redis):
    token_manager.revoke(token)

    assert mock_redis.delete.called_with(f"token:{token}")
