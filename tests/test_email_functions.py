from .context import email_functions
import os


def test_ice_ready_for_pick_up():
    doc_path = email_functions.DOC_PATH
    new_file_name = "detainers_encrypted.pdf"
    try:
        os.remove(os.path.join(doc_path, new_file_name))
    except FileNotFoundError:
        pass
    result = email_functions.ice_ready_for_pickup({})
    print(result)