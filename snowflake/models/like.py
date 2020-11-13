from ..db import db


class Like(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('likes', lazy=True))
    appreciation_id = db.Column(db.String, db.ForeignKey('appreciation.id'), nullable=False)
    appreciation = db.relationship('Appreciation')

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
