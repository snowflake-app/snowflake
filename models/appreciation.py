from db import get_db
from models.comment import Comment
from models.mention import Mention
from models.user import User


class Appreciation:
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
        appreciation.id = db.execute("SELECT LAST_INSERT_ROWID()").fetchone()[0]
        db.commit()

    @staticmethod
    def get_all():
        db = get_db()
        rows = db.execute(
            'SELECT a.id, a.content, a.created_at, u.id, u.name, u.email,'
            ' u.profile_pic, u.team_name, u.designation, u.username FROM appreciation a'
            ' JOIN user u ON a.creator = u.id ORDER BY a.created_at DESC').fetchall()

        appreciations = []

        for row in rows:
            user = User(
                id_=row[3], name=row[4], email=row[5], profile_pic=row[6], team_name=row[7], designation=row[8],
                username=row[9]
            )
            appreciation = Appreciation(id_=row[0], content=row[1], created_at=row[2], creator=user)

            appreciations.append(appreciation)

        return appreciations

    def get_like_count(self):
        db = get_db()
        total_likes = db.execute(
            'SELECT COUNT(*) FROM likes where likes.appreciation_id=?', (self.id,)).fetchone()[0]
        return total_likes

    def is_liked_by(self, user: User):
        db = get_db()
        is_liked = db.execute(
            'SELECT COUNT(*) FROM likes where likes.appreciation_id=? and likes.user_id=?',
            (self.id, user.id)).fetchone()[0]
        return is_liked > 0

    @staticmethod
    def get(id_):
        db = get_db()
        row = db.execute(
            'SELECT a.id, a.content, a.created_at, u.id, u.name, u.email, u.profile_pic, u.team_name, u.designation, u.username FROM appreciation a JOIN user u ON a.creator = u.id WHERE a.id=?',
            (id_,)).fetchone()

        user = User(
            id_=row[3], name=row[4], email=row[5], profile_pic=row[6], team_name=row[7], designation=row[8],
            username=row[9]
        )
        appreciation = Appreciation(id_=row[0], content=row[1], created_at=row[2], creator=user)

        return appreciation

    def get_mentions(self):
        db = get_db()
        mentions = []
        rows = db.execute(
            'SELECT m.id, u.id, u.name, u.email, u.profile_pic,'
            ' u.team_name, u.designation, u.username FROM mention m JOIN '
            'user u ON m.user_id = u.id where m.appreciation_id=?',
            (self.id,)).fetchall()

        for row in rows:
            user = User(
                id_=row[1], name=row[2], email=row[3], profile_pic=row[4], team_name=row[5], designation=row[6],
                username=[7]
            )
            mention = Mention(user=user, appreciation=self, id_=row[0])

            mentions.append(mention)

        return mentions

    @staticmethod
    def count_by_user(user: User):
        db = get_db()
        return db.execute('SELECT COUNT(*) FROM appreciation a WHERE a.creator = ?', (user.id,)).fetchone()[0]

    @staticmethod
    def most_appreciated():
        db = get_db()
        rows = db.execute('select user_id, count(user_id) as c from mention group by user_id order by c desc limit 5')

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
        db = get_db()
        rows = db.execute(
            'SELECT c.id, c.content, c.created_at, u.id, u.name, u.email,'
            ' u.profile_pic, u.team_name, u.designation, u.username FROM comment c'
            ' JOIN user u ON c.user_id = u.id Where c.appreciation_id=? ORDER BY c.created_at DESC',
            (self.id,)).fetchall()

        comments = []

        for row in rows:
            user = User(
                id_=row[3], name=row[4], email=row[5], profile_pic=row[6], team_name=row[7], designation=row[8],
                username=[9]
            )
            comment = Comment(id_=row[0], content=row[1], created_at=row[2], user=user, appreciation=self)

            comments.append(comment)

        return comments
