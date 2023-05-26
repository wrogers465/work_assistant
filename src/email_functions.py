import os
import pyperclip
from datetime import datetime
from pypdf import PdfWriter, PdfReader


DOC_PATH = os.path.join(os.getenv("USERPROFILE"), "Documents")

def return_tuple(subject, body, attachment=None):
    return (subject, body, attachment)


def monitor_email(options):
    court_minutes = pyperclip.paste().strip()
    if "-----" not in court_minutes:
        return return_tuple(["{}", "{}"], ["{}"])

    release_type = ""
    release_types = {
        "Bond": ["BOND REMAIN", "BOND AMENDED $"],
        "S/ROR": ["SUPERVISED ROR", "S/ROR", "SROR"],
        "ROR": ["UNSUPERVISED ROR", "ROR"],
        "Prob": ["PROBATION"]
    }

    found_release_type = False
    for k, v in release_types.items():
        for partial_sentence in v:
            if partial_sentence in court_minutes:
                release_type = k
                found_release_type = True
                break
        if found_release_type:
            break

    monitors = ""
    monitor_types = {
        "GPS": ["GPS", "ELECTRONIC MONITOR"],
        "CAM": ["CAM", "ALCOHOL MONITOR"],
        "RBT": ["REMOTE BREATH"]
    }

    for k, v in monitor_types.items():
        for partial_sentence in v:
            if partial_sentence in court_minutes:
                if monitors == "":
                    monitors += k
                else:
                    monitors += f" & {k}"
                break

    subject_args = [release_type, monitors]
    body_args = [court_minutes]

    return return_tuple(subject_args, body_args)


def ice_ready_for_pick_up(options: dict):
    folder = os.path.join(os.getenv("USERPROFILE"), "Documents")
    earliest_time, mtime = 0, 0
    newest_file = ""
    for file in os.listdir(folder):
        mtime = os.path.getmtime(os.path.join(folder, file))
        if mtime > earliest_time:
            if "encrypted" not in file:
                earliest_time = mtime
                newest_file = file
    _encrypt_pdf(newest_file, "detainers_encryped.pdf", "Records1")

    return return_tuple()


def _encrypt_pdf(file, new_file_name, password):
    project_directory = os.getcwd()
    os.chdir(DOC_PATH)

    reader = PdfReader(file)

    pdf_writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        pdf_writer.add_page(reader.pages[i])

    pdf_writer.encrypt(password)

    with open(new_file_name, "wb") as output_pdf:
        pdf_writer.write(output_pdf)
    
    os.chdir(project_directory)