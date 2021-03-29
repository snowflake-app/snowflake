from unittest.mock import patch

from flask import g

from snowflake.services.session_interface import CustomSessionInterface


@patch('snowflake.services.session_interface.RedisSessionInterface.save_session')
def test_save_session_should_ignore_api_requests(mock_save_session, app):
    session = CustomSessionInterface(key_prefix="session", redis=None)

    with app.test_request_context("/api/users/example"):
        g.login_via_header = True
        session.save_session(app, None, None)

        assert not mock_save_session.called

    with app.test_request_context("/users/example"):
        session.save_session(app, None, None)

        assert mock_save_session.called
