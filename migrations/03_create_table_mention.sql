CREATE TABLE IF NOT EXISTS mention (
                                       id              SERIAL PRIMARY KEY,
                                       appreciation_id INTEGER NOT NULL,
                                       user_id         TEXT    NOT NULL
                                   )
