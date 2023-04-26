import json
import sqlite3
import csv
import subprocess
import win32com.client as win32


DATABASE_PATH = "./data.db"


with open("config.json") as f:
     CONFIG_DATA = json.load(f)


def create_email(subject='[BLANK]', body='[BLANK]', mail_address='person1@gmail.com', cc=''):

     with open("config.json") as f:
          email_body = CONFIG_DATA['email_wrapper'].format(body)

     outlook = win32.Dispatch('outlook.application')
     mail = outlook.CreateItem(0)
     mail.To = mail_address
     mail.Cc = cc
     mail.Subject = subject
     mail.HtmlBody = email_body
     mail.Display(True)


def create_db():
    with sqlite3.connect(DATABASE_PATH) as db:
        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS emails(name TEXT, receiver TEXT, carbon_copy TEXT, subject TEXT, body TEXT, uses INTEGER, func TEXT)")


def get_initial_email_data():
    with sqlite3.connect(DATABASE_PATH) as db:
        cur = db.cursor()

        cur.execute("SELECT name FROM emails ORDER BY uses DESC")
        email_names = [item[0] for item in cur.fetchall()]

        cur.execute("SELECT * FROM emails WHERE name = ?", (email_names[0],))
        initial_email = cur.fetchone()

        return email_names, initial_email


def extract_csv_data():
    csv_file_path = CONFIG_DATA['path_of_release_report_as_csv']
    result = list()

    format_docket = lambda docket: docket.replace(',', '')[:-3]

    try:
        with open(csv_file_path) as f:
            inmates = csv.reader(f)
            for item in inmates:
                if len(item) > 19:
                    result.append((f"{item[10]}, {item[11]}", format_docket(item[9])))

            result.sort()
            return result

    except Exception as e:
        return e

def create_text_doc(csv_data: list):
    def add_space(index):
        if index < 9:
            return " "
        return ""
    
    text_doc_path = CONFIG_DATA['path_of_release_report_as_txt']


    with open(text_doc_path, "w") as f:
        for i, inmate in enumerate(csv_data):
            f.write(f"{add_space(i)}{i+1}. {inmate[1]} {inmate[0]}\n")

    subprocess.Popen(["notepad", text_doc_path])


def create_active_release_report():
    csv_data = extract_csv_data()
    create_text_doc(csv_data)