CREATE TABLE comment (
                         id              SERIAL PRIMARY KEY,
                         appreciation_id INTEGER   NOT NULL,
                         user_id         TEXT      NOT NULL,
                         content         TEXT      NOT NULL,
                         created_at      TIMESTAMP NOT NULL
                     )
