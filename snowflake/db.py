import psycopg2
from flask import g


def open_connection():
    db = psycopg2.connect('')
    return db


def get_db():
    if "db" not in g:
        g.db = open_connection()

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
