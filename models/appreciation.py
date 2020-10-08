from db import get_db
from models.user import User


class Appreciation():
    def __init__(self, creator, content, created_at, id_=-1):
        self.id = id_
        self.creator = creator
        self.content = content
        # self.to = to
        self.created_at = created_at

    @staticmethod
    def create(appreciation):
        db = get_db()
        db.execute(
            "INSERT INTO appreciation(content, created_at, creator) "
            "VALUES (?, ?, ?)",
            (appreciation.content, appreciation.created_at, appreciation.creator.id),
        )
        db.commit()

    @staticmethod
    def get_all():
        db = get_db()
        rows = db.execute(
            'SELECT a.id, a.content, a.created_at, u.id, u.name, u.email, u.profile_pic, u.team_name, u.designation FROM appreciation a JOIN user u ON a.creator = u.id').fetchall()

        appreciations = []

        for row in rows:
            user = User(
                id_=row[3], name=row[4], email=row[5], profile_pic=row[6], team_name=row[7], designation=row[8]
            )
            appreciation = Appreciation(id_=row[0], content=row[1], created_at=row[2], creator=user)

            appreciations.append(appreciation)

        return appreciations

    def get_like_count(self):
        db = get_db()
        total_likes = db.execute(
            'SELECT COUNT(*) FROM likes where likes.appreciation_id=?', (self.id,)).fetchone()[0]
        return total_likes

    @staticmethod
    def get(id_):
        db = get_db()
        row = db.execute(
            'SELECT a.id, a.content, a.created_at, u.id, u.name, u.email, u.profile_pic, u.team_name, u.designation FROM appreciation a JOIN user u ON a.creator = u.id WHERE a.id=?',
            (id_,)).fetchone()

        user = User(
            id_=row[3], name=row[4], email=row[5], profile_pic=row[6], team_name=row[7], designation=row[8]
        )
        appreciation = Appreciation(id_=row[0], content=row[1], created_at=row[2], creator=user)

        return appreciation
