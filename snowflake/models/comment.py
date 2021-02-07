from datetime import datetime

from .appreciation import Appreciation
from ..db import db


class Comment(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    created_by = db.relationship('User')

    appreciation_id = db.Column(db.BigInteger, db.ForeignKey('appreciation.id'), nullable=False)
    appreciation: Appreciation = db.relationship('Appreciation')

    @property
    def user_id(self):
        return self.created_by_id

    @property
    def user(self):
        return self.created_by

    @staticmethod
    def create(comment):
        db.session.add(comment)
        db.session.commit()

    @staticmethod
    def get(comment_id: int):
        return Comment.query.get(comment_id)
