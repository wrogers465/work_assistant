import csv
import os
import sqlite3
import time


CSV_PATH = "./tests/mock_data/server_init_data.csv"
DB_PATH = "./tests/mock_data/data.db"


def create_db():
    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS emails(name TEXT, receiver TEXT, carbon_copy TEXT, subject TEXT, body TEXT, uses INTEGER, func TEXT)")


def main():
    os.remove(DB_PATH)
    time.sleep(5)
    create_db()

    with open(CSV_PATH, encoding='utf-8') as csvfile:
        csv_data = csv.reader(csvfile)
        with sqlite3.connect(DB_PATH) as db:
            cur = db.cursor()
            for row in csv_data:
                cur.execute("INSERT INTO emails VALUES (?, ?, ?, ?, ?, ?, ?)", row)
            db.commit()


if __name__ =="__main__":
    main()