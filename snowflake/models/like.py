from sqlalchemy import func

from ..db import db, transaction, delete


class Like(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    created_by_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    created_by = db.relationship('User', backref=db.backref('likes', lazy=True))

    appreciation_id = db.Column(db.BigInteger, db.ForeignKey('appreciation.id'), nullable=False)
    appreciation = db.relationship('Appreciation')

    @staticmethod
    def get_by_appreciation(appreciation):
        return Like.query.filter_by(appreciation_id=appreciation.id).all()

    @staticmethod
    def dislike(appreciation, user):
        like = Like.query.filter_by(appreciation=appreciation, user=user).first()
        with transaction():
            delete(like)

    @staticmethod
    def get_by_appreciation_and_user(appreciation, user):
        return Like.query.filter_by(appreciation=appreciation, created_by=user).first()
