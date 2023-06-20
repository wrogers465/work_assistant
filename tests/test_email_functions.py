from .context import email_functions
import pyperclip


def test_get_emails():
    clipboard_content = """Smith, John A
jsmith14@pcsonet.com	54408	Inmate Records Specialist I
Inmate Records Shift 2
CC:  7420-002	727-773-1403 (Primary)


727-464-6345 (Office)	Fri/Sat Off

Serrano, Jacob M
jserrano@pcsonet.com	55797	Inmate Records Specialist III
Inmate Records Shift 2
CC:  7420-002	727-991-2345(Primary)

727-397-7327 (Tertiary)
727-464-6345 (Office)	Sat/Sun Off
"""
    pyperclip.copy(clipboard_content)
    email_functions.get_emails()
    email_string = pyperclip.paste()
    assert email_string == "jsmith14@pcsonet.com; jserrano@pcsonet.com"
