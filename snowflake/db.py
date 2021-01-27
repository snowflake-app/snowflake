from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@contextmanager
def transaction():
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise


def health_check():
    db.session.execute("select 1")
