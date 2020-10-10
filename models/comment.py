from db import get_db
from models.user import User


class Comment:
    def __init__(self, appreciation, user: User, content, created_at, id_=-1):
        self.user = user
        self.appreciation = appreciation
        self.content = content
        self.created_at = created_at
        self.id = id_

    @staticmethod
    def create(comment):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    INSERT INTO comment(appreciation_id, user_id, content, created_at)
                    VALUES (%s, %s, %s, %s) RETURNING id
                    ''',
                    (comment.appreciation.id, comment.user.id, comment.content, comment.created_at),
                )
                comment.id = c.fetchone()[0]
