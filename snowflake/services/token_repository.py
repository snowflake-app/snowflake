from ..redis import redis


def __with_prefix(key):
    return f"token:{key}"


def save(key, value, expiry):
    return redis.setex(__with_prefix(key), expiry, value)


def get(key):
    value = redis.get(__with_prefix(key))

    if not value:
        return None

    return value.decode('utf-8')


def delete(key: str):
    return redis.delete(__with_prefix(key))
