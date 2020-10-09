from db import get_db
from models.user import User


class Mention:
    def __init__(self, appreciation, user, id_=-1):
        self.user = user
        self.appreciation = appreciation
        self.id_ = id_

    @staticmethod
    def create(mention):
        db = get_db()
        db.execute(
            "INSERT INTO mention(appreciation_id, user_id)"
            "VALUES (?, ?)",
            (mention.appreciation.id, mention.user.id),
        )
        db.commit()

    @staticmethod
    def count_by_user(user: User):
        db = get_db()
        return db.execute('SELECT COUNT(*) FROM mention m WHERE m.user_id = ?', (user.id,)).fetchone()[0]
