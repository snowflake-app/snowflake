CREATE TABLE one_on_one_action_item (
                                        id            SERIAL PRIMARY KEY,
                                        content       TEXT    NOT NULL,
                                        created_by_id TEXT    NOT NULL,
                                        one_on_one_id INTEGER NOT NULL,
                                        state         INTEGER NOT NULL,
                                        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                    )
