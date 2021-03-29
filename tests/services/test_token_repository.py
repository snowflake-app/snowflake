from unittest.mock import patch

from snowflake.services import token_repository


@patch('snowflake.services.token_repository.redis')
def test_save_should_save_key_with_prefix_and_ttl(mock_redis):
    token_repository.save("key", "12345", 100)

    assert mock_redis.setex.called_with("token:key", "12345", 100)


@patch('snowflake.services.token_repository.redis')
def test_get_should_fetch_key_with_prefix(mock_redis):
    mock_redis.get.return_value = b"12345"

    assert token_repository.get("key") == "12345"
    assert mock_redis.get.called_with("token:key")


@patch('snowflake.services.token_repository.redis')
def test_get_should_return_none_if_key_not_found(mock_redis):
    mock_redis.get.return_value = None

    assert token_repository.get("key") is None
    assert mock_redis.get.called_with("token:key")


@patch('snowflake.services.token_repository.redis')
def test_delete_should_delete_key_with_prefix(mock_redis):
    token_repository.delete("key")

    assert mock_redis.delete.called_with("token:key")
