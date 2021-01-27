from redis import Redis

from . import settings

redis = Redis.from_url(settings.REDIS_URL, socket_keepalive=True)


def health_check():
    redis.ping()
