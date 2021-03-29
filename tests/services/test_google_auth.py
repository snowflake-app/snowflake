from unittest.mock import patch, Mock

from snowflake.services.google_auth import UserInfo, get_user_info


@patch('snowflake.services.google_auth.verify_oauth2_token')
def test_get_user_info_parses_token(mock_verify_outh2_token: Mock, app):
    with app.app_context():
        account_id = 'd8708828-6a01-4b7e-ab15-bc48acb8011e'
        name = 'Hello'
        email = 'hello@example.com'
        picture = 'https://example.com/hello.jpg'
        mock_verify_outh2_token.return_value = {'sub': account_id, 'given_name': name,
                                                'email': email,
                                                'picture': picture}

        token = '3f3b4388-69b0-4197-ac61-2fd198e6f61e'
        value = get_user_info(token)

        assert value == UserInfo(id=account_id, name=name, email=email, picture=picture)

        assert mock_verify_outh2_token.call_args[0][0] == token
