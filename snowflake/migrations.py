import datetime
import logging
import os
from dataclasses import dataclass
from os.path import dirname
from urllib.parse import urlparse

import psycopg2

from . import settings

logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))

log = logging.getLogger('migration')


def open_connection():
    uri = settings.database_uri()

    if uri is None:
        raise ValueError('DATABASE_URI not defined')

    result = urlparse(uri)
    return psycopg2.connect(
        database=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )


@dataclass
class Migration:
    version: int
    description: str
    script: str


def load_migrations():
    directory = os.path.join(dirname(__file__), '../migrations')

    files = [file for file in os.listdir(directory) if file.lower().endswith('.sql')]

    migrations = []

    for file in files:
        file_name = os.path.splitext(file)[0]
        version, description = file_name.split('_', 1)

        with open(os.path.join(directory, file)) as script_file:
            script = script_file.read()

            migrations.append(
                Migration(version=int(version), description=description, script=script))

    migrations.sort(key=lambda m: m.version)

    return migrations


def migrate():
    with open_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS migrations (
                   id SERIAL PRIMARY KEY,
                   version INTEGER NOT NULL,
                   description TEXT,
                   applied_at TIMESTAMP NOT NULL)
                """)

            cur.execute('SELECT version FROM migrations')
            rows = cur.fetchall()

            applied_versions = {row[0] for row in rows}

            migrations_to_apply = [migration for migration in load_migrations() if
                                   migration.version not in applied_versions]

            for migration in migrations_to_apply:
                log.info('Applying %s', migration.script)
                cur.execute(migration.script)

                cur.execute(
                    '''
                    INSERT INTO migrations(version, description, applied_at)
                    VALUES (%s, %s, %s)
                    ''',
                    (migration.version, migration.description, datetime.datetime.now()))
                log.info('Applied %s %s', migration.version, migration.description)

            log.info("Succesfully applied migrations till latest version")
