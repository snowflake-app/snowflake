from flask import request

from .response import bad_request


def requires_json(wrapped_func):
    def func(*args, **kwargs):
        if not request.is_json:
            return bad_request()

        return wrapped_func(*args, **kwargs)

    return func
