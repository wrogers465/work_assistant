
DROP TABLE IF EXISTS emails;
DROP TABLE IF EXISTS inmates_pending_release;

CREATE TABLE emails(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_name TEXT UNIQUE NOT NULL, 
    subject TEXT NOT NULL, 
    body TEXT NOT NULL, 
    receiver TEXT,
    cc TEXT,
    func TEXT,
    options TEXT,
    number_of_uses INTEGER DEFAULT 0 NOT NULL
);

CREATE TABLE inmates_pending_release(
    docket INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    release_datetime TEXT
);