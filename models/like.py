from db import get_db
from models.appreciation import Appreciation
from models.user import User


class Like:
    def __init__(self, appreciation: Appreciation, user: User, id_=-1):
        self.user = user
        self.appreciation = appreciation

    @staticmethod
    def create(like):
        db = get_db()
        db.execute(
            "INSERT INTO likes(appreciation_id, user_id) "
            "VALUES (?, ?)",
            (like.appreciation.id, like.user.id),
        )
        db.commit()

    @staticmethod
    def get_by_appreciation(appreciation):
        db = get_db()
        rows = db.execute(
            'SELECT l.id,u.id,u.name,u.email,u.profile_pic,u.team_name,u.designation FROM likes l JOIN user u ON l.user_id=u.id WHERE l.appreciation_id=?',
            (appreciation.id,)).fetchall()
        likes = []

        for row in rows:
            user = User(
                id_=row[1], name=row[2], email=row[3], profile_pic=row[4], team_name=row[5], designation=row[6]
            )

            like = Like(
                appreciation=appreciation, user=user, id_=row[0]
            )
            likes.append(like)

        return likes

    @staticmethod
    def dislike(appreciation, user):
        db = get_db()
        db.execute(
            'DELETE FROM likes where likes.appreciation_id=? and likes.user_id=?', (appreciation.id, user.id))
        db.commit()
