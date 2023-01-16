import re
import requests
from datetime import datetime
from lxml import html


class InmateNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)

        
class Inmate:

    URL = 'https://www.pcsoweb.com/InmateBooking/SubjectResults.aspx?id='
    
    def __init__(self, docket):
        
        res = requests.get(Inmate.URL + docket)
        self._root = html.fromstring(res.content)

        find = lambda path: self._root.xpath(path)[0].text_content()

        self.lname, self.fname = self._format_name(find('//*[@id="lblName1"]'))
        
        self.short_lname = self.lname
        try:
            self.short_lname = re.split(r'\s|-', self.lname)[0]
        except IndexError:
            pass
            
        
        self.docket = docket
        self.dob = find('//*[@id="lblDOB1"]')
        self.gender = find('//*[@id="lblSex1"]')
        self.person_id = find('//*[@id="lblSPIN"]')
        self.booking_date = datetime.strptime(find('//*[@id="lblArrestDate1"]'),
                                              '%m/%d/%Y %H:%M:%S %p')
        self.release_date = None
        self.housing = self._get_housing(find('//*[@id="CellLocation"]'))


    @property
    def name(self):
        return f'{self.lname}, {self.fname}'
    
    
    def _get_housing(self, housing):
        
        split_housing = housing.split('-')
        
        i = {'CEN': [1, 2],
             'CSOD': [1, 3],
             'SD': [1, 3],
             'ND': [1, 3],
             'HD': [2, 3]}.get(split_housing[0], None)

        if not i:
            if housing.startswith('RELEASED'):
                p = r'\d+/\d+/\d+ \d+:\d+ (AM|PM)'
                m = re.search(p, housing)
                self.release_date = datetime.strptime(m.group(),
                                                      '%m/%d/%Y %H:%M %p')
                return None

        return '-'.join(split_housing[i[0]:i[1]])
    

    def _format_name(self, name):
        last_name, first_name = name.title().split(',')
        first_name = first_name.strip().split(' ')[0]

        if last_name.startswith('Mc'):
            try:
                last_name = 'Mc' + last_name[2].upper() + last_name[3:]
            except IndexError:
                pass

        return last_name, first_name        
    
       
#FOR DEBUGGING
def main():
    while True:
        print('Enter docket number: ')
        docket = input()
        inmate = Inmate(docket)
        print(inmate.housing,
              inmate.release_date,
              inmate.booking_date,
              inmate.person_id)

if __name__ == '__main__':
    main()
    
