from ..db import get_db
from .user import User


class Mention:
    def __init__(self, appreciation, user, id_=-1):
        self.user = user
        self.appreciation = appreciation
        self.id = id_

    @staticmethod
    def create(mention):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    INSERT INTO mention(appreciation_id, user_id)
                    VALUES (%s, %s) RETURNING id
                    ''', (mention.appreciation.id, mention.user.id),
                )
                mention.id = c.fetchone()[0]

    @staticmethod
    def count_by_user(user: User):
        with get_db() as db:
            with db.cursor() as c:
                c.execute('SELECT COUNT(*) FROM mention m WHERE m.user_id = %s', (user.id,))
                return c.fetchone()[0]
