import requests
from minio import Minio

from snowflake import settings

STORAGE_BASE_URL = settings.storage_base_url()
S3_SETTINGS = settings.s3_settings()
USER_AGENT = f'Snowflake/1.0 (+{settings.base_url()})'

minio = Minio(
    S3_SETTINGS['HOST'],
    access_key=S3_SETTINGS['ACCESS_KEY'],
    secret_key=S3_SETTINGS['SECRET_KEY'],
    secure=S3_SETTINGS['SECURE']
)
BUCKET_NAME = S3_SETTINGS['BUCKET']


def make_http_request(url):
    return requests.get(url, headers={
        'User-Agent': USER_AGENT
    }, allow_redirects=True, stream=True)


def try_parse_len(string):
    try:
        return int(string)
    except ValueError:
        return -1


def put_remote_object(key, url):
    response = make_http_request(url)

    if response.status_code != 200:
        raise ValueError(f'Server returned status {response.status_code}')

    response.raw.decode_content = True
    content_length = try_parse_len(response.headers.get('Content-Length', '-1'))
    content_type = response.headers.get('Content-Type', 'application/octet-stream')

    minio.put_object(BUCKET_NAME, key, response.raw, content_length, content_type=content_type)
    return STORAGE_BASE_URL + '/' + key
