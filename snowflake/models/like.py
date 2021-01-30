from datetime import datetime
from typing import TYPE_CHECKING

from ..db import db

if TYPE_CHECKING:
    from . import Appreciation


class Like(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    created_by_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    created_by = db.relationship('User', backref=db.backref('likes', lazy=True))

    appreciation_id = db.Column(db.String, db.ForeignKey('appreciation.id'), nullable=False)
    appreciation: 'Appreciation' = db.relationship('Appreciation')

    @staticmethod
    def create(like):
        db.session.add(like)
        db.session.commit()

    @staticmethod
    def get_by_appreciation(appreciation):
        return Like.query.filter_by(appreciation_id=appreciation.id).all()

    @staticmethod
    def dislike(appreciation, user):
        like = Like.query.filter_by(appreciation_id=appreciation.id, user_id=user.id).first()
        db.session.delete(like)
        db.session.commit()

    @staticmethod
    def get_by_appreciation_and_user(appreciation, user):
        return Like.query.filter_by(appreciation=appreciation, user=user).first()
