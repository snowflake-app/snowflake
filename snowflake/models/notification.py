from .user import User
from ..db import db


class Notification(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    created_at = db.Column(db.DateTime)

    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    type = db.Column(db.String)
    object_id = db.Column(db.String)
    read = db.Column(db.Boolean, default=False)

    @staticmethod
    def create(notification):
        db.session.add(notification)
        db.session.commit()

    @staticmethod
    def get(id_):
        return Notification.query.get(id_)

    @staticmethod
    def count_by_user(user: User):
        return Notification.query.filter_by(user=user).count()

    @staticmethod
    def get_by_user(user: User):
        return Notification.query.filter_by(user=user)

