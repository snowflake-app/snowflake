ALTER TABLE appreciation
    ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE "like"
    ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE "mention"
    ALTER COLUMN created_at SET NOT NULL,
    ALTER COLUMN created_by_id SET NOT NULL;

ALTER TABLE notification
    ALTER COLUMN created_at SET NOT NULL,
    ALTER COLUMN read SET NOT NULL;

ALTER TABLE one_on_one
    ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE one_on_one_action_item
    ALTER COLUMN content SET NOT NULL,
    ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE "user"
    ALTER COLUMN profile_pic DROP NOT NULL,
    ALTER COLUMN username SET NOT NULL;

ALTER TABLE "user"
    ADD CONSTRAINT user_username_unique UNIQUE (username);
