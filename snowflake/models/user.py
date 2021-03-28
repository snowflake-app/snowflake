from flask_login import UserMixin
from sqlalchemy import func

from ..db import db


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    designation = db.Column(db.Text, nullable=False)
    team_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    profile_pic = db.Column(db.String)
    username = db.Column(db.String(255), nullable=False, unique=True)

    created_at = db.Column(db.DateTime, server_default=func.now())

    appreciations = db.relationship('Appreciation', viewonly=True, lazy=True)

    @staticmethod
    def get(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_name_prefix(q: str):
        q = q.lower()
        return User.query.filter(
            func.lower(User.username).startswith(q) |
            func.lower(User.name).startswith(q)).all()
