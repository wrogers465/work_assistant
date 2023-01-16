import win32com.client as win32
import os


def Emailer(subject='[BLANK]', body='[BLANK]',
         mail_address='person1@gmail.com', cc=''):

    email_body= f"""<body style="font-family:calibri; font-size:14.5px">{body}
    <br><br><b>Will Rogers</b>
    Inmate Records Shift Supervisor
    Inmate Records Section
    Pinellas County Sheriff’s Office
    (Ph) 727-464-8186, (Fax) 727-464-6113
    </body>
    """
    
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = mail_address
    mail.Cc = cc
    mail.Subject = subject
    mail.HtmlBody = email_body.replace('\n', '<br>')
    mail.Display(True)


if __name__ == '__main__':
    Emailer()

