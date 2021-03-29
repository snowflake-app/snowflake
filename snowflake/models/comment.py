from sqlalchemy import func

from ..db import db


class Comment(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    created_by_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    created_by = db.relationship('User')

    appreciation_id = db.Column(db.BigInteger, db.ForeignKey('appreciation.id'), nullable=False)
    appreciation = db.relationship('Appreciation')

    @staticmethod
    def get(comment_id: int):
        return Comment.query.get(comment_id)
