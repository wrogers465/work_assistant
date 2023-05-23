import os
import sqlite3


DATABASE_PATH = "./data/data.sqlite"
SCHEMA_PATH = "./data/schema.sql"


class Database:
    def __init__(self):

        if not os.path.isfile(DATABASE_PATH):
            self.conn = sqlite3.connect(DATABASE_PATH)
            self.conn.executescript(DATABASE_PATH)
        else:
            self.conn = sqlite3.connect(DATABASE_PATH)

        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def get_email_options(self) -> list:
        self.cursor.execute("SELECT template_name FROM emails ORDER BY number_of_uses DESC")
        return [ fetch[0] for fetch in self.cursor.fetchall() ]
    
    def get_email_by_template_name(self, template_name: str) -> dict:
        self.cursor.execute("SELECT * FROM emails WHERE template_name = ?", (template_name,))
        return dict(self.cursor.fetchone())
    
    def save_email(self, email_data: dict):
        for k in email_data:
            if email_data[k] == '':
                email_data[k] = None
        query = f"INSERT OR REPLACE INTO emails ({','.join(email_data.keys())}) VALUES ({','.join(['?' for _ in email_data.values()])})"
        self.cursor.execute(query, tuple(email_data.values()))
        self.conn.commit()

    def delete_email(self, template_name: str):
        query = f"DELETE FROM emails WHERE template_name = ?"
        self.cursor.execute(query, (template_name,))
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()


def init_db():
    db = sqlite3.connect(DATABASE_PATH)
    with open(SCHEMA_PATH) as f:
        db.executescript(f.read())
    db.close()
 

def get_initial_email_data():
    with sqlite3.connect(DATABASE_PATH) as db:
        cur = db.cursor()

        cur.execute("SELECT name FROM emails ORDER BY uses DESC")
        email_names = [item[0] for item in cur.fetchall()]

        cur.execute("SELECT * FROM emails WHERE name = ?", (email_names[0],))
        initial_email = cur.fetchone()

        return email_names, initial_email