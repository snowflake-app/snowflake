from datetime import datetime

from ..db import db


class Mention(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('mentions', lazy=True))

    appreciation_id = db.Column(db.BigInteger, db.ForeignKey('appreciation.id'), nullable=False)
    appreciation = db.relationship('Appreciation', backref=db.backref('mentions', lazy=True))

    created_at = db.Column(db.DateTime, lambda _: datetime.now())

    created_by_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    created_by = db.relationship('User', backref=db.backref('mentions', lazy=True))

    @staticmethod
    def create(mention):
        db.session.add(mention)
        db.session.commit()

    @staticmethod
    def count_by_user(user):
        return Mention.query.filter_by(user_id=user.id).count()
