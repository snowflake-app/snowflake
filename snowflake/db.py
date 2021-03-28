from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@contextmanager
def transaction():
    try:
        yield
        db.session.commit()  # pylint: disable=no-member
    except Exception:
        db.session.rollback()  # pylint: disable=no-member
        raise


def persist(*args):
    db.session.add_all(args)  # pylint: disable=no-member


def delete(obj):
    db.session.delete(obj)  # pylint: disable=no-member


def health_check():
    db.session.execute("select 1")  # pylint: disable=no-member


def execute(sql):
    return db.session.execute(sql)  # pylint: disable=no-member
