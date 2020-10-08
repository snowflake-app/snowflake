CREATE TABLE IF not exists user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL,
  designation TEXT NOT NULL,
  team_name TEXT NOT NULL
);

CREATE TABLE IF not exists appreciation (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  content TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  creator TEXT NOT NULL
);

CREATE TABLE likes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appreciation_id INTEGER NOT NULL,
    user_id TEXT NOT NULL
)
