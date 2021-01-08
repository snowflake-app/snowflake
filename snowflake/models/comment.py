from ..db import db


class Comment(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    appreciation_id = db.Column(db.BigInteger, db.ForeignKey('appreciation.id'), nullable=False)
    appreciation = db.relationship('Appreciation')

    @staticmethod
    def create(comment):
        db.session.add(comment)
        db.session.commit()

    @staticmethod
    def get(comment_id: int):
        return Comment.query.get(comment_id)
