from flask import jsonify

from snowflake.controllers.index import blueprint


@blueprint.route('/healthcheck')
def check_status(message):
    return jsonify({'message': 'message'}), 200
