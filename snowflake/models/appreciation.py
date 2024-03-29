from sqlalchemy import func

from .comment import Comment
from .like import Like
from .user import User
from ..db import db, execute


class Appreciation(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    created_by_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    created_by = db.relationship('User', lazy=True)
    likes = db.relationship('Like', viewonly=True, lazy=True)
    comments = db.relationship('Comment', viewonly=True, lazy=True)

    @property
    def creator(self):
        return self.created_by

    @staticmethod
    def get_all():
        return Appreciation.query.order_by(Appreciation.created_at.desc()).all()

    def get_like_count(self):
        return Like.query.filter_by(appreciation=self).count()

    def get_comment_count(self):
        return Comment.query.filter_by(appreciation=self).count()

    def is_liked_by(self, user: User):
        return Like.query.filter_by(appreciation=self, created_by=user).count() > 0

    @staticmethod
    def get(id_):
        return Appreciation.query.get(id_)

    def get_mentions(self):
        return self.mentions

    @staticmethod
    def count_by_user(user: User):
        return Appreciation.query.filter_by(created_by=user).count()

    @staticmethod
    def most_appreciated():
        rows = execute(
            '''
            SELECT user_id, COUNT(user_id) AS c FROM mention m
            JOIN "appreciation" a ON m.appreciation_id=a.id
            WHERE a.created_at BETWEEN date_trunc('month', CURRENT_DATE)
            AND (date_trunc('month', CURRENT_DATE) + INTERVAL '1 month - 1 second')
            GROUP BY user_id ORDER BY c DESC LIMIT 5
            ''')

        result = []

        for row in rows:  # pylint: disable=not-an-iterable
            user = User.get(row[0])

            count = row[1]

            result.append({
                'user': user,
                'count': count
            })

        return result

    def get_comments(self):
        return self.comments
