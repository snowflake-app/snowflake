from sqlalchemy import func

from ..db import db


class Mention(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', foreign_keys=(user_id,),
                           backref=db.backref('mentions', lazy=True))

    appreciation_id = db.Column(db.BigInteger, db.ForeignKey('appreciation.id'), nullable=False)
    appreciation = db.relationship('Appreciation', backref=db.backref('mentions', lazy=True))

    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    created_by_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    created_by = db.relationship('User', foreign_keys=(created_by_id,),
                                 backref=db.backref('mentions_given', lazy=True))

    @staticmethod
    def count_by_user(user):
        return Mention.query.filter_by(user_id=user.id).count()
