# http://flask.pocoo.org/docs/1.0/tutorial/database/
import sqlite3

import click
from flask import g
from flask.cli import with_appcontext


def open_connection():
    db = sqlite3.connect(
        "sqlite_db", detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row

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
