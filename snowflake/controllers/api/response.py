from flask import jsonify


def bad_request(message):
    return 400, jsonify({'message': message})
