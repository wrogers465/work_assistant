import json
import csv
import os
import subprocess

try:
    from classes import Email, Inmate
    import email_functions
except ModuleNotFoundError:
    from src.classes import Email, Inmate
    import src.email_functions


with open("config.json") as f:
     CONFIG_DATA = json.load(f)   

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


def email_factory(docket: str, email_data: dict, options={}) -> Email:
    inmate = Inmate(docket).as_dict()
    func = email_data["func"]
    if func:
        print(getattr(src.email_functions, func)(options))
        try:
            subject, body, attachment = getattr(src.email_functions, func)(options)
        except AttributeError:
            return (["", "", "", "", ""], ["", "", "", "", ""], None)

    email_data["subject"] = email_data["subject"].format(*subject, **inmate)
    email_data["body"] = email_data["body"].format(*body, **inmate)
    if attachment:
        email_data["attachment"] = attachment
    email = Email(**email_data)
    return email
