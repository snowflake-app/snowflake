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
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    SELECT o.id, o.created_at,
                    u.id, u.name, u.email, u.profile_pic, u.team_name, u.designation, u.username,
                    u2.id, u2.name, u2.email, u2.profile_pic, u2.team_name, u2.designation, u2.username
                    FROM one_on_one o
                    JOIN "user" u on o.user_id = u.id
                    JOIN "user" u2 on o.created_by_id = u2.id
                    WHERE o.id = %s
                    ''', (one_on_one_id,)
                )
                row = c.fetchone()
                if not row:
                    return None

                user = User(
                    id_=row[2], name=row[3], email=row[4], profile_pic=row[5], team_name=row[6], designation=row[7],
                    username=row[8]
                )

                created_by = User(
                    id_=row[9], name=row[10], email=row[11], profile_pic=row[12], team_name=row[13],
                    designation=row[14],
                    username=row[15]
                )

                one_on_one = OneOnOne(
                    user=user, created_by=created_by, id_=row[0], created_at=row[1]
                )

                return one_on_one

    @staticmethod
    def create(one_on_one):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    INSERT INTO one_on_one (user_id, created_by_id)
                    VALUES (%s, %s) RETURNING id
                    ''', (one_on_one.user.id, one_on_one.created_by.id),
                )
                one_on_one.id = c.fetchone()[0]

    @staticmethod
    def get_by_user(user):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    SELECT o.id, o.created_at,
                    u.id, u.name, u.email, u.profile_pic, u.team_name, u.designation, u.username,
                    u2.id, u2.name, u2.email, u2.profile_pic, u2.team_name, u2.designation, u2.username
                    FROM one_on_one o
                    JOIN "user" u ON o.user_id = u.id
                    JOIN "user" u2 ON o.created_by_id = u2.id
                    WHERE user_id = %s OR created_by_id = %s
                    ORDER BY o.created_at DESC
                    ''', (user.id, user.id)
                )
                rows = c.fetchall()

                one_on_ones = []

                for row in rows:
                    user = User(
                        id_=row[2], name=row[3], email=row[4], profile_pic=row[5], team_name=row[6], designation=row[7],
                        username=row[8]
                    )

                    created_by = User(
                        id_=row[9], name=row[10], email=row[11], profile_pic=row[12], team_name=row[13],
                        designation=row[14],
                        username=row[15]
                    )

                    one_on_one = OneOnOne(
                        user=user, created_by=created_by, id_=row[0], created_at=row[1]
                    )

                    one_on_ones.append(one_on_one)

                return one_on_ones

    def get_action_items(self):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    SELECT i.id, i.content, i.created_by_id, i.state,
                    u.id, u.name, u.email, u.profile_pic, u.team_name, u.designation, u.username
                    FROM one_on_one_action_item i
                    JOIN "user" u ON i.created_by_id = u.id
                    WHERE i.one_on_one_id = %s
                    ''', (self.id,))
                rows = c.fetchall()

                action_items = []

                for row in rows:
                    user = User(
                        id_=row[4], name=row[5], email=row[6], profile_pic=row[7], team_name=row[8], designation=row[9],
                        username=row[10]
                    )

                    action_item = OneOnOneActionItem(content=row[1], created_by=user, one_on_one=self, state=row[3],
                                                     id_=row[0])

                    action_items.append(action_item)

                return action_items


class OneOnOneActionItem:
    def __init__(self, content, created_by, one_on_one, state, id_=-1):
        self.state = state
        self.id = id_
        self.one_on_one = one_on_one
        self.created_by = created_by
        self.content = content

    @staticmethod
    def create(action_item):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    INSERT INTO one_on_one_action_item (content, created_by_id, one_on_one_id, state)
                    VALUES (%s, %s, %s, %s) RETURNING id
                    ''', (
                        action_item.content, action_item.created_by.id, action_item.one_on_one.id,
                        action_item.state),
                )
                action_item.id = c.fetchone()[0]

    def update(self):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    UPDATE one_on_one_action_item set state = %s WHERE id=%s
                    ''', (self.state, self.id,)
                )

    @staticmethod
    def get(_id):
        with get_db() as db:
            with db.cursor() as c:
                c.execute(
                    '''
                    SELECT i.id, i.content, i.created_by_id, i.state,
                    u.id, u.name, u.email, u.profile_pic, u.team_name, u.designation, u.username,
                    o.id, o.created_at,
                    u2.id, u2.name, u2.email, u2.profile_pic, u2.team_name, u2.designation, u2.username,
                    u3.id, u3.name, u3.email, u3.profile_pic, u3.team_name, u3.designation, u3.username
                    FROM one_on_one_action_item i
                    JOIN one_on_one o ON i.one_on_one_id = o.id
                    JOIN "user" u ON o.user_id = u.id
                    JOIN "user" u2 ON o.created_by_id = u2.id
                    JOIN "user" u3 ON o.user_id = u3.id
                    WHERE i.id = %s
                    ''', (_id,))
                row = c.fetchone()

                user = User(
                    id_=row[4], name=row[5], email=row[6], profile_pic=row[7], team_name=row[8], designation=row[9],
                    username=row[10]
                )

                created_by = User(
                    id_=row[13], name=row[14], email=row[15], profile_pic=row[16], team_name=row[17],
                    designation=row[18],
                    username=row[19]
                )

                one_on_one_user = User(
                    id_=row[20], name=row[21], email=row[22], profile_pic=row[23], team_name=row[24],
                    designation=row[25],
                    username=row[26]
                )

                one_on_one = OneOnOne(id_=row[11], created_at=row[12], created_by=created_by, user=one_on_one_user)
                action_item = OneOnOneActionItem(content=row[1], created_by=user, one_on_one=one_on_one, state=row[3],
                                                 id_=row[0])

                return action_item
