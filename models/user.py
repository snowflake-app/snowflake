from flask_login import UserMixin

from db import get_db


class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic, team_name, designation, username):
        self.designation = designation
        self.team_name = team_name
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.username = username

    @staticmethod
    def get(user_id):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    'SELECT id, name, email, profile_pic, team_name, designation, username FROM "user" WHERE id = %s',
                    (user_id,)
                )
                return User.__bind_user(c.fetchone())

    @staticmethod
    def __bind_user(row):
        if not row:
            return None

        return User(
            id_=row[0], name=row[1], email=row[2], profile_pic=row[3], team_name=row[4],
            designation=row[5],
            username=row[6]
        )

    @staticmethod
    def create(user):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    'INSERT INTO "user" (id, name, email, profile_pic, team_name, designation, username) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (user.id, user.name, user.email, user.profile_pic, user.team_name, user.designation, user.username),
                )

    @staticmethod
    def get_by_username(username):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    'SELECT id, name, email, profile_pic, team_name, designation, username'
                    ' FROM "user" WHERE username = %s', (username,)
                )
                return User.__bind_user(c.fetchone())

    @classmethod
    def find_by_name_prefix(cls, term):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    'SELECT id, name, email, profile_pic, team_name, designation, username'
                    ' FROM "user" WHERE username LIKE %s', (term + '%',)
                )

                return [User.__bind_user(row) for row in c.fetchall()]
