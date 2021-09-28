from unittest.mock import patch, MagicMock

import pytest

from snowflake.services import file_system


@patch('snowflake.services.file_system.requests.get')
@patch.object(file_system.Minio, 'put_object')
def test_put_remote_object_fetches_and_stores_remote_file(mock_minio: MagicMock,
                                                          mock_get: MagicMock):
    mock_response = MagicMock()
    mock_get.return_value = mock_response
    mock_response.status_code = 200
    mock_response.headers = {
        'Content-Length': '1000',
        'Content-Type': 'image/jpeg'
    }

    key = 'key.jpeg'
    file_system.put_remote_object(key, 'http://example.com/image.jpg')

    assert mock_minio.called

    args, kwargs = mock_minio.call_args
    assert args[0] == file_system.BUCKET_NAME
    assert args[1] == key
    assert args[2] == mock_response.raw
    assert args[3] == 1000
    assert kwargs['content_type'] == 'image/jpeg'

    assert mock_response.raw.decode_content


@patch('snowflake.services.file_system.requests.get')
@patch.object(file_system.Minio, 'put_object')
def test_put_remote_object_set_length_as_none_when_response_has_no_length(mock_minio: MagicMock,
                                                                          mock_get: MagicMock):
    mock_response = MagicMock()
    mock_get.return_value = mock_response
    mock_response.status_code = 200
    mock_response.headers = {
        'Content-Type': 'image/jpeg'
    }

    key = 'key.jpeg'
    file_system.put_remote_object(key, 'http://example.com/image.jpg')

    assert mock_minio.called

    args, kwargs = mock_minio.call_args
    assert args[0] == file_system.BUCKET_NAME
    assert args[1] == key
    assert args[2] == mock_response.raw
    assert args[3] == -1
    assert kwargs['content_type'] == 'image/jpeg'

    assert mock_response.raw.decode_content


@patch('snowflake.services.file_system.requests.get')
@patch.object(file_system.Minio, 'put_object')
def test_put_remote_object_set_length_as_none_when_response_length_is_invalid(mock_minio: MagicMock,
                                                                              mock_get: MagicMock):
    mock_response = MagicMock()
    mock_get.return_value = mock_response
    mock_response.status_code = 200
    mock_response.headers = {
        'Content-Length': 'abcd',
        'Content-Type': 'image/jpeg'
    }

    key = 'key.jpeg'
    file_system.put_remote_object(key, 'http://example.com/image.jpg')

    assert mock_minio.called

    args, kwargs = mock_minio.call_args
    assert args[0] == file_system.BUCKET_NAME
    assert args[1] == key
    assert args[2] == mock_response.raw
    assert args[3] == -1
    assert kwargs['content_type'] == 'image/jpeg'

    assert mock_response.raw.decode_content


@patch('snowflake.services.file_system.requests.get')
@patch.object(file_system.Minio, 'put_object')
def test_put_remote_object_set_mime_as_octet_stream_when_unknown(mock_minio: MagicMock,
                                                                 mock_get: MagicMock):
    mock_response = MagicMock()
    mock_get.return_value = mock_response
    mock_response.status_code = 200
    mock_response.headers = {
        'Content-Length': '1000'
    }

    key = 'key.jpeg'
    file_system.put_remote_object(key, 'http://example.com/image.jpg')

    assert mock_minio.called

    args, kwargs = mock_minio.call_args
    assert args[0] == file_system.BUCKET_NAME
    assert args[1] == key
    assert args[2] == mock_response.raw
    assert args[3] == 1000
    assert kwargs['content_type'] == 'application/octet-stream'

    assert mock_response.raw.decode_content


@patch('snowflake.services.file_system.requests.get')
@patch.object(file_system.Minio, 'put_object')
def test_put_remote_object_raises_exception_for_non_200_status(mock_minio: MagicMock,
                                                               mock_get: MagicMock):
    mock_response = MagicMock()
    mock_get.return_value = mock_response
    mock_response.status_code = 404

    key = 'key.jpeg'

    with pytest.raises(ValueError) as excinfo:
        file_system.put_remote_object(key, 'http://example.com/image.jpg')

    assert excinfo.match('Server returned status 404')

    mock_minio.assert_not_called()
