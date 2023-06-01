DROP TABLE IF EXISTS inmates_pending_release;

CREATE TABLE inmates_pending_release(
    docket INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    release_datetime TEXT
);