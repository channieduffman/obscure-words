DROP TABLE IF EXISTS words;

CREATE TABLE words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT UNIQUE NOT NULL,
    meaning TEXT NOT NULL
);