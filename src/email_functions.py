import os
import pyperclip
from datetime import datetime, timedelta
from pypdf import PdfWriter, PdfReader


DOC_PATH = os.path.join(os.getenv("USERPROFILE"), "Documents")

def return_tuple(subject, body, attachment=None):
    return (subject, body, attachment)

def set_cwd(func):

    def wrap(*args, **kwargs):
        current_cwd = os.getcwd()
        os.chdir(DOC_PATH)
        result = func(*args, **kwargs)
        os.chdir(current_cwd)
        return result

    return wrap


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

@set_cwd
def ice_ready_for_pickup(options: dict):
    earliest_time, mtime = 0, 0
    old_file_name = ""
    new_file_name = "detainers_encrypted.pdf"
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if "encrypted" in file or not os.path.isfile(file):
            continue
        mtime = os.path.getmtime(file)
        if mtime > earliest_time:
            earliest_time = mtime
            old_file_name = file
    _encrypt_pdf(old_file_name, new_file_name, "Records1")

    now = datetime.now()
    deadline = (now + timedelta(days=3, minutes=1)).strftime("%H%M on %#m/%#d/%Y")
    greeting = _get_greeting(now)

    subject_args = []
    body_args = [greeting, deadline]

    return return_tuple(subject_args, 
                        body_args,
                        os.path.join(cwd, new_file_name))


def _encrypt_pdf(file, new_file_name, password):

    reader = PdfReader(file)

    pdf_writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        pdf_writer.add_page(reader.pages[i])

    pdf_writer.encrypt(password)

    with open(new_file_name, "wb") as output_pdf:
        pdf_writer.write(output_pdf)


def _get_greeting(now=None) -> str:
    if not now:
        now = datetime.now()
    greeting = ""
    match now.hour:
        case _ if 4 < now.hour < 12:
            greeting = 'morning'
        case _ if now.hour < 18:
            greeting = 'afternoon'
        case _:
            greeting = 'evening'
    return greeting



