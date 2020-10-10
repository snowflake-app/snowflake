CREATE TABLE IF NOT EXISTS "user" (
                                      id          TEXT PRIMARY KEY,
                                      name        TEXT        NOT NULL,
                                      email       TEXT UNIQUE NOT NULL,
                                      profile_pic TEXT        NOT NULL,
                                      designation TEXT        NOT NULL,
                                      team_name   TEXT        NOT NULL
                                  );

CREATE TABLE IF NOT EXISTS appreciation (
                                            id         SERIAL PRIMARY KEY,
                                            content    TEXT NOT NULL,
                                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                            creator    TEXT NOT NULL
                                        );

CREATE TABLE likes (
                       id              SERIAL PRIMARY KEY,
                       appreciation_id INTEGER NOT NULL,
                       user_id         TEXT    NOT NULL
                   )
