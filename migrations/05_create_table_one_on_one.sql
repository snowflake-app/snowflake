CREATE TABLE one_on_one (
                            id            SERIAL PRIMARY KEY,
                            created_by_id TEXT NOT NULL,
                            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            user_id       TEXT NOT NULL
                        )
