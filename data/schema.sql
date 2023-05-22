
DROP TABLE IF EXISTS emails;

CREATE TABLE emails(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_name TEXT UNIQUE NOT NULL, 
    subject TEXT NOT NULL, 
    body TEXT NOT NULL, 
    receiver TEXT,
    cc TEXT,
    func TEXT,
    number_of_uses INTEGER DEFAULT 0 NOT NULL
);