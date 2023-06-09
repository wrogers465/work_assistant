import os
import sqlite3
from sqlite3 import Connection


DATA_PATH = "./data"
DATABASE_PATH = "./data/data.sqlite"
SCHEMA_PATH = "./data/schema.sql"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    
class Database(metaclass=Singleton):
    conn: Connection = None

    def __init__(self):
        if self.conn is None:
            if not os.path.isfile(DATABASE_PATH):
                self.conn = sqlite3.connect(DATABASE_PATH)
                with open(SCHEMA_PATH, "r") as f:
                    script = f.read()
                    self.conn.executescript(script)
            else:
                self.conn = sqlite3.connect(DATABASE_PATH)

            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()

    def get_connection(self):
        return self.conn

    def get_email_options(self) -> list:
        self.cursor.execute("SELECT template_name FROM emails ORDER BY number_of_uses DESC")
        return [ fetch[0] for fetch in self.cursor.fetchall() ]
    
    def get_email_by_template_name(self, template_name: str) -> dict:
        self.cursor.execute("SELECT * FROM emails WHERE template_name = ?", (template_name,))
        try:
            return dict(self.cursor.fetchone())
        except TypeError:
            return {}
    
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

    def reset_pending_release_inmates(self, inmate_list: list):
        with open(os.path.join(DATA_PATH, "reset_pending_release_inmates.sql"), "r") as f:
            script = f.read()
            self.conn.executescript(script)

        query = "INSERT INTO pending_release_inmates (docket, name) VALUES (?, ?)"
        self.conn.executemany(query, inmate_list)
        self.conn.commit()        

    def close(self):
        self.conn.commit()
        self.conn.close()