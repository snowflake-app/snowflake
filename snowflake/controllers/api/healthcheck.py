from flask import jsonify, Blueprint

from ... import db, redis

blueprint = Blueprint('api.healthcheck', __name__)


@blueprint.route('')
def check_status():
    db.health_check()
    redis.health_check()
    return jsonify({'message': 'OK'}), 200
