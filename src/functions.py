import json
import csv
import subprocess

import src.email_functions
from src.classes import Email, Inmate


with open("config.json") as f:
     CONFIG_DATA = json.load(f)   

def get_inmates_from_csv() -> list:
    csv_file_path = CONFIG_DATA['path_of_release_report_as_csv']
    result = list()

    format_docket = lambda docket: docket.replace(',', '')[:-3]

    try:
        with open(csv_file_path) as f:
            inmates = csv.reader(f)
            for item in inmates:
                if len(item) > 19:
                    result.append((format_docket(item[9]), f"{item[10]}, {item[11]}", None))

            result.sort()
            return result

    except Exception as e:
        return e

def create_active_release_report(csv_data: list):
    def add_space(index):
        if index < 9:
            return " "
        return ""
    
    text_doc_path = CONFIG_DATA['path_of_release_report_as_txt']


    with open(text_doc_path, "w") as f:
        for i, item in enumerate(csv_data):
            docket, name, release_date = item
            if release_date == None:
                f.write(f"{add_space(i)}{i+1}. {docket} {name}\n")
            else:
                f.write(f"{add_space(i)}{i+1}. {docket} {name} - Released: {release_date}\n")

    subprocess.Popen(["notepad", text_doc_path])

def email_factory(docket: str, email_data: dict, options={}) -> Email:
    inmate = Inmate(docket)
    func = email_data["func"]
    subject, body, attachment = ["", "", "", "", ""], ["", "", "", "", ""], None
    if func:
        try:
            subject, body, attachment = getattr(src.email_functions, func)(inmate, options)
        except AttributeError:
            pass

    inmate_as_dict = inmate.as_dict()
    email_data["subject"] = email_data["subject"].format(*subject, **inmate_as_dict)
    email_data["body"] = email_data["body"].format(*body, **inmate_as_dict)
    if attachment:
        email_data["attachment"] = attachment
    email = Email(**email_data)
    return email

def update_inmate_release_times(inmates: list):
    for i, inmate in enumerate(inmates):
        if inmate[2] != None:
            continue

        docket = inmate[0]
        inmate_object = Inmate(docket)
        inmates[i] = (docket, inmate[1], inmate_object.release_date)
    return inmates
        
