import sqlite3


def main():
    db = sqlite3.connect("./data/data.sqlite")
    with open("./tests/mock_data/test_data.sql") as f:
        db.executescript(f.read())
    db.commit()
    db.close()


if __name__ == '__main__':
    main()