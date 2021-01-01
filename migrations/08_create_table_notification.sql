create TABLE "notification" (
                                        id            SERIAL PRIMARY KEY,
                                        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        user_id TEXT    NOT NULL,
                                        type    VARCHAR NOT NULL,
                                        object_id VARCHAR NOT NULL,
                                        read      BOOLEAN DEFAULT FALSE
                                    )
