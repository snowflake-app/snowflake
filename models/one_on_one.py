from datetime import datetime

from db import get_db
from models.user import User


class OneOnOne:
    def __init__(self, user, created_by, created_at=datetime.now(), id_=-1):
        self.created_at = created_at
        self.created_by = created_by
        self.user = user
        self.id = id_

    @staticmethod
    def get(one_on_one_id):
        db = get_db()
        row = db.execute(
            "SELECT o.id, o.created_at,"
            " u.id, u.name, u.email, u.profile_pic, u.team_name, u.designation, u.username,"
            " u2.id, u2.name, u2.email, u2.profile_pic, u2.team_name, u2.designation, u2.username"
            " FROM one_on_one o"
            " JOIN user u on o.user_id = u.id"
            " JOIN user u2 on o.created_by_id = u2.id"
            " WHERE o.id = ?", (one_on_one_id,)
        ).fetchone()
        if not row:
            return None

        user = User(
            id_=row[2], name=row[3], email=row[4], profile_pic=row[5], team_name=row[6], designation=row[7],
            username=row[8]
        )

        created_by = User(
            id_=row[9], name=row[10], email=row[11], profile_pic=row[12], team_name=row[13], designation=row[14],
            username=row[15]
        )

        one_on_one = OneOnOne(
            user=user, created_by=created_by, id_=row[0], created_at=row[1]
        )

        return one_on_one

    @staticmethod
    def create(one_on_one):
        db = get_db()
        db.execute(
            "INSERT INTO one_on_one (user_id, created_by_id) "
            "VALUES (?, ?)",
            (one_on_one.user.id, one_on_one.created_by.id),
        )
        one_on_one.id = db.execute("SELECT LAST_INSERT_ROWID()").fetchone()[0]
        db.commit()

    @staticmethod
    def get_by_user(user):
        db = get_db()
        rows = db.execute(
            "SELECT o.id, o.created_at,"
            " u.id, u.name, u.email, u.profile_pic, u.team_name, u.designation, u.username,"
            " u2.id, u2.name, u2.email, u2.profile_pic, u2.team_name, u2.designation, u2.username"
            " FROM one_on_one o"
            " JOIN user u on o.user_id = u.id"
            " JOIN user u2 on o.created_by_id = u2.id"
            " WHERE user_id = ? OR created_by_id = ? ORDER BY o.created_at DESC", (user.id, user.id)
        ).fetchall()

        one_on_ones = []

        for row in rows:
            user = User(
                id_=row[2], name=row[3], email=row[4], profile_pic=row[5], team_name=row[6], designation=row[7],
                username=row[8]
            )

            created_by = User(
                id_=row[9], name=row[10], email=row[11], profile_pic=row[12], team_name=row[13], designation=row[14],
                username=row[15]
            )

            one_on_one = OneOnOne(
                user=user, created_by=created_by, id_=row[0], created_at=row[1]
            )

            one_on_ones.append(one_on_one)

        return one_on_ones
