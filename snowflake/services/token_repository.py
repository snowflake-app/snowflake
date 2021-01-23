from redis import Redis

from .. import settings

redis = Redis.from_url(settings.REDIS_URL)


def __with_prefix(key):
    return f"token:{key}"


def save(key, value, expiry):
    return redis.setex(__with_prefix(key), expiry, value)


def get(key):
    value = redis.get(__with_prefix(key))

    if not value:
        return None

    return value.decode('utf-8')
