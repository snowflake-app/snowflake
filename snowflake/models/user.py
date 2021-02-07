from datetime import datetime

from flask_login import UserMixin

from ..db import db


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255))
    designation = db.Column(db.Text)
    team_name = db.Column(db.String(255))
    email = db.Column(db.String)
    profile_pic = db.Column(db.String)
    username = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, lambda _: datetime.now())

    @staticmethod
    def get(user_id):
        return User.query.get(user_id)

    @staticmethod
    def create(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_name_prefix(q):
        return User.query.filter(User.username.startswith(q) | User.name.startswith(q)).all()
