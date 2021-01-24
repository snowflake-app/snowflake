from flask import jsonify


def error_body(message):
    return jsonify({'message': message})


def bad_request(message="Bad request"):
    return error_body(message), 400


def not_found(message="Not found"):
    return error_body(message), 404


def forbidden(message="Forbidden"):
    return jsonify(message), 403


def unauthorized(message="Unauthorized"):
    return jsonify(message), 401
