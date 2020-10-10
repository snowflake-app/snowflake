CREATE TABLE one_on_one_action_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_by_id TEXT NOT NULL,
    one_on_one_id INTEGER NOT NULL,
    state INTEGER NOT NULL
)
