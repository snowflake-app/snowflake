from flask import jsonify


def bad_request(message):
    return 400, jsonify({'message': message})


def not_found():
    return 404, jsonify({'message': "Not found"})
