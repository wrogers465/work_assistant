import json
import os
import pythoncom
import re
import requests
import threading
from datetime import datetime
from lxml import html
import win32com.client as win32


with open("config.json") as f:
     CONFIG_DATA = json.load(f)


class InmateNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)

class Email:
    def __init__(self, **kwargs):

        self._template_name = kwargs.get("template_name", None)
        self.subject = kwargs.get("subject", None)
        self.body = kwargs.get("body", None)
        self.receiver = kwargs.get("receiver", None)
        self.cc = kwargs.get("cc", None)
        self.func = kwargs.get("func", None)
        self.attachment = kwargs.get("attachment", None)

    def create(self):
        thread = threading.Thread(target=self._create_email)
        thread.start()        

    def _create_email(self):
        pythoncom.CoInitialize()

        with open("config.json") as f:
            CONFIG_DATA = json.load(f)  # Assuming you wanted to load json here.
            formatted_body = CONFIG_DATA['email_wrapper'].format(self.body)

        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = self.receiver
        try:
            mail.Cc = self.cc
        except AttributeError:
            pass
        mail.Subject = self.subject
        mail.HtmlBody = formatted_body.replace("\n", "<br>")

        if self.attachment and os.path.isfile(self.attachment):
            mail.Attachments.Add(Source=self.attachment)

        mail.Display(True)

    @property
    def template_name(self):
        return self._template_name

    @template_name.setter
    def name(self, template_name):
        self._name = template_name

    def as_list(self):
        return [self.template_name, self.subject, self.body,
                self.to, self.cc, self.function]
    
            
class Inmate:
    
    def __init__(self, docket):

        find = lambda path: self.html.xpath(path)[0].text_content()
        self.docket = str(docket)
        self.html = self._get_html()

        self.lname, self.fname = self._format_name(find('//*[@id="lblName1"]'))
        
        self.short_lname = self.lname
        try:
            self.short_lname = re.split(r'\s|-', self.lname)[0]
        except IndexError:
            pass
            
        self.dob = find('//*[@id="lblDOB1"]')
        self.gender = find('//*[@id="lblSex1"]')
        self.person_id = find('//*[@id="lblSPIN"]')
        self.booking_date = datetime.strptime(find('//*[@id="lblArrestDate1"]'),'%m/%d/%Y %H:%M:%S %p')
        self.housing, self.release_date = self._get_housing(find('//*[@id="CellLocation"]'))

        match self.gender:
            case "MALE":
                self.his_her = "his"
                self.he_she = "he"
            case "FEMALE":
                self.his_her = "her"
                self.he_she = "she"
   
    def as_dict(self):
        return self.__dict__
    
    def _get_housing(self, raw_text):

        housing = None
        release_date = None
        split_housing = raw_text.split('-')
        
        i = {'CEN': [1, 2],
             'CSOD': [1, 3],
             'SD': [1, 3],
             'ND': [1, 3],
             'HD': [2, 3]}.get(split_housing[0], None)

        if i == None:
            if raw_text.startswith('RELEASED'):
                p = r'\d+/\d+/\d+ \d+:\d+ (AM|PM)'
                m = re.search(p, raw_text)
                release_date = m.group()
        else:
            housing = '-'.join(split_housing[i[0]:i[1]])

        return housing, release_date
    
    def _format_name(self, name):
        last_name, first_name = name.title().split(',')
        first_name = first_name.strip().split(' ')[0]

        if last_name.startswith('Mc'):
            try:
                last_name = 'Mc' + last_name[2].upper() + last_name[3:]
            except IndexError:
                pass

        return last_name, first_name
    
    @property
    def charges(self):
        charges = []
        key, key_index = "", -2

        for i, td in enumerate(self.html.xpath('//td')):
            try:
                text = td.text.strip()
                if "Charge Number" in text:
                    charges.append({})
                elif ":" in text:
                    key = text.replace(":", "")
                    key_index = i
                elif (i-1) == key_index:
                    charges[-1][key] = text    
            except AttributeError:
                if(i-1) == key_index:
                    charges[-1][key] = None
        return charges

    
    def _get_html(self):
        base_url = 'https://www.pcsoweb.com/InmateBooking/SubjectResults.aspx?id='
        res = requests.get(base_url + self.docket)
        return html.fromstring(res.content)
