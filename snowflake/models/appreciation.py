from .user import User
from ..db import db


class Appreciation(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    created_by_id = db.Column(db.String, db.ForeignKey('user.id'))
    created_by = db.relationship('User', backref=db.backref('appreciations', lazy=True))

    likes = db.relationship('Like', lazy=True)
    comments = db.relationship('Comment', lazy=True)

    @property
    def creator(self):
        return self.created_by

    @staticmethod
    def create(appreciation):
        db.session.add(appreciation)
        db.session.commit()

    @staticmethod
    def get_all():
        return Appreciation.query.order_by(Appreciation.created_at.desc()).all()

    def get_like_count(self):
        return db.session.scalar('SELECT COUNT(*) FROM "like" l WHERE l.appreciation_id = :id', {'id': self.id})

    def get_comment_count(self):
        return db.session.scalar('SELECT COUNT(*) FROM comment c WHERE c.appreciation_id = :id', {'id': self.id})

    def is_liked_by(self, user: User):
        return db.session.scalar(
            'SELECT COUNT(*) FROM "like" l WHERE l.appreciation_id = :appreciation_id'
            ' AND l.user_id = :user_id',
            {'appreciation_id': self.id, 'user_id': user.id}) > 0

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
        rows = db.session.execute(
            '''
            SELECT user_id, COUNT(user_id) AS c FROM mention m JOIN "appreciation" a ON m.appreciation_id=a.id
            WHERE a.created_at BETWEEN date_trunc('month', CURRENT_DATE) 
            AND (date_trunc('month', CURRENT_DATE) + INTERVAL '1 month - 1 second')
            GROUP BY user_id ORDER BY c DESC LIMIT 5
            ''')

        result = []

        for row in rows:
            user = User.get(row[0])

            count = row[1]

            result.append({
                'user': user,
                'count': count
            })

        return result

    def get_comments(self):
        return self.comments
