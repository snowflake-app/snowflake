ALTER TABLE appreciation
    ADD CONSTRAINT "appreciation_user_fk" FOREIGN KEY
        (created_by_id) REFERENCES "user" (id);

ALTER TABLE comment
    ADD CONSTRAINT "comment_appreciation_fk" FOREIGN KEY
        (appreciation_id) REFERENCES "appreciation" (id),
    ADD CONSTRAINT "comment_user_fk" FOREIGN KEY
        (created_by_id) REFERENCES "user" (id);

ALTER TABLE "like"
    ADD CONSTRAINT "like_user_fk" FOREIGN KEY
        (created_by_id) REFERENCES "user" (id),
    ADD CONSTRAINT "like_appreciation_fk" FOREIGN KEY
        (appreciation_id) REFERENCES "appreciation" (id);

ALTER TABLE mention
    ADD CONSTRAINT "mention_user_created_by_fk" FOREIGN KEY
        (created_by_id) REFERENCES "user" (id),
    ADD CONSTRAINT "mention_appreciation_fk" FOREIGN KEY
        (appreciation_id) REFERENCES "appreciation" (id),
    ADD CONSTRAINT "mention_user_user_fk" FOREIGN KEY
        (user_id) REFERENCES "user" (id);

ALTER TABLE notification
    ADD CONSTRAINT "notification_user_fk" FOREIGN KEY
        (user_id) REFERENCES "user" (id);

ALTER TABLE one_on_one
    ADD CONSTRAINT "one_on_one_user_user_fk" FOREIGN KEY
        (user_id) REFERENCES "user" (id),
    ADD CONSTRAINT "one_on_one_user_created_by_fk" FOREIGN KEY
        (created_by_id) REFERENCES "user" (id);

ALTER TABLE one_on_one_action_item
    ADD CONSTRAINT "one_on_one_action_item_user_fk" FOREIGN KEY
        (created_by_id) REFERENCES "user" (id),
    ADD CONSTRAINT "one_on_one_action_item_one_on_one_fk" FOREIGN KEY
        (one_on_one_id) REFERENCES "one_on_one" (id);
