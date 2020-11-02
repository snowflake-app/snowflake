from .comment import Comment
from .mention import Mention
from .user import User
from ..db import get_db


class Appreciation:
    def __init__(self, creator, content, created_at, id_=-1):
        self.id = id_
        self.creator = creator
        self.content = content
        self.created_at = created_at

    @staticmethod
    def create(appreciation):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    INSERT INTO appreciation(content, created_at, creator)
                    VALUES (%s, %s, %s) RETURNING id
                    ''', (appreciation.content, appreciation.created_at, appreciation.creator.id),
                )
                appreciation.id = c.fetchone()[0]

    @staticmethod
    def get_all():
        with get_db() as db:
            with db.cursor() as c:
                c.execute('''
                    SELECT a.id, a.content, a.created_at, u.id, u.name, u.email,
                    u.profile_pic, u.team_name, u.designation, u.username FROM appreciation a
                    JOIN "user" u ON a.creator = u.id ORDER BY a.created_at DESC
                    ''')

                rows = c.fetchall()
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
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    'SELECT COUNT(*) FROM likes l where l.appreciation_id = %s', (self.id,))
                likes = c.fetchone()[0]
                return likes

    def get_comment_count(self):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    'SELECT COUNT(*) FROM comment c where c.appreciation_id = %s', (self.id,))
                comments = c.fetchone()[0]
                return comments

    def is_liked_by(self, user: User):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    'SELECT COUNT(*) FROM likes l WHERE l.appreciation_id = %s AND l.user_id = %s',
                    (self.id, user.id))
                likes = c.fetchone()[0]
                return likes > 0

    @staticmethod
    def get(id_):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    SELECT a.id, a.content, a.created_at,
                    u.id, u.name, u.email, u.profile_pic, u.team_name, u.designation, u.username
                    FROM appreciation a
                    JOIN "user" u ON a.creator = u.id
                    WHERE a.id=%s
                    ''', (id_,))
                row = c.fetchone()

                user = User(
                    id_=row[3], name=row[4], email=row[5], profile_pic=row[6], team_name=row[7], designation=row[8],
                    username=row[9]
                )
                appreciation = Appreciation(id_=row[0], content=row[1], created_at=row[2], creator=user)

                return appreciation

    def get_mentions(self):
        with get_db() as db:
            with db.cursor() as c:
                mentions = []
                c.execute(
                    '''
                    SELECT m.id,
                    u.id, u.name, u.email, u.profile_pic, u.team_name, u.designation, u.username
                    FROM mention m
                    JOIN "user" u ON m.user_id = u.id
                    WHERE m.appreciation_id = %s
                    ''', (self.id,))
                rows = c.fetchall()

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
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    SELECT COUNT(*) FROM appreciation a
                    WHERE a.creator = %s
                    ''', (user.id,))
                return c.fetchone()[0]

    @staticmethod
    def most_appreciated():
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    SELECT user_id, COUNT(user_id) AS c FROM mention
                    GROUP BY user_id ORDER BY c DESC LIMIT 5
                    ''')

                rows = c.fetchall()
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
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    'SELECT c.id, c.content, c.created_at, u.id, u.name, u.email,'
                    ' u.profile_pic, u.team_name, u.designation, u.username FROM comment c'
                    ' JOIN "user" u ON c.user_id = u.id Where c.appreciation_id=%s ORDER BY c.created_at DESC',
                    (self.id,))

                rows = c.fetchall()
                comments = []

                for row in rows:
                    user = User(
                        id_=row[3], name=row[4], email=row[5], profile_pic=row[6], team_name=row[7], designation=row[8],
                        username=[9]
                    )
                    comment = Comment(id_=row[0], content=row[1], created_at=row[2], user=user, appreciation=self)

                    comments.append(comment)

                return comments
