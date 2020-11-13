ALTER TABLE appreciation
    RENAME COLUMN creator TO created_by_id;

ALTER TABLE "likes"
    RENAME TO "like";

ALTER TABLE one_on_one_action_item
    ALTER state TYPE bool USING state::boolean;
