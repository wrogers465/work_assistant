import tkinter as tk
from functions import email_factory, create_active_release_report
from db import Database
import time
from threading import Thread


class UserInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        self._db = Database()
        self._center_window()

        self.title('Work Assistant')
        self.bind('<Return>', self._create_email)
        
        post_frm = tk.Frame(self, borderwidth=2, relief="groove")
        options_frm = tk.Frame(self)

        #post_frm objects:
        self.dkt_entry = tk.Entry(post_frm)
        self.dkt_entry.focus()

        self.email_options = self._db.get_email_options()

        self.selected_email = tk.StringVar(self)
        self.selected_email.set(self.email_options[0])
        self._set_current_email()
        
        email_menu = tk.OptionMenu(post_frm, self.selected_email, *self.email_options)

        self.selected_email.trace('w', self._set_current_email)
        
        create_email_btn = tk.Button(post_frm,
                                  text='Create Email',
                                  width=10,
                                  command=self._create_email)
        
        add_email_template_btn = tk.Button(post_frm,
                                     text="Edit Templates",
                                     command=lambda self=self: AddEmailWindow(self))

        #options_frm objects:
        
        admin_tasks_btn = tk.Button(options_frm,
                                    text="Admin Tasks",
                                    command=lambda self=self: AdminTasksWindow(self))

        post_frm.grid(row=0, column=0, padx=10, pady=10)
        options_frm.grid(row=0, column=1)
        
        self.dkt_entry.grid(columnspan=2 ,padx=10, pady=10)
        email_menu.grid(row=1, columnspan=2, padx=5, pady=5)
        create_email_btn.grid(row=2, column=0, padx=5, pady=5)
        add_email_template_btn.grid(row=2, column=1, padx=5, pady=5)

        admin_tasks_btn.grid()
    

    def _center_window(self):
        windowWidth = 320
        windowHeight = 140
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        xCoord = int((screenWidth/2) - (windowWidth/2))
        yCoord = int((screenHeight/2) - (windowHeight/2))

        self.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCoord, yCoord))

    def _create_email(self, event=None):
        docket = self.dkt_entry.get()
        template_name = self.selected_email.get()
        self.dkt_entry.delete(0, tk.END)
        # if len(docket) != 7 or not docket.isnumeric():
        #     return None

        email_data = self._db.get_email_by_template_name(template_name)
        
        email = email_factory(docket, email_data)
        email.create()

    def _set_current_email(self, *args) -> dict:
        template_name = self.selected_email.get()
        current_email = self._db.get_email_by_template_name(template_name)
        self.current_email = current_email

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.close()


class AddEmailWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.title("Template Editor")
        template_menu_frame = tk.Frame(self)
        entry_frame = tk.Frame(self)
        text_box_frame = tk.Frame(self)
        button_frame = tk.Frame(self)
        notice_frame = tk.Frame(self)

        self.selected_email = tk.StringVar(self)
        self.selected_email.set(parent.selected_email.get())
        self.selected_email.trace("w", self._set_fields)
        template_menu_label = tk.Label(template_menu_frame, text="Template:")
        email_menu = tk.OptionMenu(template_menu_frame, self.selected_email, *parent.email_options)

        template_name_label = tk.Label(entry_frame, text="Name:")
        self.template_name_entry = tk.Entry(entry_frame, width=25)

        subject_label = tk.Label(entry_frame, text="Subject:")
        self.subject_entry = tk.Entry(entry_frame, width=35)

        receiver_label = tk.Label(entry_frame, text="To:")
        self.receiver_entry = tk.Entry(entry_frame, width=50)

        cc_label = tk.Label(entry_frame, text="Cc:")
        self.cc_entry = tk.Entry(entry_frame, width=50)

        func_label = tk.Label(entry_frame, text="Function:")
        self.func_entry = tk.Entry(entry_frame, width=15)

        body_label = tk.Label(text_box_frame, text="Body:")
        self.body_text_box = tk.Text(text_box_frame, height=15, width=75)

        save_button = tk.Button(button_frame, text="Save", width=10, command=self._save)
        self.notice_label = tk.Label(notice_frame, text="")

        self._set_fields(parent.current_email)

        #***GRIDDING***
        template_menu_frame.grid()
        template_menu_label.grid(row=0, column=0)
        email_menu.grid(row=0, column=1)

        entry_frame.grid(padx=10, pady=10, sticky="w")
        template_name_label.grid(row=0, column=0, sticky="e")
        self.template_name_entry.grid(row=0, column=1, sticky="w")

        subject_label.grid(row=1, column=0, sticky="e")
        self.subject_entry.grid(row=1, column=1, sticky="w")

        #entry frame column 2, 3
        receiver_label.grid(row=0, column=2, padx=7, pady=2, sticky="e")
        self.receiver_entry.grid(row=0, column=3)

        cc_label.grid(row=1, column=2, padx=7, pady=2, sticky="e")
        self.cc_entry.grid(row=1, column=3)

        func_label.grid(row=2, column=2, padx=7, pady=2, sticky="e")
        self.func_entry.grid(row=2, column=3, sticky="w")

        text_box_frame.grid(padx=10, pady=10)
        body_label.grid(row=0, column=0, sticky="e")
        self.body_text_box.grid(row=0, column=1, sticky="w")

        button_frame.grid()
        save_button.grid(row=0, column=0, padx=10, pady=10)

        notice_frame.grid()
        self.notice_label.grid()       

    def _save(self):
        email_data = {
            "template_name": self.template_name_entry.get(),
            "subject": self.subject_entry.get(),
            "body": self.body_text_box.get("1.0", tk.END).strip(),
            "receiver": self.receiver_entry.get(),
            "cc": self.cc_entry.get(),
            "func": self.func_entry.get()
        }
        self.parent._db.save_email(email_data)

        self._empty_fields()

        self._give_notice_thread(f"Email template \"{email_data['template_name']}\" successfully saved.")

    def _give_notice_thread(self, message):
        Thread(target=self._give_notice, args=(message,)).start()

    def _give_notice(self, message):
        self.notice_label.config(text=message)
        time.sleep(3)
        self.notice_label.config(text="")


    def _set_fields(self, *args):
        self.parent.selected_email.set(self.selected_email.get())
        email_data = self.parent.current_email
        self._empty_fields()
        self.template_name_entry.insert(0, email_data["template_name"])
        self.subject_entry.insert(0, email_data["subject"])
        self.body_text_box.insert("1.0", email_data["body"])
        self.receiver_entry.insert(0, email_data["receiver"])
        self.cc_entry.insert(0, email_data["cc"])
        self.func_entry.insert(0, email_data["func"])


    def _empty_fields(self):
        self.template_name_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.body_text_box.delete("1.0", tk.END)
        self.receiver_entry.delete(0, tk.END)
        self.cc_entry.delete(0, tk.END)
        self.func_entry.delete(0, tk.END)


class AdminTasksWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Admin Tasks")

        active_release_report_lbl = tk.Label(self, text="Generate Active Report:")
        active_release_report_btn = tk.Button(self,
                                              text="Run",
                                              command=create_active_release_report,
                                              width=15)
        active_release_report_lbl.grid(row=0, column=0, padx=10, pady=10)
        active_release_report_btn.grid(row=0, column=1, padx=10, pady=10)

if __name__ == '__main__':
    window = UserInterface()
    window.mainloop()
