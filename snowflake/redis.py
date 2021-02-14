from redis import Redis

from . import settings

redis = Redis.from_url(settings.redis_uri(), socket_keepalive=True)


def health_check():
    redis.ping()
