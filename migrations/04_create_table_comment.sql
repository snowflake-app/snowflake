CREATE TABLE comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appreciation_id INTEGER NOT NULL,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
)
