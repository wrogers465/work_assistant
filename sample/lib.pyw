import csv
import os
import subprocess

def extract_csv_data():
    CSV_FILE_NAME = "nochrg.csv"
    CSV_FILE_PATH = r"C:\Users\wrogers\Documents"
    result = list()

    format_docket = lambda docket: docket.replace(',', '')[:-3]

    try:
        with open(os.path.join(CSV_FILE_PATH, CSV_FILE_NAME)) as f:
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
    
    TEXT_DOC_PATH = r"C:\Users\wrogers\Documents"
    TEXT_DOC_NAME = "inmates.txt"
    FULL_PATH = os.path.join(TEXT_DOC_PATH, TEXT_DOC_NAME)
  

    with open(FULL_PATH, "w") as f:
        for i, inmate in enumerate(csv_data):
            f.write(f"{add_space(i)}{i+1}. {inmate[1]} {inmate[0]}\n")

    subprocess.Popen(["notepad", FULL_PATH])


def active_release_report():
    csv_data = extract_csv_data()
    create_text_doc(csv_data)


def test():
    return 1


