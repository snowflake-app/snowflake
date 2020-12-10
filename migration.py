# track which SQL scripts are already applied
import datetime
import os
from dataclasses import dataclass

from snowflake.db import open_connection


@dataclass
class Migration:
    version: int
    description: str
    script: str


def load_migrations(directory='migrations'):
    files = os.listdir(directory)

    migrations = []

    for file in files:
        if not file.endswith('.sql'):
            continue

        file_name = os.path.splitext(file)[0]
        version, description = file_name.split('_', 1)

        with open(os.path.join(directory, file)) as f:
            script = f.read()

            migrations.append(Migration(version=int(version), description=description, script=script))

    migrations.sort(key=lambda m: m.version)

    return migrations


def migrate():
    with open_connection() as conn:
        with conn.cursor() as c:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS migrations (
                   id SERIAL PRIMARY KEY,
                   version INTEGER NOT NULL,
                   description TEXT,
                   applied_at TIMESTAMP NOT NULL)
                """)

            c.execute('SELECT version FROM migrations')
            rows = c.fetchall()

            applied_versions = set([row[0] for row in rows])

            migrations = load_migrations()

            for migration in migrations:
                if migration.version not in applied_versions:
                    print('Applying', migration.script)
                    c.execute(migration.script)

                    c.execute('INSERT INTO migrations(version, description, applied_at) VALUES (%s, %s, %s)',
                              (migration.version, migration.description, datetime.datetime.now()))
                    print(f'Applied v{migration.version} {migration.description}')

            print("Applied migrations")


if __name__ == '__main__':
    migrate()
