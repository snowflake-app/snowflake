from flask import g
from flask_session import RedisSessionInterface


class CustomSessionInterface(RedisSessionInterface):
    def save_session(self, *args, **kwargs):
        if not g.get('login_via_header'):
            super().save_session(*args, **kwargs)
