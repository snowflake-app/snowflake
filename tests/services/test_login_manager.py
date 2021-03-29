from unittest.mock import Mock, patch

import pytest
from flask import Request, g
from werkzeug.exceptions import HTTPException

from snowflake.models import User
from snowflake.services.login_manager import load_user_from_header, unauthorized_handler, \
    load_user, on_user_loaded_from_header


def test_load_user_from_header_returns_none_if_authorization_is_missing():
    mock_request = Mock(Request)
    mock_request.headers = {}

    assert load_user_from_header(mock_request) is None


def test_load_user_from_header_returns_400_if_header_is_malformed(app):
    with app.app_context():
        mock_request = Mock(Request)
        mock_request.headers = {
            'Authorization': 'Bearer'
        }

        with pytest.raises(HTTPException) as ex_info:
            load_user_from_header(mock_request)

        assert ex_info.value.code == 400
        # noinspection PyUnresolvedReferences
        assert ex_info.value.description[0].json == {
            'message': 'Malformed authorization'
        }


def test_load_user_from_header_returns_none_if_scheme_is_not_bearer(app):
    with app.app_context():
        mock_request = Mock(Request)
        mock_request.headers = {
            'Authorization': 'Basic aGVsbG86d29ybGQ='
        }

        assert load_user_from_header(mock_request) is None


@patch('snowflake.services.login_manager.token_manager.load_user')
def test_load_user_from_header_returns_user_for_token(mock_load_user: Mock, app):
    user = User(id='1', username='example')
    mock_load_user.return_value = user
    with app.app_context():
        mock_request = Mock(Request)
        mock_request.headers = {
            'Authorization': 'Bearer 2ebad019-c1bc-4acf-911d-02230b845959'
        }

        assert load_user_from_header(mock_request) == user
        assert mock_load_user.is_called_with('2ebad019-c1bc-4acf-911d-02230b845959')


def test_unauthorized_handler_returns_json_response_for_api_routes(app):
    with app.test_request_context('/api/users'):
        response, status = unauthorized_handler()

        assert status == 401
        assert response.json == {
            'message': 'Unauthorized'
        }


@patch('snowflake.services.login_manager.User.get')
def test_load_user_returns_user_by_id(mock_get):
    user = User(id='1', username='example')
    mock_get.return_value = user

    assert load_user('1') == user
    assert mock_get.is_called_with('1')


def test_unauthorized_handler_returns_redirect_for_routes(app):
    with app.test_request_context('/users'):
        response = unauthorized_handler()

        assert response.status_code == 302
        assert response.headers['Location'] == '/login/?next=%2Fusers'


def test_on_user_loaded_from_header_marks_request(app):
    with app.app_context(), app.test_request_context('/hello'):
        on_user_loaded_from_header()
        assert g.login_via_header
