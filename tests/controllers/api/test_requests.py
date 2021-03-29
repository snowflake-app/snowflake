from flask import jsonify

from snowflake.controllers.api.request import requires_json


def test_requires_json_returns_400_if_request_is_not_json(app):
    @requires_json
    def handler_func():
        return jsonify("OK"), 200

    with app.test_request_context('/api/endpoint', json={"message": "hello"}):
        resp, status = handler_func()
        assert status == 200
        assert resp.json == "OK"

    with app.test_request_context('/api/endpoint', data={"message": "hello"}):
        resp, status = handler_func()
        assert status == 400
        assert resp.json == {"message": "Bad request"}
