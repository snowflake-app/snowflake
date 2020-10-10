from db import get_db


class OneOnOneActionItem:
    def __init__(self, content, created_by, one_on_one, state, id_=-1):
        self.state = state
        self.id_ = id_
        self.one_on_one = one_on_one
        self.created_by = created_by
        self.content = content

    @staticmethod
    def create(action_item):
        db = get_db()
        params = (
            action_item.content, action_item.created_by.id, action_item.one_on_one.id,
            action_item.state)

        print(params)
        db.execute(
            "INSERT INTO one_on_one_action_item (content, created_by_id, one_on_one_id, state) "
            "VALUES (?, ?, ?, ?)",
            params,
        )
        action_item.id = db.execute("SELECT LAST_INSERT_ROWID()").fetchone()[0]
        db.commit()
