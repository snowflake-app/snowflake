from flask_redis import FlaskRedis

redis = FlaskRedis(socket_keepalive=True)


def health_check():
    redis.ping()
