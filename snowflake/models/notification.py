from . import Comment
from .appreciation import Appreciation
from .user import User
from ..db import db

TYPE_APPRECIATION = "appreciation"
TYPE_COMMENT_ON_APPRECIATION_RECEIVED = "comment_on_appreciation_received"
TYPE_COMMENT_ON_APPRECIATION_GIVEN = "comment_on_appreciation_given"
TYPE_COMMENT_ON_APPRECIATION_COMMENTED = "comment_on_appreciation_commented"


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
    def count_unread_by_user(user: User):
        return Notification.query.filter_by(user=user, read=False).count()

    @staticmethod
    def get_by_user(user: User):
        return Notification.query.filter_by(user=user).all()

    @staticmethod
    def get_unread_by_user(user: User):
        return Notification.query.filter_by(user=user, read=False).all()

    @property
    def object(self):
        if self.type == TYPE_APPRECIATION:
            return Appreciation.get(int(self.object_id))
        elif self.type == TYPE_COMMENT_ON_APPRECIATION_GIVEN or self.type == TYPE_COMMENT_ON_APPRECIATION_RECEIVED:
            return Comment.get(int(self.object_id))

        return None
