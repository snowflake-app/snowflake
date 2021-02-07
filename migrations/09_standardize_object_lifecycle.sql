ALTER TABLE comment
    RENAME COLUMN user_id TO created_by_id;

ALTER TABLE "like"
    RENAME COLUMN user_id TO created_by_id;

ALTER TABLE "like"
    ADD COLUMN created_at TIMESTAMP DEFAULT now();

ALTER TABLE mention
    ADD COLUMN created_by_id TEXT;

ALTER TABLE mention
    ADD COLUMN created_at TIMESTAMP DEFAULT now();

ALTER TABLE "user"
    ADD COLUMN created_at TIMESTAMP DEFAULT now();


UPDATE mention
SET
    created_at    = appreciation.created_at,
    created_by_id = appreciation.created_by_id
FROM
    appreciation
WHERE
    mention.appreciation_id = appreciation.id;
