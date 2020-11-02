from ..db import get_db
from .appreciation import Appreciation
from .user import User


class Like:
    def __init__(self, appreciation: Appreciation, user: User, id_=-1):
        self.user = user
        self.appreciation = appreciation
        self.id = id_

    @staticmethod
    def create(like):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    INSERT INTO likes(appreciation_id, user_id)
                    VALUES (%s, %s) RETURNING id
                    ''',
                    (like.appreciation.id, like.user.id),
                )
                like.id = c.fetchone()[0]

    @staticmethod
    def get_by_appreciation(appreciation):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    SELECT l.id,
                    u.id, u.name, u.email, u.profile_pic, u.team_name, u.designation, u.username
                    FROM likes l
                    JOIN "user" u ON l.user_id = u.id
                    WHERE l.appreciation_id = %s
                    ''', (appreciation.id,))
                rows = c.fetchall()

                likes = []

                for row in rows:
                    user = User(
                        id_=row[1], name=row[2], email=row[3], profile_pic=row[4], team_name=row[5], designation=row[6],
                        username=row[7]
                    )

                    like = Like(
                        appreciation=appreciation, user=user, id_=row[0]
                    )
                    likes.append(like)

                return likes

    @staticmethod
    def dislike(appreciation, user):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    'DELETE FROM likes l WHERE l.appreciation_id = %s AND l.user_id = %s', (appreciation.id, user.id))
