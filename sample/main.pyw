import pyperclip
import sys
import tkinter as tk

from emailer import Emailer
from inmate import Inmate


class CourtMinutes:
    def __init__(self, text):
        self.text = text

    def find_match(self, dict_, end_fast=False):
        list_ = []
        end_now = False
        for k, v in dict_.items():
            if end_now:
                break
            for item in v:
                if item in self.text:
                    list_.append(k)
                    if end_fast:
                        end_now = True
                    break
        return list_

        


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Monitor Email')
        self.geometry('300x200')
        self.bind('<Return>', self._post_dkt)
        
        post_frm = tk.Frame(self)
        options_frm = tk.Frame(self)

        #post_frm objects:
        self.dkt_entry = tk.Entry(post_frm)
        self.dkt_entry.focus()
        
        self.post_btn = tk.Button(post_frm,
                                  text='Create Email',
                                  width=10,
                                  command=self._post_dkt)

        #options_frm objects:
        self.baker_act_var = tk.IntVar()
        self.baker_act_btn = tk.Checkbutton(options_frm,
                                                                         text='Baker Act',
                                                                         variable=self.baker_act_var)

        
        self.error_lbl = tk.Label(self, text='')

        post_frm.grid(row=0, column=0)
        options_frm.grid(row=0, column=1)
        
        self.dkt_entry.grid(padx=10, pady=10)
        self.post_btn.grid(padx=10, pady=10)

        self.baker_act_btn.grid(padx=10, pady=10)
        
        self.error_lbl.grid(padx=10, pady=10)


    def _update_error_lbl(self, msg):
        self.error_lbl.configure(text=msg)


    def _post_dkt(self, event=None):
        docket = self.dkt_entry.get().strip()
        
        self.dkt_entry.delete(0, tk.END)
        baker_act_var = self.baker_act_var.get()
        self.baker_act_var.set(0)
        
        if len(docket) != 7 and not docket.isnumeric():
            return None

        monitor_types = {'CAM': ['CAM', 'ALCOHOL MONITOR'],
                         'GPS': ['GPS', 'ELECTRONIC MONITOR'],
                         'RBT': ['RBT', 'REMOTE BREATH']}

        release_types = {'S/ROR': ['S/ROR', 'SUPERVISED ROR', 'SROR'],
                         'ROR': ['ROR', 'U/ROR', 'UNSUPERVISED ROR'],
                         'Bond': ['BOND REMAIN', 'BOND AMENDED'],
                         'EMP Transfer': ['SERVED ON GPS',
                                          'TO BE SERVED ON ALTERNATIVE SENTENCING'],
                         'Prob': ['PROBATION']}


        court_minutes = CourtMinutes(pyperclip.paste())
        release_type = court_minutes.find_match(release_types, end_fast=True)
        monitors = court_minutes.find_match(monitor_types)

        body_flag = 'Please advise when to schedule.'
        
        try:
            subject = f'{release_type[0]}'
        except IndexError as e:
            self._update_error_lbl('Could not find the release type in court minutes.')
        
        if 'EMP Transfer' in release_type:
            try:
                monitors.remove('GPS')
            except ValueError:
                pass            

        
        inmate = Inmate(docket)



        match len(monitors):
            case 1:
                subject += f' w/ {monitors[0]}'
            case 2:
                subject += f' w/ {monitors[0]} & {monitors[1]}'
            case default:
                pass


        if baker_act_var == 1:
            
            def get_pronouns(gender):
                return {'MALE': ('He', 'his'),
                              'FEMALE': ('She', 'her')}.get(gender, ('He', 'his'))

            def get_phrasing(release_type):
                match release_type:
                    case 'Bond':
                        return f'has posted {release_type.lower()} and a monitor is a condition of release'
                    case default:
                        return f'was given {release_type} today in court and a monitor is a condition of release'

            pronouns = get_pronouns(inmate.gender)
            phrasing_1 = get_phrasing(release_type[0])
            
            subject += ' (To PEMHS)'
            body_flag = f'''The above subject {phrasing_1}. {pronouns[0]} is also being baker acted and will be transported to PEMHS.

                                  If needed, we can provide PEMHS a hold order instructing that ASU/APAD be called prior to {pronouns[1]} discharge.'''
            
        else:
            subject += f' - {inmate.short_lname}'


        body = f'''Docket: {inmate.docket}
                   Name: {inmate.name}
                   Person ID: {inmate.person_id}
                    

                   {body_flag}


                   Thanks,


                   {court_minutes.text}'''


        Emailer(subject=subject,
                body=body,
                mail_address='ASU + MPU',
                cc='SSs + COC')


if __name__ == '__main__':
    root = GUI()
    root.mainloop()
